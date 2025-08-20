import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import os

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Análisis de Uso de Suelo: Impacto Ambiental de los Alimentos"

# Expose server for deployment
server = app.server

# Load and prepare data
def load_and_prepare_data():
    """Load and prepare the land usage dataset"""
    # Get the directory of this script for relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "land-use-kcal-poore.csv")
    
    df_land = pd.read_csv(data_path)
    df_land.rename(columns={'Land use per 1000kcal (Poore & Nemecek, 2018)': 'use'}, inplace=True)
    
    # Create a copy with categories for the treemap
    df_land_categories = df_land.copy()
    df_land_categories['Category'] = 'Other'
    
    # Define food categories
    food_categories = {
        'Meat': ['Beef (beef herd)', 'Beef (dairy herd)', 'Lamb & Mutton', 'Pig Meat', 'Poultry Meat'],
        'Dairy': ['Milk', 'Cheese', 'Eggs'],
        'Fruits': ['Apples', 'Bananas', 'Berries & Grapes', 'Citrus Fruit'],
        'Vegetables': ['Brassicas', 'Tomatoes', 'Potatoes', 'Onions & Leeks', 'Root Vegetables', 'Cassava'],
        'Grains': ['Barley', 'Maize', 'Rice', 'Wheat & Rye', 'Oatmeal'],
        'Legumes': ['Peas', 'Other Pulses', 'Groundnuts', 'Tofu (soybeans)'],
        'Oils': ['Palm Oil', 'Olive Oil', 'Rapeseed Oil', 'Sunflower Oil'],
        'Sweets': ['Dark Chocolate', 'Beet Sugar', 'Cane Sugar'],
        'Seafood': ['Fish (farmed)', 'Prawns (farmed)'],
        'Other': ['Coffee', 'Nuts']
    }
    
    # Assign categories
    for category, foods in food_categories.items():
        df_land_categories.loc[df_land_categories['Entity'].isin(foods), 'Category'] = category
    
    return df_land, df_land_categories, food_categories

# Load data
df_land, df_land_categories, food_categories = load_and_prepare_data()

def create_horizontal_bar_chart(df_land, log_scale=False):
    """Create horizontal bar chart with optional log scale"""
    df_sorted = df_land.sort_values('use', ascending=True)
    
    title = 'Uso de Suelo por 1000kcal por Tipo de Alimento'
    if log_scale:
        title += ' (Escala Logarítmica)'
    
    fig = px.bar(df_sorted, 
                 x='use', 
                 y='Entity',
                 orientation='h',
                 title=title,
                 labels={'use': 'Uso de Suelo (m²/1000kcal)', 'Entity': 'Tipo de Alimento'},
                 color='use',
                 color_continuous_scale='RdYlGn_r',
                 height=800)
    
    if log_scale:
        fig.update_xaxes(type="log")
        fig.update_layout(xaxis_title='Uso de Suelo (m²/1000kcal) - Escala Log')
    
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        height=900,
        width=None,  # Use full available width
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=200, r=50, t=80, b=50),
        autosize=True
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black'
    )
    
    fig.update_yaxes(
        showgrid=False,
        linecolor='black'
    )
    
    return fig

def create_treemap(df_land_categories):
    """Create treemap visualization"""
    # Sort the data by 'use' column in descending order for treemap squares arrangement
    df_sorted = df_land_categories.sort_values('use', ascending=False)
    
    fig_treemap = px.treemap(
        df_sorted, 
        path=['Category', 'Entity'], 
        values='use',
        color='use',
        color_continuous_scale='RdYlGn_r',
        title='Intensidad de Uso de Suelo por Categoría y Tipo de Alimento'
    )
    
    # Improve label visibility with enhanced text settings
    fig_treemap.update_traces(
        root_color='white',
        tiling=dict(pad=2),
        textfont=dict(
            size=12,
            color='black',
            family='Arial, sans-serif'
        ),
        textposition='middle center',
        texttemplate='%{label}<br>%{value:.1f} m²',
        marker=dict(line=dict(width=1.5, color='white')),
        textinfo='label+value'
    )
    
    # Enhance layout for better visibility
    fig_treemap.update_layout(
        height=900,
        width=None,  # Use full available width
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='black', size=12),
        title=dict(
            font=dict(size=18),
            x=0.5,
            y=0.98
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        autosize=True
    )
    
    # Configure text fonts for better visibility
    fig_treemap.update_traces(
        insidetextfont=dict(
            size=11,
            color='black',
            family='Arial Black, sans-serif'
        ),
        outsidetextfont=dict(
            size=13,
            color='black',
            family='Arial Black, sans-serif'
        ),
        textposition='middle center'
    )
    
    return fig_treemap

def create_summary_statistics():
    """Create summary statistics table"""
    stats = df_land['use'].describe().round(2)
    
    # Create a DataFrame for the table
    stats_df = pd.DataFrame({
        'Estadística': ['Promedio', 'Desviación Estd.', 'Mínimo', '25%', 'Mediana', '75%', 'Máximo'],
        'Valor (m²/1000kcal)': [
            stats['mean'], stats['std'], stats['min'], 
            stats['25%'], stats['50%'], stats['75%'], stats['max']
        ]
    })
    
    return stats_df

# Create all visualizations
horizontal_bar = create_horizontal_bar_chart(df_land, log_scale=False)
horizontal_bar_log = create_horizontal_bar_chart(df_land, log_scale=True)
treemap = create_treemap(df_land_categories)
stats_df = create_summary_statistics()

# Define app layout
app.layout = html.Div([
    html.Div([
        html.H1("🌱 Análisis de Uso de Suelo: Impacto Ambiental de los Alimentos", 
                style={'textAlign': 'center', 'marginBottom': 30, 'color': '#2E7D32'}),
        
        html.P([
            "Este dashboard interactivo analiza el uso del suelo que se requiere para producir diferentes tipos de alimentos. ",
            "Los datos están expresados en metros cuadrados para producir 1000 kilocalorías de cada alimento."
        ], style={'textAlign': 'center', 'marginBottom': 40, 'fontSize': 16, 'color': '#666', 
                 'maxWidth': '800px', 'margin': '0 auto 40px auto'}),
        
        # Summary statistics card
        html.Div([
            html.H3("📊 Estadísticas Generales", style={'color': '#2E7D32', 'marginBottom': 20}),
            html.Div([
                html.Div([
                    html.H4(f"{stats_df.iloc[0, 1]:.1f}", style={'color': '#1976D2', 'margin': 0}),
                    html.P("Promedio (m²/1000kcal)", style={'margin': '5px 0', 'fontSize': 14})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '15px', 
                                               'backgroundColor': '#E3F2FD', 'borderRadius': '8px', 
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{stats_df.iloc[4, 1]:.1f}", style={'color': '#388E3C', 'margin': 0}),
                    html.P("Mediana (m²/1000kcal)", style={'margin': '5px 0', 'fontSize': 14})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '15px', 
                                               'backgroundColor': '#E8F5E8', 'borderRadius': '8px', 
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{stats_df.iloc[6, 1]:.1f}", style={'color': '#D32F2F', 'margin': 0}),
                    html.P("Máximo (m²/1000kcal)", style={'margin': '5px 0', 'fontSize': 14})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '15px', 
                                               'backgroundColor': '#FFEBEE', 'borderRadius': '8px', 
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{len(df_land)}", style={'color': '#7B1FA2', 'margin': 0}),
                    html.P("Tipos de Alimentos", style={'margin': '5px 0', 'fontSize': 14})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '15px', 
                                               'backgroundColor': '#F3E5F5', 'borderRadius': '8px', 
                                               'margin': '10px', 'flex': '1'})
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around', 'marginBottom': 30, 'gap': '10px'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '12px', 'marginBottom': 30, 'width': '100%'}),
        
        # Tab system for different charts
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='📊 Gráfico de Barras', value='tab-1', style={'fontSize': 16}),
            dcc.Tab(label='🗺️ Mapa de Árbol', value='tab-2', style={'fontSize': 16}),
        ], style={'marginBottom': 30}),
        
        html.Div(id='tabs-content')
        
    ], style={'maxWidth': '95%', 'width': '100%', 'margin': '0 auto', 'padding': '10px'})
])

@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'))
def render_content(active_tab):
    if active_tab == 'tab-1':
        return html.Div([
            html.H2("📊 Gráfico de Barras", 
                    style={'textAlign': 'center', 'marginBottom': 20, 'color': '#2E7D32'}),
            
            html.P([
                "Este gráfico muestra todos los alimentos ordenados por su utilización de suelo. ",
                "Los colores van del verde (menor impacto) al rojo (mayor impacto). ",
                "Se puede cambiar entre escala normal y logarítmica usando el botón de abajo."
            ], style={'textAlign': 'center', 'marginBottom': 20, 'fontSize': 14, 'color': '#666'}),
            
            # Only show the bar chart (no scale toggle)
            html.Div([
                dcc.Graph(
                    figure=horizontal_bar,
                    style={'height': '950px', 'width': '100%'},
                    config={'displayModeBar': True, 'responsive': True}
                )
            ], style={'width': '100%', 'margin': '0 auto'}),
            
            html.Div([
                html.H3("🔍 Puntos Clave:", style={'color': '#2E7D32', 'marginBottom': 10}),
                html.Ul([
                    html.Li("La carne de res requiere significativamente más suelo que otros alimentos."),
                    html.Li("Los productos animales generalmente requieren más suelo que los vegetales."),
                    html.Li("Las legumbres y granos tienen un impacto relativamente bajo en el uso del suelo.")
                ], style={'fontSize': 14, 'color': '#666'})
            ], style={'marginTop': 30, 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px'})
        ])
    
    elif active_tab == 'tab-2':
        return html.Div([
            html.H2("🌲 Treemap", 
                    style={'textAlign': 'center', 'marginBottom': 20, 'color': '#2E7D32'}),
            
            html.P([
                "Este gráfico organiza los alimentos en categorías y el uso del suelo de cada uno. El tamaño de cada rectángulo es proporcional al uso de suelo, ",
                "y el color indica la intensidad (verde = menor impacto, rojo = mayor impacto)."
            ], style={'textAlign': 'center', 'marginBottom': 30, 'fontSize': 14, 'color': '#666'}),
            
            html.Div([
                dcc.Graph(
                    figure=treemap,
                    style={'height': '950px', 'width': '100%'},
                    config={'displayModeBar': True, 'responsive': True}
                )
            ], style={'width': '100%', 'margin': '0 auto'}),
            
            html.Div([
                html.H3("🎯 Interpretación:", style={'color': '#2E7D32', 'marginBottom': 10}),
                html.Ul([
                    html.Li("Los rectángulos más grandes representan mayor uso de suelo por 1000kcal."),
                    html.Li("La categoría 'Meat' (Carnes) domina visualmente el espacio disponible."),
                    html.Li("Las categorías 'Grains' (Granos) y 'Legumes' (Legumbres) ocupan espacios pequeños."),
                    html.Li("Dentro de cada categoría se puede comparar fácilmente el impacto relativo.")
                ], style={'fontSize': 14, 'color': '#666'})
            ], style={'marginTop': 30, 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px'})
        ])

    # Removed callback for scale toggle and dynamic bar chart

# Run the app
if __name__ == '__main__':
    # For development
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8051)))
