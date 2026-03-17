"""
Installiert ein Python-Paket und führt einen grundlegenden Import-Test zur Verifizierung der Installation durch.

Auto-generiert durch skill_erstellen
Skill-Name: install_and_test_python_package
"""

# Standard-Imports für Skills
import random
import time
import math
import datetime
import os
import subprocess
import json
from typing import Optional, List, Dict, Any

# Haupt-Skill-Code
import subprocess
import sys

def install_and_test_python_package(package_name: str):
    """
    Installiert ein Python-Paket und führt grundlegende Tests aus, um die Funktionalität zu verifizieren.
    """
    results = []

    # 1. Installation
    try:
        results.append(f"Versuche, {package_name} zu installieren...")
        install_command = [sys.executable, "-m", "pip", "install", package_name]
        install_process = subprocess.run(install_command, capture_output=True, text=True, check=True)
        results.append(f"Installation von {package_name} erfolgreich.")
        results.append("Pip Output:\n" + install_process.stdout)
    except subprocess.CalledProcessError as e:
        results.append(f"Fehler bei der Installation von {package_name}: {e}")
        results.append("Pip Error Output:\n" + e.stderr)
        return {"status": "error", "message": "\n".join(results)}
    except Exception as e:
        results.append(f"Unerwarteter Fehler bei der Installation: {e}")
        return {"status": "error", "message": "\n".join(results)}

    # 2. Test (Importversuch)
    try:
        results.append(f"Versuche, {package_name} zu importieren, um die Installation zu verifizieren...")
        # Ersetze Bindestriche durch Unterstriche für den Import, da dies oft die Konvention ist.
        # Dies ist ein einfacher Versuch; komplexere Pakete könnten andere Importnamen haben.
        __import__(package_name.replace('-', '_')) 
        results.append(f"Erfolgreich importiert: {package_name}")
        results.append(f"Grundlegender Import-Test für {package_name} erfolgreich.")
    except ImportError as e:
        results.append(f"Fehler beim Importieren von {package_name}: {e}")
        return {"status": "error", "message": "\n".join(results)}
    except Exception as e:
        results.append(f"Unerwarteter Fehler beim Testen: {e}")
        return {"status": "error", "message": "\n".join(results)}
    
    return {"status": "success", "message": "\n".join(results)}


# Registrierung für den SkillManager
AVAILABLE_SKILLS = [install_and_test_python_package]
