# Bard Hero – Anleitung

Rhythmusspiel für den Zynthian (Raspberry Pi 5): Du spielst die Melodie eines Liedes – mit Keytar,
Gitarren-Controller, BeatStep, Zynthian-Tasten, Tastatur oder Gamepad –, die Band spielt den Rest. Greifst du
daneben, verstummt die Melodie, bis du wieder triffst.

## Installieren

Am einfachsten aus dem ZynSimple-Mischpult: ⋯ → „🎸 Bard Hero“. Beim ersten Mal lädt ZynSimple Bard Hero von
GitHub, installiert die Spiel-Bausteine (pygame, FluidSynth, Soundfont – braucht Internet, einige Minuten) und
bereitet die Lieder vor (ein paar Minuten, nur einmal).

Von Hand (per SSH, als root):

    cd /tmp && wget -O bh.zip https://codeload.github.com/gansklebrig/Bard-Hero/zip/refs/heads/stabil
    unzip -q bh.zip && bash Bard-Hero-stabil/install.sh
    bard-hero start

Installiert wird nach `/zynthian/zynthian-my-data/bard-hero`, die vorige Version bleibt als `bard-hero.vorher`.
Spielstände, Einstellungen und vorbereitete Lieder liegen getrennt in `/zynthian/zynthian-my-data/bardhero`.

## Updates

Bard Hero sucht beim Start und alle 6 Stunden selbst nach Updates (Einstellungen → Updates → „Automatisch
suchen“). Gibt es eins, steht im Titelmenü „⬆ Update auf Version …“.

- **Kanal Stabil** (Standard): nur Versionen, deren Tests grün sind. **Test**: immer das Neueste.
- Ein Update wird geladen, installiert, und Bard Hero startet von selbst neu.
- **Abgebrochene Installation:** Liegt die neueste Version schon heruntergeladen da, aber ist nicht installiert
  (Strom weg, Neustart …), zeigt Updates „Installation fortsetzen“ – ohne neu herunterzuladen.
- **Aufräumen:** Updates zeigt, was weg kann – alte oder schon installierte Update-Dateien, abgebrochene
  Downloads, Entpack-Reste, Lieder, die es nicht mehr gibt, und den Paket-Zwischenspeicher – und wie viel Platz
  das bringt. Ein Tipp auf „Aufräumen“ löscht genau das.

## MIDI prüfen, MIDI-Kanal, Lautstärke-Drehregler

- **MIDI prüfen** (Einstellungen → MIDI prüfen …): zeigt, welche MIDI-Eingänge gefunden wurden (JACK, USB,
  DIN-Buchse) und jede ankommende Taste mit Gerät, **Kanal** und Note. „Dein Controller sendet auf Kanal X“ –
  mit ✓ (SEL/Enter) wird genau dieser Kanal fest eingestellt. Kommt gar nichts an, liegt es nicht am Kanal,
  sondern an Kabel/Buchse.
- **MIDI-Kanal (Eingang):** „alle“ (Standard) oder nur Kanal 1–16 – andere Kanäle werden dann ignoriert.
- **DIN-Buchse:** Bard Hero liest sie jetzt robuster (auch neben JACK) und stellt die Baudrate selbst richtig,
  wenn nur Datensalat ankommt.
- **Lautstärke:** Drehregler 1 am Zynthian ist überall die Gesamtlautstärke (mit Anzeige), auch mitten im Lied.
  Welcher Regler: Einstellungen → Lautstärke-Drehregler. Am Computer: + / −.

## Mit jedem Gitarren-Controller

- **Controller einrichten:** Nach „drück eine Taste auf deinem Instrument“ zeigt Bard Hero den erkannten Controller
  als kleine Zeichnung. Mit ✓ auf „Controller“ wählst du die Bauform und drückst die Tasten einmal der Reihe nach:
  - *Keytar / Keyboard* – C D E F G (Standard, nichts anzulernen)
  - *5 Tasten in einer Reihe* – klassische Guitar-Hero- und Rock-Band-Gitarren
  - *6 Tasten: 3 oben, 3 unten* – wie Guitar Hero Live
  - *6 Tasten in einer Reihe*
- **3 oben + 3 unten:** Die Notenbahn hat dann 3 Bahnen; jede Note ist ein Plektrum – hell = untere Taste,
  dunkel mit Glutrand = obere Taste. Auf *Leicht* nur die untere Reihe.
- **Gitarren mit Anschlag-Leiste** (USB-Gitarren als Gamepad): Beim Einrichten einmal anschlagen – dann gilt wie im
  Original: Bund greifen und anschlagen. Ohne Anschlag-Leiste zählt jeder Tastendruck sofort.
- USB-Gitarren werden am Namen erkannt („Guitar Hero Live“ → 3 + 3) und die Bauform schon vorgeschlagen.
- Einrichten geht auch unter Einstellungen → „Controller einrichten“. Jedes Gerät merkt sich seine Belegung.

## Rhythmusspiel mit der Keytar

Die dritte App neben Mischpult und DJ-Pult: **Bard Hero**, ein Guitar-Hero-artiges Spiel. Du spielst die Melodie
eines Liedes, die Band spielt den Rest. Greifst du daneben, verstummt die Melodie, bis du wieder triffst.

- **Starten:** ⋯ → „🎸 Bard Hero“, oder Einstellungen → System → Bard Hero, oder BACK 3 s → System-Menü.
  Beim allerersten Start werden einmalig die Spiel-Bausteine installiert (braucht Internet, einige Minuten) und die
  Lieder vorbereitet (ein paar Minuten, nur einmal; man kann schon spielen, sobald das erste Lied fertig ist).
- **13 eigene Lieder** in ganz verschiedenen Stimmungen: Lagerfeuer am Isarufer (gemütlich), Zur Krummen Gans
  (Tavernen-Polka), Funkenflug (Funk/Disco), Glut des Drachen (epischer Power Metal), Neonnebel (Synthwave),
  Die Hexe vom Moor (Folk-Jig im 6/8-Takt), Galopp der Goblins (Ska-Punk), Mondwalzer (Walzer),
  Sturm über Thalgard (Speed Metal), Handpan-Traum (Ambient Techno in D-Kurd), Ritt des Kraken (Surf-Rock),
  Laut und Ehrlich (Pop-Punk) und Die Feuerinsel (Tribal-Finale). Jedes Lied hat einen eigenen bewegten Hintergrund.
- **Spielarten:** *Hero* – die Tasten deines Controllers (Keytar C D E F G, jede Oktave), *Barde* – die echten Töne auf einer Klaviatur.
  Stufen Leicht, Mittel, Schwer, Meister.
- **Zu zweit:** *Duell* (beide die Melodie, wer hat mehr Punkte?) und *Duett* (Spieler 1 Melodie, Spieler 2 Bass).
  Jeder drückt am Anfang eine Taste auf seinem Gerät: Keytar, BeatStep, ein anderes MIDI-Gerät, die Zynthian-Tasten
  (F1–F4 + PLAY), eine Tastatur (1–5) oder ein Gamepad. Andere Tasten: Einstellungen → Tasten anlernen.
- **Inspiration:** goldene Notenfolgen fehlerfrei spielen füllt die Leiste; voll zündet sie selbst (oder per C+G
  gleichzeitig, Pedal oder Modulationsrad) – doppelte Punkte und Feuer.
- **Ton & Mikrofon:** Mikro an Zynthian-Eingang 1 oder 2 – Pegel, Hall und „Musik leiser beim Sprechen“ für
  Kommentatoren. Alle Pegel mit Anzeige, im Spiel jederzeit über die Pause erreichbar.
- **Beamer:** HDMI-Beamer anstecken – das Bild kommt automatisch auf Display und Beamer
  (Einstellungen → Bild: automatisch · Zynthian-Display · Beamer · beide).
- **Grafik:** Ruhig · Mittel · Prächtig – wenn das Bild ruckelt, eine Stufe runter. Verzögerung (z. B. am Beamer)
  misst „Verzögerung messen …“ selbst.
- **Menüs mit der Keytar:** C ▲ · D ▼ · E ◀ · F ▶ · G ✓ · A zurück. Am Zynthian: Pfeile, SEL, BACK, Drehregler.
  Zurück zum Mischpult: Titel → „Zum Mischpult“ oder BACK 3 s halten.
- Kein Blau – auch nicht im Spiel.

## Bedienung

- **Menüs mit der Keytar:** C ▲ · D ▼ · E ◀ · F ▶ · G ✓ · A zurück. Am Zynthian: Pfeile, SEL, BACK.
- **Drehregler 1** = Lautstärke, überall. **BACK 3 s** = Bard Hero verlassen (zum Mischpult, Aus, Neustart).
- Hilfe bei Problemen: `bard-hero pruefen` (per SSH) zeigt Pakete, Dienste, Lieder, Bildschirme und MIDI.
  Ein Absturz landet in `/zynthian/zynthian-my-data/bardhero/absturz.log`.
