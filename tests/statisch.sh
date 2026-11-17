#!/bin/bash
# Code-Prüfung: Python ohne Tippfehler/unbenutzte Namen, Shell-Skripte ohne Syntaxfehler.
set -e
cd "$(dirname "$0")/.."
python3 -m pyflakes *.py lieder tests
for f in bard-hero *.sh; do bash -n "$f"; done
echo "Code-Prüfung: alles sauber"
