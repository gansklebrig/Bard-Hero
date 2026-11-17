#!/bin/bash
# Bard Hero entfernen. Mit --alles auch Spielstände, Einstellungen und vorbereitete Lieder.
DEST="${BH_DIR:-/zynthian/zynthian-my-data/bard-hero}"
systemctl stop bard-hero.service 2>/dev/null
rm -f /etc/systemd/system/bard-hero.service /usr/local/bin/bard-hero
systemctl daemon-reload 2>/dev/null
rm -rf "$DEST" "$DEST.vorher"
[ "$1" == "--alles" ] && rm -rf /zynthian/zynthian-my-data/bardhero
echo "Bard Hero entfernt$([ "$1" == "--alles" ] && echo " (mit allen Daten)")."
systemctl start zynthian.service 2>/dev/null
