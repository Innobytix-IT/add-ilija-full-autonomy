"""
Crawlt eine Liste von KI-bezogenen Websites, extrahiert deren Inhalt und führt eine grundlegende Analyse durch, einschließlich Titel, Zusammenfassung, Wortanzahl, gefundener KI-Schlüsselwörter und einer rudimentären Stimmungsanalyse.

Auto-generiert durch skill_erstellen
Skill-Name: crawl_and_analyze_ai_sites
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
from collections import Counter

def crawl_and_analyze_ai_sites(urls: list) -> dict:
    results = {}
    keywords = [
        "ki", "ai", "künstliche intelligenz", "artificial intelligence",
        "machine learning", "deep learning", "neural networks", "gpt", "llm",
        "datenscience", "data science", "algorithm", "ethik", "automation",
        "robotik", "computer vision", "natural language processing", "nlp",
        "reinforcement learning", "generative ai", "transformer", "modelle",
        "ethischen", "automatisierung", "algorithmen", "modell"
    ]

    positive_words = [
        "innovativ", "fortschritt", "zukunft", "revolution", "verbesserung",
        "effizient", "potential", "ermöglicht", "erfolg", "durchbruch", "chancen",
        "optimierung", "effektiv", "vorteil", "intelligent"
    ]
    negative_words = [
        "herausforderung", "risiko", "ethisch", "probleme", "einschränkung",
        "datenschutz", "missbrauch", "kosten", "komplexität", "fehler",
        "bedenken", "gefahr", "schwierigkeiten", "kontroversen"
    ]

    for url in urls:
        site_analysis = {
            "status": "error",
            "message": "Initialization error",
            "title": "N/A",
            "summary": "N/A",
            "word_count": 0,
            "found_keywords": [],
            "sentiment_score": {"positive": 0, "negative": 0, "overall": "neutral"},
            "raw_text_length": 0
        }
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"
            site_analysis["title"] = title

            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div'])
            all_text_parts = []
            for element in text_elements:
                if element.name not in ['script', 'style'] and element.get_text(strip=True):
                    all_text_parts.append(element.get_text(separator=' ', strip=True))

            all_text = ' '.join(all_text_parts)
            all_text_lower = all_text.lower()
            site_analysis["raw_text_length"] = len(all_text)

            found_keywords = list(set([kw for kw in keywords if kw in all_text_lower]))
            site_analysis["found_keywords"] = found_keywords
            
            positive_count = sum(1 for word in positive_words if word in all_text_lower)
            negative_count = sum(1 for word in negative_words if word in all_text_lower)
            
            sentiment_overall = "neutral"
            if positive_count > negative_count:
                sentiment_overall = "positiv"
            elif negative_count > positive_count:
                sentiment_overall = "negativ"
            
            site_analysis["sentiment_score"] = {
                "positive": positive_count,
                "negative": negative_count,
                "overall": sentiment_overall
            }

            word_count = len(all_text.split())
            site_analysis["word_count"] = word_count

            summary = all_text[:700].rsplit(' ', 1)[0] + "..." if len(all_text) > 700 else all_text
            site_analysis["summary"] = summary
            
            site_analysis["status"] = "success"
            site_analysis["message"] = "Successfully crawled and analyzed."

        except requests.exceptions.HTTPError as e:
            site_analysis["message"] = f"HTTP Error {e.response.status_code}: {e}"
        except requests.exceptions.ConnectionError as e:
            site_analysis["message"] = f"Connection Error: {e}"
        except requests.exceptions.Timeout as e:
            site_analysis["message"] = f"Timeout Error: {e}"
        except requests.exceptions.RequestException as e:
            site_analysis["message"] = f"Request Exception: {e}"
        except Exception as e:
            site_analysis["message"] = f"An unexpected error occurred during processing: {e}"
        
        results[url] = site_analysis
    return results

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [crawl_and_analyze_ai_sites]
