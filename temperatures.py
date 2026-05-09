"""
temperatures.py - Obté temperatures diàries via Open-Meteo API
===============================================================
Part 2 - T01-Bloc5-0487-ENTORNS
Obté les temperatures horàries d'una ciutat, calcula max/min/mitjana
en Python i exporta els resultats a un fitxer JSON amb la data d'avui.
"""

import requests
import json
from datetime import datetime


# ─── Configuració de la ciutat ────────────────────────────────────────────────
CITY_NAME = "Barcelona"
LATITUDE = 41.3851
LONGITUDE = 2.1734
TIMEZONE = "Europe/Madrid"


def get_temperatures():
    """
    Consulta l'API Open-Meteo per obtenir temperatures horàries del dia actual.
    Calcula max, min i mitjana en Python (no des de l'API).
    Exporta els resultats a temp_YYYYMMDD.json.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "temperature_2m",
        "timezone": TIMEZONE,
        "forecast_days": 1
    }

    print(f"🌍 Obtenint temperatures de {CITY_NAME}...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extreure les temperatures horàries
    temperatures = data["hourly"]["temperature_2m"]
    hores = data["hourly"]["time"]

    # ─── Càlculs en Python ────────────────────────────────────────────────────
    temp_max = max(temperatures)
    temp_min = min(temperatures)
    temp_mitjana = round(sum(temperatures) / len(temperatures), 2)

    # ─── Construir el diccionari resultat ─────────────────────────────────────
    avui = datetime.now().strftime("%Y%m%d")
    data_llegible = datetime.now().strftime("%d/%m/%Y")

    resultat = {
        "ciutat": CITY_NAME,
        "latitud": LATITUDE,
        "longitud": LONGITUDE,
        "data": data_llegible,
        "generació": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperatures_horàries": [
            {"hora": hora, "temperatura_C": temp}
            for hora, temp in zip(hores, temperatures)
        ],
        "resum": {
            "temperatura_maxima_C": temp_max,
            "temperatura_minima_C": temp_min,
            "temperatura_mitjana_C": temp_mitjana,
        },
        "font": "Open-Meteo API (https://open-meteo.com/)"
    }

    # ─── Exportar a JSON ──────────────────────────────────────────────────────
    filename = f"temp_{avui}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(resultat, f, ensure_ascii=False, indent=2)

    print(f"✅ Fitxer guardat: {filename}")
    print(f"   🌡️  Màxima : {temp_max}°C")
    print(f"   🌡️  Mínima : {temp_min}°C")
    print(f"   🌡️  Mitjana: {temp_mitjana}°C")

    return filename


if __name__ == "__main__":
    get_temperatures()
