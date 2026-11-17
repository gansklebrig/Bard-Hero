# -*- coding: utf-8 -*-
"""
Bard Hero – nach Updates suchen, laden, installieren und aufräumen.

Ein Update holt die neue Version von github.com/gansklebrig/Bard-Hero (Kanal „stabil“ = nur Versionen mit grünen
Tests, „test“ = immer das Neueste), installiert sie mit install.sh und startet Bard Hero neu.

Geladene Updates liegen in  <daten>/updates/bardhero-<version>.zip  (während des Ladens „.teil“).
Daraus ergibt sich beim Aufräumen:
  • eine fertige ZIP der neuesten Version, die noch nicht installiert ist → Installation wurde abgebrochen,
    sie kann ohne neues Herunterladen fortgesetzt werden
  • ZIPs von installierten oder älteren Versionen, „.teil“-Reste, alte Entpack-Ordner in /tmp,
    Lieder, die es nicht mehr gibt, und der Paket-Zwischenspeicher von apt → können weg
"""
import glob
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.request
import zipfile

HIER = os.path.dirname(os.path.abspath(__file__))           # /zynthian/zynthian-my-data/bard-hero
DATEN = os.environ.get("BH_DATEN", "/zynthian/zynthian-my-data/bardhero")
REPO = "gansklebrig/Bard-Hero"
CACHE = os.path.join(DATEN, "updates")
UA = {"User-Agent": "BardHero-Updater"}
LOG = os.path.join(tempfile.gettempdir(), "bardhero-update.log")
APT_CACHE = "/var/cache/apt/archives"


def ver(s):
    try:
        return tuple(int(x) for x in str(s).strip().lstrip("v").split("."))
    except ValueError:
        return (0,)


def installiert():
    try:
        with open(os.path.join(HIER, "VERSION"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "?"


def kanal():
    """(repo, zweig) – Einstellung „Update-Kanal“ in Bard Hero."""
    try:
        with open(os.path.join(DATEN, "einstellungen.json"), encoding="utf-8") as f:
            s = json.load(f)
    except (OSError, ValueError):
        s = {}
    return s.get("update_repo") or REPO, "main" if s.get("update_kanal", "stabil") == "test" else "stabil"


def _holen(url, timeout=10):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read(64).decode("utf-8", "replace").strip()


def pruefen(timeout=10):
    """→ {installiert, neueste, verfuegbar, fehler, zweig}"""
    repo, zweig = kanal()
    raus = {"installiert": installiert(), "neueste": None, "verfuegbar": False, "fehler": None, "zweig": zweig,
            "zeit": time.time()}
    try:
        try:
            neu = _holen(f"https://raw.githubusercontent.com/{repo}/{zweig}/VERSION?t={int(time.time())}", timeout)
        except urllib.error.HTTPError as e:
            if e.code != 404 or zweig == "main":
                raise
            zweig = raus["zweig"] = "main"
            neu = _holen(f"https://raw.githubusercontent.com/{repo}/main/VERSION?t={int(time.time())}", timeout)
        raus["neueste"] = neu
        raus["verfuegbar"] = ver(neu) > ver(raus["installiert"])
    except urllib.error.HTTPError as e:
        raus["fehler"] = f"GitHub antwortet mit Fehler {e.code}"
    except Exception:
        raus["fehler"] = "Kein Internet oder GitHub nicht erreichbar"
    return raus


# ---------------------------------------------------------------------------------------------------------
# Bestand: was liegt herum?
# ---------------------------------------------------------------------------------------------------------
def _groesse(p):
    try:
        if os.path.isdir(p):
            return sum(os.path.getsize(os.path.join(w, f)) for w, _, fs in os.walk(p) for f in fs)
        return os.path.getsize(p)
    except OSError:
        return 0


def zip_version(p):
    """Version in einer Bard-Hero-ZIP (None = kaputt oder keine Bard-Hero-ZIP)."""
    try:
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None:
                return None
            namen = z.namelist()
            if not any(n.endswith("bardhero.py") for n in namen):
                return None
            for n in namen:
                if n.count("/") <= 1 and n.endswith("VERSION"):
                    return z.read(n).decode("utf-8", "replace").strip()
    except (OSError, zipfile.BadZipFile, RuntimeError):
        return None
    return None


def bestand(neueste=None, lieder_ids=None):
    """→ {"bereit": (pfad, version) | None, "weg": [(pfad, groesse, grund)]}"""
    jetzt = ver(installiert())
    bereit = None
    weg = []
    for p in sorted(glob.glob(os.path.join(CACHE, "*"))):
        if p.endswith(".teil"):
            weg.append((p, _groesse(p), "abgebrochener Download"))
            continue
        if not p.endswith(".zip"):
            continue
        v = zip_version(p)
        if v is None:
            weg.append((p, _groesse(p), "beschädigte Datei"))
        elif ver(v) <= jetzt:
            weg.append((p, _groesse(p), f"Version {v} ist schon installiert"))
        elif neueste and ver(v) < ver(neueste):
            weg.append((p, _groesse(p), f"Version {v} ist überholt"))
        elif bereit is None or ver(v) > ver(bereit[1]):
            if bereit:
                weg.append((bereit[0], _groesse(bereit[0]), f"Version {bereit[1]} ist überholt"))
            bereit = (p, v)
    # Entpack-Reste früherer Updates (älter als eine Stunde, damit nichts Laufendes erwischt wird)
    for p in glob.glob(os.path.join(tempfile.gettempdir(), "bardhero-update-*")):
        try:
            if time.time() - os.path.getmtime(p) > 3600:
                weg.append((p, _groesse(p), "Entpack-Rest eines früheren Updates"))
        except OSError:
            pass
    # Lieder, die es nicht mehr gibt
    if lieder_ids:
        for p in glob.glob(os.path.join(DATEN, "lieder", "*")):
            if os.path.isdir(p) and os.path.basename(p) not in lieder_ids:
                weg.append((p, _groesse(p), "Lied gibt es nicht mehr"))
    # Paket-Zwischenspeicher (von der Installation von pygame & Co.)
    debs = glob.glob(os.path.join(APT_CACHE, "*.deb"))
    if debs:
        weg.append((APT_CACHE, sum(_groesse(d) for d in debs), f"Paket-Zwischenspeicher ({len(debs)} Pakete)"))
    return {"bereit": bereit, "weg": weg}


def aufraeumen(weg):
    frei = 0
    for p, g, _ in weg:
        try:
            if p == APT_CACHE:
                subprocess.call(["apt-get", "clean"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
            elif os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
            frei += g
        except (OSError, subprocess.TimeoutExpired):
            pass
    return frei


def groesse_text(n):
    for e, f in (("GB", 1e9), ("MB", 1e6), ("kB", 1e3)):
        if n >= f:
            return f"{n / f:.1f} {e}".replace(".", ",")
    return f"{n} B"


# ---------------------------------------------------------------------------------------------------------
# Laden und Installieren (läuft in einem Faden; Fortschritt in self.stand)
# ---------------------------------------------------------------------------------------------------------
class Updater:
    def __init__(self):
        self.stand = {"aktiv": False, "phase": "", "anteil": 0.0, "text": "", "fehler": None, "fertig": False}
        self.lock = threading.Lock()

    def _setzen(self, **k):
        with self.lock:
            self.stand.update(k)

    def starten(self, version, bereit=None):
        if self.stand["aktiv"]:
            return
        self._setzen(aktiv=True, phase="laden", anteil=0.0, text="", fehler=None, fertig=False)
        threading.Thread(target=self._lauf, args=(version, bereit), daemon=True).start()

    def _lauf(self, version, bereit):
        try:
            pfad = bereit or self._laden(version)
            self._installieren(pfad)
        except Exception as e:
            self._setzen(aktiv=False, fehler=str(e))

    def _laden(self, version):
        os.makedirs(CACHE, exist_ok=True)
        repo, zweig = kanal()
        if zweig != "main":
            try:
                _holen(f"https://raw.githubusercontent.com/{repo}/{zweig}/VERSION")
            except Exception:
                zweig = "main"
        url = f"https://codeload.github.com/{repo}/zip/refs/heads/{zweig}"
        ziel = os.path.join(CACHE, f"bardhero-{version}.zip")
        teil = ziel + ".teil"
        self._setzen(phase="laden", text="Update wird heruntergeladen")
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, \
                    open(teil, "wb") as f:
                total = int(r.headers.get("Content-Length") or 0) or 9_000_000
                n = 0
                while True:
                    b = r.read(64 * 1024)
                    if not b:
                        break
                    f.write(b)
                    n += len(b)
                    if n > 40 * 1024 * 1024:
                        raise RuntimeError("Download ist unerwartet groß")
                    self._setzen(anteil=min(0.97, n / total), text=f"{groesse_text(n)} geladen")
        except Exception as e:
            raise RuntimeError(f"Download fehlgeschlagen ({e}) – hat der Zynthian Internet?")
        v = zip_version(teil)
        if v is None:
            os.remove(teil)
            raise RuntimeError("Die geladene Datei ist beschädigt – bitte nochmal versuchen")
        ziel = os.path.join(CACHE, f"bardhero-{v}.zip")
        os.replace(teil, ziel)
        self._setzen(anteil=1.0, text=f"Version {v} geladen")
        return ziel

    def _installieren(self, pfad):
        self._setzen(phase="installieren", anteil=0.0, text="Wird ausgepackt")
        tmp = tempfile.mkdtemp(prefix="bardhero-update-")
        with zipfile.ZipFile(pfad) as z:
            for name in z.namelist():
                if name.startswith("/") or ".." in name.split("/"):
                    raise RuntimeError("Ungültige ZIP-Datei")
            z.extractall(tmp)
        src = next((w for w, _, fs in os.walk(tmp) if "install.sh" in fs and "bardhero.py" in fs), None)
        if not src:
            shutil.rmtree(tmp, ignore_errors=True)
            raise RuntimeError("In der ZIP fehlt install.sh")
        try:
            os.remove(LOG)
        except OSError:
            pass
        # außerhalb des Spiel-Dienstes installieren (der Dienst wird danach neu gestartet)
        cmd = f"bash '{src}/install.sh' > '{LOG}' 2>&1; echo \"ENDE $?\" >> '{LOG}'; rm -rf '{tmp}'"
        if shutil.which("systemd-run") and not os.environ.get("BH_OHNE_SYSTEMD"):
            subprocess.Popen(["systemd-run", "--no-block", "--collect", "--quiet",
                              f"--unit=bardhero-update-{int(time.time())}", "/bin/bash", "-c", cmd],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["/bin/bash", "-c", cmd], start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t0 = time.monotonic()
        while time.monotonic() - t0 < 600:
            time.sleep(0.4)
            try:
                with open(LOG, encoding="utf-8", errors="replace") as f:
                    zeilen = [z.strip() for z in f if z.strip()]
            except OSError:
                continue
            for z in zeilen:
                m = re.match(r"SCHRITT (\d+)/(\d+) (.*)", z)
                if m:
                    self._setzen(anteil=(int(m.group(1)) - 1) / max(1, int(m.group(2)) - 1), text=m.group(3))
            ende = [z for z in zeilen if z.startswith("ENDE ")]
            if ende:
                if ende[-1] != "ENDE 0" or not any("Fertig!" in z for z in zeilen):
                    letzte = [z for z in zeilen if not z.startswith(("ENDE", "SCHRITT", "=="))][-1:]
                    raise RuntimeError("Installation fehlgeschlagen" + (f": {letzte[0][:80]}" if letzte else ""))
                try:
                    os.remove(pfad)                    # installiert → die ZIP braucht es nicht mehr
                except OSError:
                    pass
                self._setzen(aktiv=False, fertig=True, anteil=1.0, text="Installiert – Bard Hero startet neu")
                return
        raise RuntimeError("Installation hat zu lange gedauert")


def bard_hero_neu_starten():
    cmd = ["systemctl", "restart", "bard-hero.service"]
    if shutil.which("systemd-run"):
        cmd = ["systemd-run", "--no-block", "--collect", "--quiet"] + cmd
    subprocess.Popen(cmd, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
