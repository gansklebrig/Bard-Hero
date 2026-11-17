#!/bin/bash
# Bard Hero installieren oder aktualisieren (auf dem Zynthian, als root):  bash install.sh
# Kopiert nach /zynthian/zynthian-my-data/bard-hero (die vorige Version bleibt als bard-hero.vorher),
# richtet den Befehl „bard-hero“ und den Dienst ein. Spielstände, Einstellungen und vorbereitete Lieder liegen
# getrennt in /zynthian/zynthian-my-data/bardhero und bleiben erhalten.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${BH_DIR:-/zynthian/zynthian-my-data/bard-hero}"
VER=$(cat "$SRC/VERSION" 2>/dev/null || echo "?")

echo "SCHRITT 1/3 Kopiere Bard Hero $VER"
if [ "$SRC" != "$DEST" ]; then
    if [ -d "$DEST" ]; then
        rm -rf "$DEST.vorher"
        mv "$DEST" "$DEST.vorher"
    fi
    mkdir -p "$DEST"
    cp -r "$SRC"/. "$DEST"/
    rm -rf "$DEST/.git" "$DEST/.github" "$DEST/tests"
fi
find "$DEST" -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
chmod +x "$DEST"/bard-hero "$DEST"/*.sh "$DEST"/*.py 2>/dev/null || true

echo "SCHRITT 2/3 Richte Befehl und Dienst ein"
if [ -d /run/systemd/system ] && [ -z "$BH_KEIN_DIENST" ]; then
    BH_DIR="$DEST" bash "$DEST/bard-hero" einrichten
else
    echo "(kein systemd – Dienst übersprungen)"
fi

echo "SCHRITT 3/3 Fertig"
echo "Fertig! Version $VER ist installiert."
