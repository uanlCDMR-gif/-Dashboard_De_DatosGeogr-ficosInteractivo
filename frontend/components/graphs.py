# graphs.py - Componentes gráficos reutilizables para el dashboard

import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Optional

def generate_choropleth_map(data: List[Dict[str, Any]], metric: str = "Densidad(hab/km²)") -> px.choropleth:
    """
    Genera un mapa de calor (choropleth) basado en una métrica específica.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos procesados de países.
        metric (str): Métrica a visualizar en el mapa (ej.: "Población", "Densidad").
        
    Returns:
        px.choropleth: Mapa interactivo de Plotly.
    """
    try:
        # Convertir datos a DataFrame para Plotly
        df = pd.DataFrame(data)
        
        # Validar que los campos necesarios existan
        required_fields = ["Nombre", metric]
        for field in required_fields:
            if field not in df.columns:
                raise ValueError(f"Campo faltante en los datos: {field}")
        
        # Crear el mapa de calor
        fig = px.choropleth(
            df,
            locations="Nombre",
            locationmode="country names",
            color=metric,
            hover_name="Nombre",
            color_continuous_scale="Viridis",
            title=f"Distribución Mundial de {metric.capitalize()}"
        )
        return fig
    except Exception as e:
        print(f"Error al generar el mapa de calor: {e}")
        return px.choropleth(title="Error al cargar el mapa")

def generate_bar_chart(data: List[Dict[str, Any]], metric: str = "Población", top_n: int = 10) -> px.bar:
    """
    Genera un gráfico de barras con los países que tienen los valores más altos en una métrica.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos procesados de países.
        metric (str): Métrica a visualizar (ej.: "Población", "Área(km²)").
        top_n (int): Número de países a mostrar (ej.: 10).
        
    Returns:
        px.bar: Gráfico de barras interactivo.
    """
    try:
        # Convertir datos a DataFrame
        df = pd.DataFrame(data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Filtrar top N países por métrica
        df_sorted = df.sort_values(by=metric, ascending=False).head(top_n)
        
        # Crear gráfico de barras
        fig = px.bar(
            df_sorted,
            x="Nombre",
            y=metric,
            title=f"Top {top_n} Países por {metric.capitalize()}",
            labels={"Nombre": "País", metric: metric.capitalize()}
        )
        fig.update_layout(xaxis_title="País", yaxis_title=metric.capitalize())
        return fig
    except Exception as e:
        print(f"Error al generar el gráfico de barras: {e}")
        return px.bar(title="Error al cargar el gráfico")

def generate_line_chart(data: List[Dict[str, Any]], metric: str = "Población", region: str = "Americas") -> px.line:
    """
    Genera un gráfico de líneas con datos históricos (simulados) de una métrica en una región.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        metric (str): Métrica a visualizar (ej.: "Población").
        region (str): Región geográfica a analizar.
        
    Returns:
        px.line: Gráfico de líneas interactivo.
    """
    try:
        # Simular datos históricos (ej.: crecimiento poblacional)
        df = pd.DataFrame(data)
        filtered = df[df["Región"].str.contains(region, case=False, na=False)]
        
        if filtered.empty:
            raise ValueError(f"No hay países en la región '{region}'")
        
        # Simular datos temporales (ej.: crecimiento anual)
        years = [2015, 2016, 2017, 2018, 2019, 2020]
        line_data = []
        for _, row in filtered.iterrows():
            growth_rate = 0.01  # Tasa de crecimiento simulada
            country_data = [{"Año": year, "País": row["Nombre"], metric: int(row[metric] * (1 + growth_rate) ** (year - 2015))} for year in years]
            line_data.extend(country_data)
        
        df_line = pd.DataFrame(line_data)
        
        # Generar gráfico de líneas
        fig = px.line(
            df_line,
            x="Año",
            y=metric,
            color="País",
            title=f"Tendencia de {metric} en {region}",
            labels={"Año": "Año", metric: metric.capitalize()}
        )
        return fig
    except Exception as e:
        print(f"Error al generar el gráfico de líneas: {e}")
        return px.line(title="Error al cargar el gráfico")

def generate_pie_chart(data: List[Dict[str, Any]], metric: str = "Población") -> px.pie:
    """
    Genera un gráfico de torta (pie) con la proporción de una métrica por región.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        metric (str): Métrica a analizar (ej.: "Población").
        
    Returns:
        px.pie: Gráfico de torta interactivo.
    """
    try:
        # Agrupar datos por región
        df = pd.DataFrame(data)
        region_stats = df.groupby("Región")[metric].sum().reset_index()
        
        # Generar gráfico de torta
        fig = px.pie(
            region_stats,
            values=metric,
            names="Región",
            title=f"Distribución Mundial por {metric.capitalize()}",
            labels={"Región": "Región", metric: metric.capitalize()}
        )
        return fig
    except Exception as e:
        print(f"Error al generar el gráfico de torta: {e}")
        return px.pie(title="Error al cargar el gráfico")

def generate_scatter_chart(data: List[Dict[str, Any]], x_metric: str = "Área(km²)", y_metric: str = "Población") -> px.scatter:
    """
    Genera un gráfico de dispersión entre dos métricas.
    
    Args:
        data (List[Dict]): Lista de diccionarios con datos de países.
        x_metric (str): Métrica para el eje X.
        y_metric (str): Métrica para el eje Y.
        
    Returns:
        px.scatter: Gráfico de dispersión interactivo.
    """
    try:
        # Convertir datos a DataFrame
        df = pd.DataFrame(data)
        
        # Validar métricas
        for metric in [x_metric, y_metric]:
            if metric not in df.columns:
                raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar gráfico de dispersión
        fig = px.scatter(
            df,
            x=x_metric,
            y=y_metric,
            hover_name="Nombre",
            title=f"Relación entre {x_metric} y {y_metric}",
            labels={x_metric: x_metric.capitalize(), y_metric: y_metric.capitalize()}
        )
        return fig
    except Exception as e:
        print(f"Error al generar el gráfico de dispersión: {e}")
        return px.scatter(title="Error al cargar el gráfico")