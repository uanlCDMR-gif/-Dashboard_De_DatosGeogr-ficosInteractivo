# main_layout.py - Diseño principal del dashboard con Plotly Dash

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def generate_main_layout(app):
    """
    Genera el diseño principal del dashboard utilizando componentes de Dash y Bootstrap.
    Args:
        app: Instancia de la aplicación Dash.
    Returns:
        html.Div: Estructura del layout principal.
    """
    # Datos simulados para el mapa (requiere token de Mapbox)
    country_data = pd.DataFrame({
        "name": ["Colombia", "Brazil", "France", "India", "China"],
        "density": [44.56, 25.5, 120.0, 464.0, 153.0],
        "iso3": ["COL", "BRA", "FRA", "IND", "CHN"]
    })

    # Crear mapa de calor (choropleth)
    fig_map = px.choropleth(
        country_data,
        locations="iso3",
        locationmode="country names",
        color="density",
        hover_name="name",
        color_continuous_scale="Viridis",
        title="Densidad Poblacional por País"
    )

    # Datos simulados para el gráfico de barras (top 10 países)
    bar_data = pd.DataFrame({
        "name": ["China", "India", "EE.UU.", "Indonesia", "Pakistán", 
                 "Brasil", "Nigeria", "Bangladesh", "Rusia", "México"],
        "population": [1402112000, 1380004385, 331002651, 273523615, 
                       220752339, 212559417, 206139589, 164689383, 
                       145934462, 128932753]
    })

    # Crear gráfico de barras inicial (top 10 países por población)
    fig_bar = px.bar(
        bar_data, 
        x="name", 
        y="population", 
        title="Top 10 Países por Población",
        labels={"name": "País", "population": "Población"}
    )

    # Definir el layout principal del dashboard
    layout = html.Div([
        # Título del dashboard
        dbc.Row([
            dbc.Col([
                html.H1("Dashboard Geográfico Interactivo", className="text-center text-primary mb-4")
            ], width=12)
        ]),

        # Sección de navegación y filtros
        dbc.Row([
            dbc.Col([
                html.Label("Seleccionar Métrica:", className="font-weight-bold"),
                dcc.Dropdown(
                    id="metric-dropdown",
                    options=[
                        {"label": "Población", "value": "population"},
                        {"label": "Área (km²)", "value": "area"},
                        {"label": "Densidad (hab/km²)", "value": "density"}
                    ],
                    value="population",
                    clearable=False
                )
            ], width=4, className="mb-4"),
        ], justify="center"),

        # Sección de gráficos
        dbc.Row([
            # Mapa de calor
            dbc.Col([
                html.H4("Mapa de Calor de Densidad Poblacional", className="text-center"),
                dcc.Graph(
                    id="choropleth-map",
                    figure=fig_map,
                    config={"displayModeBar": False}
                )
            ], width=12, lg=6, className="mb-4"),

            # Gráfico de barras dinámico
            dbc.Col([
                html.H4("Top 10 Países por Métrica", className="text-center"),
                dcc.Graph(
                    id="bar-chart",
                    figure=fig_bar,
                    config={"displayModeBar": False}
                )
            ], width=12, lg=6, className="mb-4"),
        ]),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Footer("Datos geográficos y demográficos proporcionados por REST Countries", 
                            className="text-center text-muted mt-4")
            ], width=12)
        ])
    ], style={"padding": "20px"})

    return layout