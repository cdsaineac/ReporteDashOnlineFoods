import pandas as pd 
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

## 1. Cargar el DataFrame
df = pd.read_csv('onlinefoods.csv')

## 2. Transformación de datos (Si es necesario)

## 3. Crear la aplicación Dash
external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Reporte de pedidos de comida online"

### 4. Definir el layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([html.H1("Reporte de pedidos de comida online")]),
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona el género:"),
            dcc.Dropdown(
            id='selector_genero',
            options=[{'label': genero, 'value': genero} for genero in df['Gender'].unique()],
            value=df['Gender'].unique()[0]  # Valor por defecto
            )
        ], width=3),
        dbc.Col([
            html.Label("Selecciona la ocupación:"),
            dcc.RadioItems(
            id='selector_ocupacion',
            options=[{'label': ocupacion, 'value': ocupacion} for ocupacion in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0]  # Valor por defecto
        )], width=3),
        dbc.Col([
            html.Label("Selecciona el rango de edad:"),
            dcc.RangeSlider(
            id='selector_edad',
            min=df['Age'].min(),
            max=df['Age'].max(),
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(df['Age'].min(), df['Age'].max() + 1)},
            step=1
        )], width=6)
        ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafica_barras')
        ]),
        dbc.Col([
            dcc.Graph(id='grafica_torta')
        ])        
    ])
], fluid=True)
### 5. Definir los callbacks (Si es necesario)  
@app.callback(
    [Output('grafica_barras', 'figure'),
     Output('grafica_torta', 'figure')],
    [Input('selector_ocupacion', 'value'),
     Input('selector_genero', 'value'),
     Input('selector_edad', 'value')]  
)

def crear_graficas(valor_ocupacion, valor_genero, valor_edad):
    # Filtrar el DataFrame según el género seleccionado
    df_filtrado = df[(df['Gender'] == valor_genero) & (df['Occupation'] == valor_ocupacion) & (df['Age'] >= valor_edad[0]) & (df['Age'] <= valor_edad[1])]
    conteo_feedback_estado_civil = df_filtrado.groupby(['Marital Status','Feedback'])['Age'].count().reset_index().sort_values(by='Feedback', ascending=False)

    grafica_barras = px.bar(conteo_feedback_estado_civil,
                            x='Marital Status',
                            y='Age',
                            color = 'Feedback',
                            title='Promedio del tamaño de la familia por estado civil',
                            color_discrete_sequence=['#65c78c', '#f74a50'])
    
    conteo_votos_feedback = df_filtrado.groupby(['Feedback'])['Age'].count().reset_index().sort_values(by='Feedback', ascending=False)
    grafica_torta = px.pie(conteo_votos_feedback,
                            names='Feedback',
                            values='Age',
                            title='Distribución del tamaño de la familia por estado civil',
                            color_discrete_sequence=['#65c78c', '#f74a50'])

    return grafica_barras, grafica_torta







