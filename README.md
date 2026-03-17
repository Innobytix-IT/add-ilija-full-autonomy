# 🤖 Ilija Full Autonomy Edition

Ein vollständig autonomer KI-Agent der rund um die Uhr arbeitet, lernt und sich selbst weiterentwickelt.

![Version](https://img.shields.io/badge/version-stable--v1-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-required-blue)

---

## Was ist Ilija?

Ilija ist ein autonomer KI-Agent der ohne menschliche Eingriffe:

- **Eigene Ziele generiert** und sie Schritt für Schritt ausführt
- **80+ Skills** nutzt und bei Bedarf neue Skills selbst schreibt
- **Auf Moltbook** postet, kommentiert und mit anderen Agenten interagiert
- **Sein Langzeitgedächtnis** (ChromaDB) nutzt um aus Erfahrungen zu lernen
- **Sich selbst verbessert** durch Analyse vergangener Erfolge und Misserfolge
- **Ein Web-Dashboard** bereitstellt zum Beobachten und Chatten

## Architektur

```
┌─────────────────────────────────────────┐
│           Web Dashboard (Port 5001)      │
│        Chat | Live-Log | Stats           │
└───────────────────┬─────────────────────┘
                    │
┌───────────────────▼─────────────────────┐
│              Kernel                      │
│   LLM Provider (Gemini/Claude/GPT)       │
└──────┬──────────────────────┬───────────┘
       │                      │
┌──────▼──────┐    ┌──────────▼──────────┐
│ Goal Engine │    │   Full Autonomy Loop │
│ (Ziele      │    │   Plan → Execute →   │
│  generieren)│    │   Evaluate → Learn   │
└──────┬──────┘    └──────────┬───────────┘
       │                      │
┌──────▼──────────────────────▼───────────┐
│            Skill Manager                 │
│         80+ ausführbare Skills           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         ChromaDB Langzeitgedächtnis      │
│         1300+ gespeicherte Einträge      │
└─────────────────────────────────────────┘
```

## Features

- **Vollautonomer Loop** – Ilija arbeitet 24/7 ohne Eingriff
- **Multi-Provider** – Gemini, Claude, GPT, lokales Ollama
- **Self-Improvement** – analysiert eigene Fehler und lernt daraus
- **Skill-Selbsterstellung** – schreibt neue Python-Skills bei Bedarf
- **Persistentes Gedächtnis** – ChromaDB mit semantischer Suche
- **Moltbook Integration** – soziales Netzwerk für KI-Agenten
- **Web-Dashboard** – Live-Monitoring und Chat-Interface
- **Evolution Tracker** – verfolgt Entwicklung und Fortschritt

## Schnellstart

```bash
git clone https://github.com/Innobytix-IT/Ilija-Full-Autonomy.git
cd Ilija-Full-Autonomy
bash INSTALL.sh
```

Danach Dashboard öffnen: **http://localhost:5000**

## Voraussetzungen

- Docker + Docker Compose
- Gemini API Key (kostenlos: https://aistudio.google.com)
- Moltbook Account (https://www.moltbook.com)
- 8GB RAM, 20GB Speicher

## Konfiguration

```bash
cp .env.example .env
nano .env  # API-Keys eintragen

cp moltbook_config.json.example moltbook_config.json
nano moltbook_config.json  # Moltbook-Zugangsdaten eintragen
```

## Dashboard

Nach der Installation erreichbar unter `http://localhost:5000`

- **Chat** – direkt mit Ilija kommunizieren
- **Live Log** – Aktivitäten in Echtzeit beobachten  
- **Stats** – Skills, Provider, History

## Projektstruktur

```
Ilija-Full-Autonomy/
├── full_autonomy_main.py    # Einstiegspunkt
├── full_autonomy_loop.py    # Kern-Ausführungsloop
├── kernel.py                # LLM-Kernel
├── providers.py             # LLM-Provider (Gemini/Claude/GPT)
├── goal_engine.py           # Ziel-Generierung
├── skill_manager.py         # Skill-Verwaltung
├── web_server.py            # Dashboard-Server
├── skills/                  # 80+ Python-Skills
├── templates/               # Dashboard HTML
├── data/                    # Persistente Daten
├── memory/                  # ChromaDB Langzeitgedächtnis
└── docker-compose.yml       # Docker-Konfiguration
```

## Bekannte Limitierungen

- Web-Suche erfordert Internetzugang im Container
- Ollama (lokales LLM) muss separat installiert werden
- Moltbook Rate-Limits können Skills verlangsamen

## Lizenz

MIT License – frei verwendbar und modifizierbar.

---

Entwickelt als experimentelles autonomes KI-System. Stand: Februar 2026.
