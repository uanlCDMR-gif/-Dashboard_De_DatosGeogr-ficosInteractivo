# app.py - Configuración principal del dashboard con Plotly Dash

import dash
from dash import html, dcc, Input, Output
import requests
import pandas as pd
from main_layout import generate_main_layout
from graphs import (
    generate_choropleth_map,
    generate_bar_chart,
    generate_pie_chart,
    generate_scatter_chart
)

# Inicializar la aplicación Dash con Bootstrap
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap @5.3.0/dist/css/bootstrap.min.css"])
server = app.server  # Requerido para despliegue en servidores como Heroku o Render

# Datos simulados para pruebas (en producción, se obtienen del backend)
countries_data = [
    {"Nombre": "China", "Población": 1402112000, "Área(km²)": 9596961, "Densidad(hab/km²)": 146.1, "Región": "Asia"},
    {"Nombre": "India", "Población": 1380004385, "Área(km²)": 3287590, "Densidad(hab/km²)": 419.7, "Región": "Asia"},
    {"Nombre": "EE.UU.", "Población": 331002651, "Área(km²)": 9833520, "Densidad(hab/km²)": 34.7, "Región": "Americas"},
    {"Nombre": "Indonesia", "Población": 273523615, "Área(km²)": 1904569, "Densidad(hab/km²)": 143.6, "Región": "Asia"},
    {"Nombre": "Pakistán", "Población": 220752339, "Área(km²)": 881912, "Densidad(hab/km²)": 250.3, "Región": "Asia"},
    {"Nombre": "Brasil", "Población": 212559417, "Área(km²)": 8515767, "Densidad(hab/km²)": 24.9, "Región": "Americas"},
    {"Nombre": "Nigeria", "Población": 206139589, "Área(km²)": 923768, "Densidad(hab/km²)": 223.1, "Región": "Africa"},
    {"Nombre": "Bangladesh", "Población": 164689383, "Área(km²)": 147570, "Densidad(hb/km²)": 1116.0, "Región": "Asia"},
    {"Nombre": "Rusia", "Población": 145934462, "Área(km²)": 17098242, "Densidad(hab/km²)": 8.5, "Región": "Europe"},
    {"Nombre": "México", "Población": 128932753, "Área(km²)": 1964375, "Densidad(hab/km²)": 65.6, "Región": "Americas"},
    {"Nombre": "Colombia", "Población": 50882891, "Área(km²)": 1141748, "Densidad(hab/km²)": 44.56, "Región": "Americas"},
    {"Nombre": "Argentina", "Población": 45376763, "Área(km²)": 2780400, "Densidad(hab/km²)": 16.3, "Región": "Americas"},
    {"Nombre": "Kenia", "Población": 53771296, "Área(km²)": 580367, "Densidad(hab/km²)": 92.7, "Región": "Africa"},
    {"Nombre": "Francia", "Población": 67902648, "Área(km²)": 551695, "Densidad(hab/km²)": 123.0, "Región": "Europe"},
    {"Nombre": "Japón", "Población": 125847423, "Área(km²)": 377975, "Densidad(hab/km²)": 333.0, "Región": "Asia"}
]

# Cargar el layout principal
app.layout = generate_main_layout(app)

# Callback para actualizar el mapa de calor
@app.callback(
    Output("choropleth-map", "figure"),
    Input("metric-dropdown", "value")
)
def update_choropleth(metric):
    """
    Actualiza el mapa de calor según la métrica seleccionada.
    Args:
        metric (str): Métrica a visualizar (ej.: "Población", "Densidad").
    Returns:
        plotly.graph_objects.Figure: Mapa actualizado.
    """
    try:
        # Convertir a DataFrame
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista en los datos
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar mapa de calor
        return generate_choropleth_map(df.to_dict(orient="records"), metric)
    except Exception as e:
        print(f"Error al actualizar el mapa de calor: {e}")
        return generate_choropleth_map([], "Población")  # Devolver un mapa vacío en caso de error

# Callback para actualizar el gráfico de barras
@app.callback(
    Output("bar-chart", "figure"),
    Input("metric-dropdown", "value")
)
def update_bar_chart(metric):
    """
    Actualiza el gráfico de barras según la métrica seleccionada.
    Args:
        metric (str): Métrica a visualizar (ej.: "Población", "Área").
    Returns:
        plotly.graph_objects.Figure: Gráfico de barras actualizado.
    """
    try:
        # Simular llamada al backend (en producción, usar requests.get())
        # Ejemplo: response = requests.get(f"https://api-url/api/v1/top-10/{metric}")
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar gráfico de barras
        return generate_bar_chart(df.to_dict(orient="records"), metric, top_n=10)
    except Exception as e:
        print(f"Error al actualizar el gráfico de barras: {e}")
        return generate_bar_chart([], "Población")  # Devolver gráfico vacío en caso de error

# Callback para actualizar el gráfico de torta (pie chart)
@app.callback(
    Output("pie-chart", "figure"),
    Input("metric-dropdown", "value")
)
def update_pie_chart(metric):
    """
    Actualiza el gráfico de torta según la métrica seleccionada.
    Args:
        metric (str): Métrica a visualizar (ej.: "Población").
    Returns:
        plotly.graph_objects.Figure: Gráfico de torta actualizado.
    """
    try:
        # Simular llamada al backend
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar gráfico de torta
        return generate_pie_chart(df.to_dict(orient="records"), metric)
    except Exception as e:
        print(f"Error al actualizar el gráfico de torta: {e}")
        return generate_pie_chart([], "Población")  # Devolver gráfico vacío en caso de error

# Callback para actualizar el gráfico de dispersión
@app.callback(
    Output("scatter-chart", "figure"),
    Input("metric-dropdown", "value")
)
def update_scatter_chart(metric):
    """
    Actualiza el gráfico de dispersión entre dos métricas.
    Args:
        metric (str): Métrica para el eje Y (el eje X es fijo como "Área(km²)").
    Returns:
        plotly.graph_objects.Figure: Gráfico de dispersión actualizado.
    """
    try:
        # Simular llamada al backend
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar gráfico de dispersión (Área vs. Métrica seleccionada)
        return generate_scatter_chart(df.to_dict(orient="records"), x_metric="Área(km²)", y_metric=metric)
    except Exception as e:
        print(f"Error al actualizar el gráfico de dispersión: {e}")
        return generate_scatter_chart([], "Área(km²)", "Población")  # Devolver gráfico vacío en caso de error

# Callback para actualizar el gráfico de líneas
@app.callback(
    Output("line-chart", "figure"),
    Input("metric-dropdown", "value")
)
def update_line_chart(metric):
    """
    Actualiza el gráfico de líneas con tendencias históricas de una métrica por región.
    Args:
        metric (str): Métrica a analizar (ej.: "Población").
    Returns:
        plotly.graph_objects.Figure: Gráfico de líneas actualizado.
    """
    try:
        # Simular llamada al backend
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Generar gráfico de líneas (simulado para Europa)
        return generate_line_chart(df.to_dict(orient="records"), metric, region="Asia")
    except Exception as e:
        print(f"Error al actualizar el gráfico de líneas: {e}")
        return generate_line_chart([], "Población", "Asia")  # Devolver gráfico vacío en caso de error

# Callback para actualizar la tabla de datos
@app.callback(
    Output("data-table", "children"),
    Input("metric-dropdown", "value")
)
def update_data_table(metric):
    """
    Actualiza la tabla de datos según la métrica seleccionada.
    Args:
        metric (str): Métrica a mostrar (ej.: "Población").
    Returns:
        dash.html.Table: Tabla actualizada.
    """
    try:
        # Simular llamada al backend
        df = pd.DataFrame(countries_data)
        
        # Validar que la métrica exista
        if metric not in df.columns:
            raise ValueError(f"Métrica '{metric}' no encontrada en los datos")
        
        # Ordenar por métrica y devolver tabla
        df_sorted = df.sort_values(by=metric, ascending=False).head(10)
        return generate_data_table(df_sorted)
    except Exception as e:
        print(f"Error al actualizar la tabla de datos: {e}")
        return html.Div("Error al cargar la tabla", className="alert alert-danger")

def generate_data_table(df):
    """
    Genera una tabla HTML a partir de un DataFrame.
    Args:
        df (pd.DataFrame): DataFrame con datos procesados de países.
    Returns:
        dash.html.Table: Tabla HTML para Dash.
    """
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)