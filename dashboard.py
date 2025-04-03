
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Cargar el archivo CSV combinado
file_path = r'G:\Mi unidad\SUPERMERCADOS\preciossupermercados_combined.csv'
df = pd.read_csv(file_path)

# Convertir 'FechaConsulta' a tipo datetime
df['FechaConsulta'] = pd.to_datetime(df['FechaConsulta'])

# Convertir 'Precio' a string, aplicar reemplazo de caracteres no numéricos y luego convertir a numérico
df['Precio'] = df['Precio'].astype(str).str.replace(r'[^\d,]', '', regex=True).str.replace(',', '.')
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

# Filtrar datos no válidos si fuese necesario
df = df.dropna(subset=['Precio', 'FechaConsulta'])

# Obtener listas únicas para los desplegables
categorias = df['Categoria_Nueva'].unique()
productos = df['Producto'].unique()
supermercados = df['Supermercado'].unique()

# Inicializar la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Variación de Precios de Productos"),

    html.Div([
        html.Label("Seleccionar Categoría:"),
        dcc.Dropdown(
            id='categoria-dropdown',
            options=[{'label': 'Todos', 'value': 'all'}] +
                    [{'label': cat, 'value': cat} for cat in categorias],
            value='all',  # Seleccionar "Todos" por defecto
            multi=False
        ),
    ]),

    html.Div([
        html.Label("Seleccionar Producto:"),
        dcc.Dropdown(
            id='producto-dropdown',
            options=[{'label': 'Todos', 'value': 'all'}] +
                    [{'label': prod, 'value': prod} for prod in productos],
            value='all',  # Seleccionar "Todos" por defecto
            multi=False
        ),
    ]),

    html.Div([
        html.Label("Seleccionar Supermercado:"),
        dcc.Dropdown(
            id='supermercado-dropdown',
            options=[{'label': 'Todos', 'value': 'all'}] +
                    [{'label': super, 'value': super} for super in supermercados],
            value='all',  # Seleccionar "Todos" por defecto
            multi=False
        ),
    ]),

    dcc.Graph(id='price-variation-graph')
])

@app.callback(
    Output('price-variation-graph', 'figure'),
    Input('categoria-dropdown', 'value'),
    Input('producto-dropdown', 'value'),
    Input('supermercado-dropdown', 'value')
)
def update_graph(selected_category, selected_product, selected_supermarket):
    # Filtrar el DataFrame según las selecciones
    filtered_df = df.copy()
    
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['Categoria_Nueva'] == selected_category]
    
    if selected_product != 'all':
        filtered_df = filtered_df[filtered_df['Producto'] == selected_product]
    
    if selected_supermarket != 'all':
        filtered_df = filtered_df[filtered_df['Supermercado'] == selected_supermarket]

    # Crear la figura
    fig = go.Figure()

    for prod in filtered_df['Producto'].unique():
        prod_df = filtered_df[filtered_df['Producto'] == prod].sort_values('FechaConsulta')
        fig.add_trace(
            go.Scatter(
                x=prod_df['FechaConsulta'],
                y=prod_df['Precio'],
                mode='lines+markers',
                name=prod
            )
        )

    fig.update_layout(
        title="Variación de Precios",
        xaxis_title="Fecha de Consulta",
        yaxis_title="Precio (Gs)",
        hovermode="x unified",
        template="plotly_dark",
        legend_title="Producto",
        margin=dict(l=50, r=50, t=100, b=50)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
