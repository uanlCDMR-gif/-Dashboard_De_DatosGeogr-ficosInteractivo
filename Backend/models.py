# models.py - Modelos de datos para validación con Pydantic

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Modelo base para un país con datos estructurados
class CountryModel(BaseModel):
    """
    Modelo que representa un país con sus atributos geográficos y demográficos.
    """
    name: str
    population: int
    area: int
    density: float
    region: str
    subregion: Optional[str] = None  # Algunos países no tienen subregión definida
    languages: str  # Cadena separada por comas (ej.: "Español, Inglés")
    currencies: str  # Cadena con código y nombre de moneda (ej.: "COP (Peso colombiano)")

# Modelo para el top 10 de países por métrica (población, área)
class Top10CountryModel(BaseModel):
    """
    Modelo que representa un país en el top 10 según una métrica específica.
    """
    name: str
    metric_value: int

# Respuesta para el endpoint `/api/v1/top-10/{metric}`
class Top10Response(BaseModel):
    """
    Modelo que encapsula una lista de países en el top 10.
    """
    top_10: List[Top10CountryModel]

# Modelo para filtrar países por región
class FilteredCountryModel(BaseModel):
    """
    Modelo simplificado para países filtrados por región.
    """
    name: str
    population: int
    region: str

# Modelo para calcular estadísticas básicas (media, mediana, varianza, desviación estándar)
class StatsResponse(BaseModel):
    """
    Modelo que representa estadísticas básicas (media, mediana, varianza, desviación estándar)
    para una métrica específica (población, área o densidad).
    """
    metric: str
    mean: float
    median: float
    variance: float
    std_dev: float

# Modelo para la respuesta completa de países (lista de CountryModel)
class CountryListResponse(BaseModel):
    """
    Modelo que encapsula una lista de países con datos estructurados.
    """
    data: List[CountryModel]

# Modelo para errores y mensajes de respuesta
class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error en la API.
    """
    detail: str

# Modelo para la respuesta de prueba de la API
class RootResponse(BaseModel):
    """
    Modelo para la respuesta inicial de la API.
    """
    message: str
    version: str