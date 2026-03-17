"""
Aggregates content from a list of URLs and provides a basic summary for each. Fetches web page content, extracts visible text, and generates a truncated summary.

Auto-generiert durch skill_erstellen
Skill-Name: news_aggregator_summarizer
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

def news_aggregator_summarizer(urls: list):
    results = {}
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text, focusing on paragraphs
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs if p.get_text().strip()])

            # If no paragraphs, try to get text from body as a fallback
            if not article_text and soup.body:
                article_text = soup.body.get_text(separator=' ', strip=True)

            # Generate a truncated summary
            summary = article_text[:500] + '...' if len(article_text) > 500 else article_text
            if not summary.strip(): # Ensure summary is not just whitespace
                summary = 'No substantial content found or extracted.'

            results[url] = {'status': 'success', 'summary': summary}
        except requests.exceptions.RequestException as e:
            results[url] = {'status': 'error', 'message': f'Failed to retrieve {url}: {e}'}
        except Exception as e:
            results[url] = {'status': 'error', 'message': f'An unexpected error occurred for {url}: {e}'}
    return results

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [news_aggregator_summarizer]
