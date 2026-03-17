"""
Führt eine Web-Suche (z.B. über DuckDuckGo) für eine gegebene Anfrage durch und gibt eine Liste relevanter URLs zurück.

Auto-generiert durch skill_erstellen
Skill-Name: web_recherche
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
import urllib.parse

def web_recherche(query: str, num_results: int = 10) -> list:
    search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a_tag in soup.find_all('a', class_='result__a'):
            href = a_tag.get('href')
            if href and 'duckduckgo.com/y.js' not in href:
                if href.startswith('http') and 'duckduckgo.com/l/' in href:
                    try:
                        redirect_url_part = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('uddg', [''])[0]
                        actual_url = urllib.parse.unquote(redirect_url_part)
                        if actual_url.startswith('http'):
                            links.append(actual_url)
                    except IndexError:
                        pass 
                elif href.startswith('http'):
                    links.append(href)
            if len(links) >= num_results:
                break
        return list(set(links)) 
    except requests.exceptions.RequestException as e:
        return [f"Error during web search: {e}"]
    except Exception as e:
        return [f"An unexpected error occurred: {e}"]

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [web_recherche]
