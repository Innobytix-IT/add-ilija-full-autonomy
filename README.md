# 🤖 Ilija — Full Autonomy AI Agent

> **A fully autonomous AI agent that works 24/7, generates its own goals, writes new skills on demand, and learns from every experience.**

![Version](https://img.shields.io/badge/version-stable--v1-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-required-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Skills](https://img.shields.io/badge/skills-80%2B-orange)

---

## 🧠 What is Ilija?

Ilija is a fully autonomous AI agent that operates **without any human intervention** around the clock.

It generates its own goals, executes them, evaluates the results — and writes brand new Python skills whenever it needs new capabilities to grow.

```
Plan → Execute → Evaluate → Learn → repeat forever
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔁 **Full Autonomy Loop** | Works 24/7 with zero human input |
| 🧩 **80+ Skills** | Executable Python modules for every task |
| ✍️ **Self-Writing Skills** | Generates new skills on demand |
| 🧠 **Long-Term Memory** | ChromaDB with semantic search (1300+ entries) |
| 🌐 **Multi-Provider** | Gemini, Claude, GPT-4, Ollama (local) |
| 📱 **Moltbook Integration** | Posts, comments, interacts with other agents |
| 📊 **Web Dashboard** | Live log, chat and stats at `localhost:5001` |
| 📈 **Evolution Tracker** | Tracks progress and development over time |
| 🔧 **Self-Improvement** | Analyzes its own mistakes and optimizes itself |

---

## 🚀 Quickstart

```bash
git clone https://github.com/Innobytix-IT/Ilija-Full-Autonomy.git
cd Ilija-Full-Autonomy
cp .env.example .env
nano .env  # Add your API key
bash INSTALL.sh
```

Then open the dashboard: **http://localhost:5001**

---

## ⚙️ Requirements

- Docker + Docker Compose
- **Gemini API Key** (free: [aistudio.google.com](https://aistudio.google.com))
- **Moltbook Account** (optional: [moltbook.com](https://www.moltbook.com))
- 8 GB RAM · 20 GB storage

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│         Web Dashboard (Port 5001)         │
│       Chat  |  Live-Log  |  Stats         │
└────────────────────┬─────────────────────┘
                     │
┌────────────────────▼─────────────────────┐
│                  Kernel                   │
│     LLM Provider: Gemini / Claude / GPT  │
└──────┬──────────────────────┬────────────┘
       │                      │
┌──────▼──────┐    ┌──────────▼──────────┐
│ Goal Engine │    │  Full Autonomy Loop  │
│ Generate &  │    │  Plan → Execute →    │
│ prioritize  │    │  Evaluate → Learn    │
└──────┬──────┘    └──────────┬──────────┘
       │                      │
┌──────▼──────────────────────▼──────────┐
│             Skill Manager               │
│          80+ Python Skills              │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│         ChromaDB Long-Term Memory        │
│         1300+ semantic entries           │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Ilija-Full-Autonomy/
├── full_autonomy_main.py     # Entry point
├── full_autonomy_loop.py     # Core loop
├── kernel.py                 # LLM kernel
├── providers.py              # Gemini / Claude / GPT / Ollama
├── goal_engine.py            # Goal generation
├── skill_manager.py          # Skill management & validation
├── skill_validator.py        # Security check for new skills
├── evolution_tracker.py      # Progress tracking
├── web_server.py             # Dashboard server
├── skills/                   # 80+ Python skills
├── templates/                # Dashboard HTML
├── data/                     # Persistent data
├── memory/                   # ChromaDB long-term memory
└── docker-compose.yml        # Docker setup
```

---

## 🔌 Supported LLM Providers

| Provider | Model | Cost |
|---|---|---|
| **Gemini** | gemini-1.5-pro | Free (API Key) |
| **Claude** | claude-3-sonnet | Pay-per-use |
| **GPT-4** | gpt-4o | Pay-per-use |
| **Ollama** | llama3, mistral, ... | Fully local / free |

---

## 🧩 Skill Examples

Ilija ships with 80+ ready-to-use skills, including:

- `memory.py` — Read/write long-term memory
- `autonomous_web_api_integration.py` — Discover and use APIs autonomously
- `automatic_error_diagnosis_and_repair.py` — Self-healing on errors
- `skill_factory_improved.py` — Dynamically generate new skills
- `moltbook_publish_post.py` — Social media for AI agents
- `crawl_and_analyze_ai_sites.py` — Automatically follow AI news
- `news_aggregator_summarizer.py` — Aggregate and summarize news
- `log_pattern_recognizer.py` — Detect patterns in logs

---

## ⚠️ Known Limitations

- Web search requires active internet access inside the container
- Ollama must be installed separately
- Moltbook rate limits may slow down some skills
- Tested on Linux only (Windows via WSL should work)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Developed by **Innobytix-IT**
Experimental autonomous AI system · February 2026

---

*If you like Ilija, give the repo a ⭐ Star on GitHub!*

---
---

# 🤖 Ilija — Full Autonomy AI Agent (Deutsch)

> **Ein autonomer KI-Agent, der 24/7 arbeitet, eigene Ziele entwickelt, neue Skills schreibt und aus jeder Erfahrung lernt.**

---

## 🧠 Was ist Ilija?

Ilija ist ein vollständig autonomer KI-Agent, der **ohne menschliche Eingriffe** rund um die Uhr arbeitet.

Er generiert eigene Ziele, führt sie aus, bewertet die Ergebnisse — und schreibt bei Bedarf neue Python-Skills, um sich selbst weiterzuentwickeln.

```
Plan → Execute → Evaluate → Learn → repeat forever
```

---

## ✨ Features

| Feature | Beschreibung |
|---|---|
| 🔁 **Vollautonomer Loop** | Arbeitet 24/7 ohne menschlichen Eingriff |
| 🧩 **80+ Skills** | Ausführbare Python-Module für alle Aufgaben |
| ✍️ **Skill-Selbsterstellung** | Schreibt neue Skills bei Bedarf selbst |
| 🧠 **Langzeitgedächtnis** | ChromaDB mit semantischer Suche (1300+ Einträge) |
| 🌐 **Multi-Provider** | Gemini, Claude, GPT-4, Ollama (lokal) |
| 📱 **Moltbook Integration** | Postet, kommentiert, interagiert mit anderen Agenten |
| 📊 **Web-Dashboard** | Live-Log, Chat und Stats unter `localhost:5001` |
| 📈 **Evolution Tracker** | Verfolgt Fortschritt und Entwicklung über Zeit |
| 🔧 **Self-Improvement** | Analysiert eigene Fehler und optimiert sich selbst |

---

## 🚀 Schnellstart

```bash
git clone https://github.com/Innobytix-IT/Ilija-Full-Autonomy.git
cd Ilija-Full-Autonomy
cp .env.example .env
nano .env  # API-Key eintragen
bash INSTALL.sh
```

Dann Dashboard öffnen: **http://localhost:5001**

---

## ⚙️ Voraussetzungen

- Docker + Docker Compose
- **Gemini API Key** (kostenlos: [aistudio.google.com](https://aistudio.google.com))
- **Moltbook Account** (optional: [moltbook.com](https://www.moltbook.com))
- 8 GB RAM · 20 GB Speicher

---

## 🔌 Unterstützte LLM-Provider

| Provider | Modell | Kosten |
|---|---|---|
| **Gemini** | gemini-1.5-pro | Kostenlos (API Key) |
| **Claude** | claude-3-sonnet | Pay-per-use |
| **GPT-4** | gpt-4o | Pay-per-use |
| **Ollama** | llama3, mistral, ... | Komplett lokal/gratis |

---

## ⚠️ Bekannte Limitierungen

- Web-Suche erfordert aktiven Internetzugang im Container
- Ollama muss separat installiert werden
- Moltbook Rate-Limits können einzelne Skills verlangsamen
- Nur auf Linux getestet (Windows via WSL möglich)

---

## 📄 Lizenz

MIT License — frei verwendbar, modifizierbar und verteilbar.

---

*Wenn dir Ilija gefällt, gib dem Repo einen ⭐ Star auf GitHub!*





###############################################################

# 🤖 Ilija — Full Autonomy AI Agent

> **Ein autonomer KI-Agent, der 24/7 arbeitet, eigene Ziele entwickelt, neue Skills schreibt und aus jeder Erfahrung lernt.**

![Version](https://img.shields.io/badge/version-stable--v1-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-required-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Skills](https://img.shields.io/badge/skills-80%2B-orange)

---

## 🧠 Was ist Ilija?

Ilija ist ein vollständig autonomer KI-Agent, der **ohne menschliche Eingriffe** rund um die Uhr arbeitet.

Er generiert eigene Ziele, führt sie aus, bewertet die Ergebnisse — und schreibt bei Bedarf neue Python-Skills, um sich selbst weiterzuentwickeln.

```
Plan → Execute → Evaluate → Learn → repeat forever
```

---

## ✨ Features

| Feature | Beschreibung |
|---|---|
| 🔁 **Vollautonomer Loop** | Arbeitet 24/7 ohne menschlichen Eingriff |
| 🧩 **80+ Skills** | Ausführbare Python-Module für alle Aufgaben |
| ✍️ **Skill-Selbsterstellung** | Schreibt neue Skills bei Bedarf selbst |
| 🧠 **Langzeitgedächtnis** | ChromaDB mit semantischer Suche (1300+ Einträge) |
| 🌐 **Multi-Provider** | Gemini, Claude, GPT-4, Ollama (lokal) |
| 📱 **Moltbook Integration** | Postet, kommentiert, interagiert mit anderen Agenten |
| 📊 **Web-Dashboard** | Live-Log, Chat und Stats unter `localhost:5001` |
| 📈 **Evolution Tracker** | Verfolgt Fortschritt und Entwicklung über Zeit |
| 🔧 **Self-Improvement** | Analysiert eigene Fehler und optimiert sich selbst |

---

## 🚀 Schnellstart

```bash
git clone https://github.com/Innobytix-IT/Ilija-Full-Autonomy.git
cd Ilija-Full-Autonomy
cp .env.example .env
nano .env  # API-Key eintragen
bash INSTALL.sh
```

Dann Dashboard öffnen: **http://localhost:5001**

---

## ⚙️ Voraussetzungen

- Docker + Docker Compose
- **Gemini API Key** (kostenlos: [aistudio.google.com](https://aistudio.google.com))
- **Moltbook Account** (optional: [moltbook.com](https://www.moltbook.com))
- 8 GB RAM · 20 GB Speicher

---

## 🏗️ Architektur

```
┌──────────────────────────────────────────┐
│         Web Dashboard (Port 5001)         │
│       Chat  |  Live-Log  |  Stats         │
└────────────────────┬─────────────────────┘
                     │
┌────────────────────▼─────────────────────┐
│                  Kernel                   │
│     LLM Provider: Gemini / Claude / GPT  │
└──────┬──────────────────────┬────────────┘
       │                      │
┌──────▼──────┐    ┌──────────▼──────────┐
│ Goal Engine │    │  Full Autonomy Loop  │
│ Ziele gene- │    │  Plan → Execute →    │
│ rieren      │    │  Evaluate → Learn    │
└──────┬──────┘    └──────────┬──────────┘
       │                      │
┌──────▼──────────────────────▼──────────┐
│             Skill Manager               │
│          80+ Python Skills              │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│       ChromaDB Langzeitgedächtnis        │
│       1300+ semantische Einträge         │
└─────────────────────────────────────────┘
```

---

## 📁 Projektstruktur

```
Ilija-Full-Autonomy/
├── full_autonomy_main.py     # Einstiegspunkt
├── full_autonomy_loop.py     # Kern-Loop
├── kernel.py                 # LLM-Kernel
├── providers.py              # Gemini / Claude / GPT / Ollama
├── goal_engine.py            # Zielgenerierung
├── skill_manager.py          # Skill-Verwaltung & Validierung
├── skill_validator.py        # Sicherheitsprüfung neuer Skills
├── evolution_tracker.py      # Fortschrittsverfolgung
├── web_server.py             # Dashboard-Server
├── skills/                   # 80+ Python-Skills
├── templates/                # Dashboard HTML
├── data/                     # Persistente Daten
├── memory/                   # ChromaDB Langzeitgedächtnis
└── docker-compose.yml        # Docker-Setup
```

---

## 🔌 Unterstützte LLM-Provider

| Provider | Modell | Kosten |
|---|---|---|
| **Gemini** | gemini-1.5-pro | Kostenlos (API Key) |
| **Claude** | claude-3-sonnet | Pay-per-use |
| **GPT-4** | gpt-4o | Pay-per-use |
| **Ollama** | llama3, mistral, ... | Komplett lokal/gratis |

---

## 🧩 Skill-Beispiele

Ilija bringt über 80 fertige Skills mit, darunter:

- `gedaechtnis.py` — Langzeitgedächtnis lesen/schreiben
- `autonome_web_api_integration.py` — APIs selbst entdecken und nutzen
- `automatische_fehlerdiagnose_und_reparatur.py` — Selbstheilung bei Fehlern
- `skill_factory_improved.py` — Neue Skills dynamisch generieren
- `moltbook_beitrag_veroeffentlichen.py` — Social Media für KI-Agenten
- `crawl_and_analyze_ai_sites.py` — KI-News automatisch verfolgen
- `news_aggregator_summarizer.py` — News aggregieren und zusammenfassen
- `log_pattern_recognizer.py` — Muster in Logs erkennen

---

## ⚠️ Bekannte Limitierungen

- Web-Suche erfordert aktiven Internetzugang im Container
- Ollama muss separat installiert werden
- Moltbook Rate-Limits können einzelne Skills verlangsamen
- Nur auf Linux getestet (Windows via WSL möglich)

---

## 📄 Lizenz

MIT License — frei verwendbar, modifizierbar und verteilbar.

---

## 👤 Autor

Entwickelt von **Innobytix-IT**
Experimentelles autonomes KI-System · Stand: Februar 2026

---

*Wenn dir Ilija gefällt, gib dem Repo einen ⭐ Star auf GitHub!*
