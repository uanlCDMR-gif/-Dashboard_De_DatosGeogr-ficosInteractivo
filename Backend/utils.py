# utils.py - Funciones auxiliares para el backend

import statistics
from typing import List, Dict, Any, Optional

def calculate_density(population: int, area: int) -> float:
    """
    Calcula la densidad poblacional (habitantes/km²).
    
    Args:
        population (int): Población total.
        area (int): Área territorial en km².
        
    Returns:
        float: Densidad poblacional redondeada a 2 decimales.
    """
    try:
        if area <= 0:
            return 0.0
        return round(population / area, 2)
    except ZeroDivisionError:
        return 0.0

def calculate_statistics(data: List[Dict[str, Any]], metric: str = "Población") -> Dict[str, float]:
    """
    Calcula métricas estadísticas (media, mediana, varianza, desviación estándar) 
    para un campo numérico específico en una lista de diccionarios.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos procesados de países.
        metric (str): Campo numérico a analizar (ej.: "Población", "Área(km²)", "Densidad(hab/km²)").
        
    Returns:
        Dict[str, float]: Estadísticas básicas (media, mediana, varianza, desviación estándar).
    """
    try:
        # Filtrar valores válidos (mayores a 0)
        values = [country[metric] for country in data if country.get(metric, 0) > 0]
        
        if not values:
            return {
                "mean": 0.0,
                "median": 0.0,
                "variance": 0.0,
                "std_dev": 0.0
            }
        
        mean = round(statistics.mean(values), 2)
        median = round(statistics.median(values), 2)
        variance = round(statistics.variance(values), 2) if len(values) > 1 else 0.0
        std_dev = round(variance ** 0.5, 2) if variance > 0 else 0.0
        
        return {
            "mean": mean,
            "median": median,
            "variance": variance,
            "std_dev": std_dev
        }
    except statistics.StatisticsError as e:
        # Capturar errores de estadísticas (ej.: varianza en listas vacías)
        print(f"Error al calcular estadísticas: {e}")
        return {
            "mean": 0.0,
            "median": 0.0,
            "variance": 0.0,
            "std_dev": 0.0
        }
    except Exception as e:
        print(f"Error inesperado al calcular estadísticas: {e}")
        return {
            "mean": 0.0,
            "median": 0.0,
            "variance": 0.0,
            "std_dev": 0.0
        }

def validate_country_data(country: Dict[str, Any]) -> bool:
    """
    Valida que un país tenga campos clave con valores válidos.
    
    Args:
        country (Dict): Diccionario con datos de un país.
        
    Returns:
        bool: True si los datos son válidos, False en caso contrario.
    """
    required_fields = [
        "Nombre", 
        "Población", 
        "Área(km²)", 
        "Densidad(hab/km²)", 
        "Región", 
        "Subregión"
    ]
    
    for field in required_fields:
        if field not in country:
            print(f"Campo faltante: {field}")
            return False
        if isinstance(country[field], (int, float)) and country[field] < 0:
            print(f"Valor inválido en campo {field}: {country[field]}")
            return False
        if isinstance(country[field], str) and country[field] == "":
            print(f"Campo vacío: {field}")
            return False
    return True

def format_country_output(country: Dict[str, Any], fields: List[str] = None) -> Dict[str, Any]:
    """
    Formatea un país para devolver solo campos específicos.
    
    Args:
        country (Dict): Diccionario con datos de un país.
        fields (List[str], optional): Lista de campos a incluir. Si es None, se usan todos.
        
    Returns:
        Dict[str, Any]: Diccionario con campos seleccionados.
    """
    if fields is None:
        return country
    
    formatted = {}
    for field in fields:
        if field in country:
            formatted[field] = country[field]
    return formatted

def filter_countries_by_region(data: List[Dict[str, Any]], region: str) -> List[Dict[str, Any]]:
    """
    Filtra países por región geográfica.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        region (str): Región geográfica a filtrar (ej.: "Americas").
        
    Returns:
        List[Dict]: Lista de países en la región especificada.
    """
    return [country for country in data if country.get("Región", "").lower() == region.lower()]

def find_extreme_values(data: List[Dict[str, Any]], metric: str = "Población") -> Dict[str, Dict[str, Any]]:
    """
    Encuentra los países con valores extremos (máximo y mínimo) en una métrica específica.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        metric (str): Métrica a analizar (ej.: "Población", "Área(km²)").
        
    Returns:
        Dict[str, Dict]: Diccionario con países de valores extremos.
    """
    if not data:
        return {"max": {}, "min": {}}
    
    try:
        max_country = max(data, key=lambda x: x.get(metric, 0))
        min_country = min(data, key=lambda x: x.get(metric, float('inf')))
        
        return {
            "max": max_country,
            "min": min_country
        }
    except Exception as e:
        print(f"Error al encontrar valores extremos: {e}")
        return {"max": {}, "min": {}}

def interpret_statistics(stats: Dict[str, float], metric: str = "Población") -> str:
    """
    Interpreta estadísticas básicas y genera una descripción contextualizada.
    
    Args:
        stats (Dict): Diccionario con estadísticas (media, mediana, varianza, desviación estándar).
        metric (str): Métrica analizada (ej.: "Población", "Área(km²)").
        
    Returns:
        str: Descripción interpretativa de las estadísticas.
    """
    if stats["mean"] == 0:
        return "No hay suficientes datos para interpretar estadísticas."
    
    interpretation = f"Análisis de {metric}:\n"
    
    # Interpretación de asimetría
    if stats["mean"] > stats["median"] * 1.2:
        interpretation += "- Alta asimetría positiva (valores extremos altos).\n"
    elif stats["median"] > stats["mean"] * 1.2:
        interpretation += "- Alta asimetría negativa (valores extremos bajos).\n"
    else:
        interpretation += "- Distribución simétrica.\n"
    
    # Interpretación de dispersión
    coefficient_of_variation = stats["std_dev"] / stats["mean"] if stats["mean"] > 0 else 0
    if coefficient_of_variation > 1:
        interpretation += "- Alta dispersión entre valores.\n"
    elif coefficient_of_variation > 0.5:
        interpretation += "- Dispersión moderada entre valores.\n"
    else:
        interpretation += "- Baja dispersión entre valores.\n"
    
    # Interpretación de valores extremos
    interpretation += f"- Media: {stats['mean']}\n"
    interpretation += f"- Mediana: {stats['median']}\n"
    interpretation += f"- Desviación estándar: {stats['std_dev']}\n"
    
    return interpretation.strip()

def extract_language_codes(country: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrae códigos de idiomas desde un país estructurado.
    
    Args:
        country (Dict): Diccionario con datos de un país.
        
    Returns:
        Dict[str, str]: Diccionario con códigos de idiomas y sus nombres.
    """
    languages = country.get("Idiomas", "N/A")
    if languages == "N/A":
        return {}
    
    # Ejemplo: "Español, Inglés" -> {"spa": "Español", "eng": "Inglés"}
    language_list = languages.split(", ")
    return {f"lang_{i+1}": lang for i, lang in enumerate(language_list)}

def clean_currency_format(currency_str: str) -> Dict[str, str]:
    """
    Limpia y normaliza el formato de monedas.
    
    Args:
        currency_str (str): Cadena con información de monedas (ej.: "COP (Peso colombiano)").
        
    Returns:
        Dict[str, str]: Diccionario con código y nombre de la moneda.
    """
    if currency_str == "N/A":
        return {"code": "N/A", "name": "N/A"}
    
    try:
        code, name = currency_str.split(" (")
        name = name.replace(")", "").strip()
        return {"code": code, "name": name}
    except ValueError:
        return {"code": "N/A", "name": "Formato inválido"}

def find_country_by_name(data: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    """
    Busca un país por su nombre común.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        name (str): Nombre del país a buscar.
        
    Returns:
        Optional[Dict]: Diccionario con datos del país si se encuentra, None en caso contrario.
    """
    return next((country for country in data if country["Nombre"].lower() == name.lower()), None)

def format_population(population: int) -> str:
    """
    Formatea la población en notación legible (ej.: 1.38M para 1380004385).
    
    Args:
        population (int): Población total.
        
    Returns:
        str: Población formateada.
    """
    if population >= 1_000_000_000:
        return f"{round(population / 1_000_000_000, 2)}B"
    elif population >= 1_000_000:
        return f"{round(population / 1_000_000, 2)}M"
    elif population >= 1_000:
        return f"{round(population / 1_000, 2)}K"
    else:
        return str(population)