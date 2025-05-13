# api.py - Conexión a la API REST Countries y procesamiento de datos

import requests
import json
from typing import List, Dict, Any
from utils import calculate_density  # Función para calcular densidad (población / área)

# URL de la API REST Countries
REST_COUNTRIES_URL = "https://restcountries.com/v3.1/all "

def get_countries() -> List[Dict[str, Any]]:
    """
    Obtiene datos de todos los países desde la API REST Countries y los transforma en una estructura tabular.

    Returns:
        List[Dict]: Lista de diccionarios con datos procesados de cada país.
    """
    try:
        # Realizar solicitud GET a la API REST Countries
        response = requests.get(REST_COUNTRIES_URL, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP (ej.: 404, 500)

        # Parsear respuesta JSON
        raw_data = response.json()

        # Procesar datos crudos y estructurarlos
        structured_data = []
        for country in raw_data:
            # Extraer campos clave con valores predeterminados para evitar KeyError
            name = country.get("name", {}).get("common", "N/A")
            population = country.get("population", 0)
            area = country.get("area", 0)
            region = country.get("region", "N/A")
            subregion = country.get("subregion", "N/A")
            
            # Extraer idiomas como cadena separada por comas
            languages = ", ".join(country.get("languages", {}).values()) or "N/A"
            
            # Extraer monedas como cadena con código y nombre (ej.: "COP (Peso colombiano)")
            currencies = country.get("currencies", {})
            currency_list = []
            for code, info in currencies.items():
                if isinstance(info, dict) and "name" in info:
                    currency_list.append(f"{code} ({info['name']})")
            currency_str = ", ".join(currency_list) or "N/A"

            # Calcular densidad poblacional
            density = calculate_density(population, area)

            # Agregar país estructurado a la lista final
            structured_data.append({
                "Nombre": name,
                "Población": population,
                "Área(km²)": area,
                "Densidad(hab/km²)": density,
                "Región": region,
                "Subregión": subregion,
                "Idiomas": languages,
                "Monedas": currency_str
            })

        return structured_data

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión (ej.: timeout, servidor caído)
        print(f"Error al conectar con la API REST Countries: {e}")
        return []

    except json.JSONDecodeError as e:
        # Manejar errores en el formato JSON de la respuesta
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []

    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"Error inesperado al procesar datos: {e}")
        return []