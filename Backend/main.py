# main.py - Backend con FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from fastapi import Query
from api import get_countries

# Definición de modelos Pydantic para validación de datos
class CountryModel(BaseModel):
    name: str
    population: int
    area: int
    density: float
    region: str
    subregion: str

class Top10CountryModel(BaseModel):
    name: str
    metric_value: int

class Top10Response(BaseModel):
    top_10: List[Top10CountryModel]

class FilteredCountryModel(BaseModel):
    name: str
    population: int
    region: str

class StatsResponse(BaseModel):
    metric: str
    mean: float
    median: float
    variance: float
    std_dev: float

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="REST Countries API Dashboard",
    description="API personalizada para análisis y visualización de datos geográficos y demográficos",
    version="1.0"
)

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (ajustar según necesidad)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Endpoint: Obtener todos los países con datos estructurados
@app.get("/api/v1/countries", response_model=List[CountryModel])
async def get_all_countries():
    """
    Devuelve una lista de todos los países con datos estructurados:
    - Nombre
    - Población
    - Área (km²)
    - Densidad poblacional
    - Región
    - Subregión
    """
    try:
        countries = get_countries()
        return [
            {
                "name": country["Nombre"],
                "population": country["Población"],
                "area": country["Área(km²)"],
                "density": country["Densidad(hab/km²)"],
                "region": country["Región"],
                "subregion": country["Subregión"]
            }
            for country in countries
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener datos: {e}"
        ) from e

# Endpoint: Obtener top 10 países por métrica (población, área)
@app.get("/api/v1/top-10/{metric}", response_model=Top10Response)
async def top_10(metric: str = Query(..., regex="^(population|area)$")):
    """
    Devuelve los 10 países con mayor valor en una métrica específica:
    - Metric: "population" o "area"
    Ejemplo: /api/v1/top-10/population
    """
    try:
        countries = get_countries()
        # Validar métrica y ordenar
        if metric == "population":
            sorted_list = sorted(countries, key=lambda x: x["Población"], reverse=True)[:10]
        elif metric == "area":
            sorted_list = sorted(countries, key=lambda x: x["Área(km²)"], reverse=True)[:10]
        else:
            raise HTTPException(status_code=400, detail="Métrica no válida")

        # Transformar a formato esperado
        top_10_data = [
            {"name": country["Nombre"], "metric_value": country["Población"] if metric == "population" else country["Área(km²)"]}
            for country in sorted_list
        ]
        return {"top_10": top_10_data}
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Métrica '{metric}' no válida."
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}") from e

# Endpoint: Filtrar países por región
@app.get("/api/v1/filter", response_model=List[FilteredCountryModel])
async def filter_by_region(region: str):
    """
    Filtra países por región (ej.: "Americas", "Europe")
    Ejemplo: /api/v1/filter?region=Americas
    """
    try:
        countries = get_countries()
        if filtered := [country for country in countries if country["Región"].lower() == region.lower()]:
            return filtered
        else:
            raise HTTPException(status_code=404, detail=f"No se encontraron países en la región '{region}'")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al filtrar datos: {e}"
        ) from e

# Endpoint: Calcular estadísticas básicas
@app.get("/api/v1/stats", response_model=StatsResponse)
async def calculate_stats(metric: str = Query(..., regex="^(population|area|density)$")):
    """
    Calcula estadísticas básicas (media, mediana, varianza, desviación estándar) para una métrica:
    - Metric: "population", "area" o "density"
    """
    try:
        countries = get_countries()
        # Seleccionar métrica
        if metric == "population":
            values = [country["Población"] for country in countries if country["Población"] > 0]
        elif metric == "area":
            values = [country["Área(km²)"] for country in countries if country["Área(km²)"] > 0]
        elif metric == "density":
            values = [country["Densidad(hab/km²)"] for country in countries if country["Densidad(hab/km²)"] > 0]
        else:
            raise HTTPException(status_code=400, detail="Métrica no válida")

        # Calcular estadísticas
        mean = round(sum(values) / len(values), 2)
        median = sorted(values)[len(values) // 2] if len(values) % 2 == 1 else (sorted(values)[len(values)//2 - 1] + sorted(values)[len(values)//2]) / 2
        variance = round(sum((x - mean) ** 2 for x in values) / len(values), 2)
        std_dev = round(variance ** 0.5, 2)

        return {
            "metric": metric,
            "mean": mean,
            "median": median,
            "variance": variance,
            "std_dev": std_dev
        }
    except ZeroDivisionError as e:
        raise HTTPException(
            status_code=400,
            detail="No hay suficientes datos para calcular estadísticas.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al calcular estadísticas: {e}"
        ) from e

# Ruta raíz para verificar que la API está activa
@app.get("/")
async def root():
    return {"message": "API REST Countries - Dashboard Geográfico Interactivo", "version": "1.0"}