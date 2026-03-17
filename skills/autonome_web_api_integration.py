"""
Führt dynamische Web-API-Anfragen aus. Ermöglicht die Interaktion mit verschiedenen APIs, indem die HTTP-Methode, URL, Header, Abfrageparameter und Body-Daten dynamisch übergeben werden.

Auto-generiert durch skill_erstellen
Skill-Name: autonome_web_api_integration
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
import json

def autonome_web_api_integration(method: str, url: str, headers: dict = None, params: dict = None, data: dict = None, json_data: dict = None):
    """
    Führt dynamische Web-API-Anfragen aus.
    Ermöglicht die Interaktion mit verschiedenen APIs, indem die HTTP-Methode, URL, Header,
    Abfrageparameter und Body-Daten dynamisch übergeben werden.

    Args:
        method (str): Die HTTP-Methode (z.B. 'GET', 'POST', 'PUT', 'DELETE').
        url (str): Die vollständige URL des API-Endpunkts.
        headers (dict, optional): Ein Dictionary von HTTP-Headern. Defaults to None.
        params (dict, optional): Ein Dictionary von URL-Abfrageparametern. Defaults to None.
        data (dict, optional): Ein Dictionary von Formulardaten für POST/PUT-Anfragen. Defaults to None.
        json_data (dict, optional): Ein Dictionary für den JSON-Body von POST/PUT-Anfragen. Defaults to None.

    Returns:
        dict: Eine Erfolgs- oder Fehlermeldung mit der API-Antwort.
    """
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json_data,
            timeout=30 # Add a timeout for robustness
        )
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        try:
            return {"status": "success", "response": response.json()}
        except json.JSONDecodeError:
            return {"status": "success", "response": response.text}
            
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "message": f"HTTP error occurred: {http_err}", "response_text": http_err.response.text if http_err.response else "N/A"}
    except requests.exceptions.ConnectionError as conn_err:
        return {"status": "error", "message": f"Connection error occurred: {conn_err}"}
    except requests.exceptions.Timeout as timeout_err:
        return {"status": "error", "message": f"Timeout error occurred: {timeout_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"status": "error", "message": f"An unexpected request error occurred: {req_err}"}
    except Exception as e:
        return {"status": "error", "message": f"An unknown error occurred: {e}"}

# Registrierung für den SkillManager
AVAILABLE_SKILLS = [autonome_web_api_integration]
