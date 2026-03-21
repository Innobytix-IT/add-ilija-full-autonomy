"""
Ruft das aktuelle Wetter für Offenburg aus dem Internet ab (Web Scraping) von wetter.com.

Auto-generiert durch skill_erstellen
Skill-Name: wetter_offenburg_abfragen
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
import requests
from bs4 import BeautifulSoup

def wetter_offenburg_abfragen():
    url = "https://www.wetter.com/deutschland/offenburg/DE0007873.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        temperatur = "Nicht gefunden"
        beschreibung = "Nicht gefunden"

        # Versuche, die Temperatur zu finden (häufig in einem Data-Block oder spezifischem Span)
        temp_element = soup.select_one('div.current-weather__temperature > span.c-font__size--50')
        if temp_element:
            temperatur = temp_element.text.strip() + "C"
        else:
            # Fallback für andere potenzielle Selektoren
            temp_element_fallback = soup.find('span', class_='current-weather__temperature-value')
            if temp_element_fallback:
                temperatur = temp_element_fallback.text.strip() + "C"

        # Versuche, die Beschreibung zu finden
        desc_element = soup.select_one('div.current-weather__description')
        if desc_element:
            beschreibung = desc_element.text.strip()
        else:
            # Fallback für andere potenzielle Selektoren
            desc_element_fallback = soup.find('div', class_='weather-condition-text')
            if desc_element_fallback:
                beschreibung = desc_element_fallback.text.strip()

        if temperatur == "Nicht gefunden" and beschreibung == "Nicht gefunden":
            return {"status": "error", "message": "Wetterdaten konnten nicht vollständig extrahiert werden. Die HTML-Struktur der Webseite könnte sich geändert haben oder die Elemente wurden nicht gefunden.", "raw_html_sample": response.text[:500]}
        else:
            return {"status": "success", "temperatur": temperatur, "beschreibung": beschreibung}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Fehler beim Abrufen der Webseite: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Ein unerwarteter Fehler ist aufgetreten: {e}"}

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [wetter_offenburg_abfragen]
