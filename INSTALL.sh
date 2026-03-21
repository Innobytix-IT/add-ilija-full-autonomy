#!/bin/bash
# =============================================================
# Ilija Full Autonomy Edition - Installationsskript
# Ausfuehren mit: bash INSTALL.sh
# =============================================================

set -e

echo ""
echo "============================================"
echo "  Ilija Full Autonomy Edition - Installation"
echo "============================================"
echo ""

# Voraussetzungen prüfen
echo "[CHECK] Prüfe Voraussetzungen..."

if ! command -v docker &> /dev/null; then
    echo "FEHLER: Docker nicht gefunden!"
    echo "Installation: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker compose version &> /dev/null 2>&1 && ! docker compose version &> /dev/null 2>&1; then
    echo "FEHLER: Docker Compose nicht gefunden!"
    exit 1
fi

echo "  Docker: OK"
echo "  Docker Compose: OK"

# .env prüfen
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ""
        echo "WICHTIG: .env Datei wurde erstellt."
        echo "Bitte API-Keys eintragen:"
        echo "  nano .env"
        echo ""
        echo "Danach INSTALL.sh erneut ausführen."
        exit 0
    else
        echo "FEHLER: .env.example nicht gefunden!"
        exit 1
    fi
fi

# Moltbook Config prüfen
if [ ! -f "moltbook_config.json" ]; then
    if [ -f "moltbook_config.json.example" ]; then
        cp moltbook_config.json.example moltbook_config.json
        echo ""
        echo "WICHTIG: moltbook_config.json wurde erstellt."
        echo "Bitte Moltbook-Zugangsdaten eintragen:"
        echo "  nano moltbook_config.json"
        echo ""
        echo "Danach INSTALL.sh erneut ausführen."
        exit 0
    fi
fi

# Gemini API Key prüfen
if grep -q "dein_gemini_key_hier" .env 2>/dev/null; then
    echo ""
    echo "FEHLER: Bitte GEMINI_API_KEY in .env eintragen!"
    echo "Kostenloser Key: https://aistudio.google.com"
    echo "  nano .env"
    exit 1
fi

# Verzeichnisse erstellen
mkdir -p memory logs data

# data/entwicklungsziele.json initialisieren falls nicht vorhanden
if [ ! -f "data/entwicklungsziele.json" ]; then
    echo "[]" > data/entwicklungsziele.json
fi

echo ""
echo "[BUILD] Baue Docker Image..."
docker compose build

echo ""
echo "[START] Starte Ilija..."
docker compose up -d

echo ""
echo "[WAIT] Warte auf Start..."
sleep 10

# Status prüfen
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "============================================"
    echo "  INSTALLATION ERFOLGREICH!"
    echo "============================================"
    echo ""
    echo "  Dashboard: http://localhost:5000"
    echo ""
    echo "Nützliche Befehle:"
    echo "  docker compose logs -f ilija    # Live-Logs"
    echo "  docker compose stop             # Stoppen"
    echo "  docker compose start            # Starten"
    echo "  docker compose restart ilija    # Neustarten"
    echo ""
else
    echo ""
    echo "FEHLER beim Start! Logs prüfen:"
    echo "  docker compose logs ilija"
    exit 1
fi
