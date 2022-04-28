#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_table
import base64
import pandas as pd
import numpy as np
from file_handle import File_Handle
from SIR_model import SIR
from SIR_predict import SirPredict
from utilities.utilities import Utilities 
import matplotlib.pyplot as plt

#%%
#Instances
handle = File_Handle()
sirmodel = SIR()
sirpredict = SirPredict()
utl = Utilities()
fig = go.Figure()

#%%
#Downloading data
# handle.download_censo_file()
file_status = 'sucess'#handle.download_covid_file()

#%%
#Loading data
censo_df = pd.read_excel('data/ProyeccionMunicipios2005_2020.xls', sheet_name = 'Mpios',header=8)

censo_df['MPIO'] = np.where(censo_df['MPIO'] == 'Bogotá, D.C.', 'Bogotá D.C.', censo_df['MPIO'])
censo_df['MPIO'] = np.where(censo_df['MPIO'] == 'Cartagena', 'Cartagena de Indias', censo_df['MPIO'])

data_org = pd.read_csv('data/Casos_positivos_de_COVID-19_en_Colombia.csv')

#%%
#Execution
#------------------------------------------------------------------
data = pd.DataFrame()
cities = ["Medellín"]
data = data_org[data_org["Ciudad de ubicación"].isin(cities)]
data = utl.dates_fix(data)
data = utl.build_counters(data)
data = utl.clean_dataset(data)
cities = utl.get_cities(data)
dates = utl.get_dates(data)
mv_med = utl.build_mineable_view(data, cities, dates)

tasas_med = sirmodel.sir_tasas_init(mv_med)
sir_formulas_med = sirmodel.sir_tasas(tasas_med, censo_df)
original_med, predict_med = sirpredict.predict(sir_formulas_med,censo_df)

#------------------------------------------------------------------
data = pd.DataFrame()
cities = ["Bogotá D.C."]
data = data_org[data_org["Ciudad de ubicación"].isin(cities)]
data = utl.dates_fix(data)
data = utl.build_counters(data)
data = utl.clean_dataset(data)
cities = utl.get_cities(data)
dates = utl.get_dates(data)
mv_bog = utl.build_mineable_view(data, cities, dates)

tasas_bog = sirmodel.sir_tasas_init(mv_bog)
sir_formulas_bog = sirmodel.sir_tasas(tasas_bog, censo_df)
original_bog, predict_bog = sirpredict.predict(sir_formulas_bog,censo_df)

#------------------------------------------------------------------
data = pd.DataFrame()
cities = ["Cali"]
data = data_org[data_org["Ciudad de ubicación"].isin(cities)]
data = utl.dates_fix(data)
data = utl.build_counters(data)
data = utl.clean_dataset(data)
cities = utl.get_cities(data)
dates = utl.get_dates(data)
mv_cali = utl.build_mineable_view(data, cities, dates)

tasas_cali = sirmodel.sir_tasas_init(mv_cali)
sir_formulas_cali = sirmodel.sir_tasas(tasas_cali, censo_df)
original_cali, predict_cali = sirpredict.predict(sir_formulas_cali,censo_df)

#------------------------------------------------------------------
data = pd.DataFrame()
cities = ["Barranquilla"]
data =data_org[data_org["Ciudad de ubicación"].isin(cities)]
data = utl.dates_fix(data)
data = utl.build_counters(data)
data = utl.clean_dataset(data)
cities = utl.get_cities(data)
dates = utl.get_dates(data)
mv_bar = utl.build_mineable_view(data, cities, dates)

tasas_bar = sirmodel.sir_tasas_init(mv_bar)
sir_formulas_bar = sirmodel.sir_tasas(tasas_bar, censo_df)
original_bar, predict_bar = sirpredict.predict(sir_formulas_bar,censo_df)

#------------------------------------------------------------------
data = pd.DataFrame()
cities = ["Cartagena de Indias"]
data = data_org[data_org["Ciudad de ubicación"].isin(cities)]
data = utl.dates_fix(data)
data = utl.build_counters(data)
data = utl.clean_dataset(data)
cities = utl.get_cities(data)
dates = utl.get_dates(data)
mv_car = utl.build_mineable_view(data, cities, dates)

tasas_car = sirmodel.sir_tasas_init(mv_car)
sir_formulas_car = sirmodel.sir_tasas(tasas_car, censo_df)
original_car, predict_car = sirpredict.predict(sir_formulas_car,censo_df)

# ------------------------------------------------------------------
#%%
originales_list = [original_car,original_bar,original_cali,original_bog,original_med]
predichos_list = [predict_car,predict_bar,predict_cali,predict_bog,predict_med]

originales = pd.concat(originales_list)
predichos = pd.concat(predichos_list)

corto_plazo = predichos.head(5)
corto_plazo = corto_plazo['t'].tail(1)
mediano_plano = predichos.iloc[5:15]
mediano_plano = mediano_plano['t'].tail(1)
largo_plazo = predichos.tail(20)
largo_plazo = largo_plazo['t'].tail(1)
 


#%%
#Visualization

last_update = data['fecha reporte web'].max()
las_t = originales['t'].max()

tabtitle = 'Covid-19'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets) 
server = app.server
app.title=tabtitle

app.layout = html.Div(children=[
    
    html.Div([
        html.Div([
            html.Img(id='logo',
                    src='data:image/png;base64,{}'.format(base64.b64encode(open('img/logo.png', 'rb')\
                        .read()).decode()),
                    style={"height": '60%', "width": '60%', "margin-bottom": "25px"}
                    )],className="one-third column",),
        html.Div([
            html.Div([
            html.H1(children='Covid-19 en Colombia - Predicción',
            style = { "margin-bottom": "0px", 'font-size': '50px' }
            ,),
            html.Label(['Comportamiento del coronavirus en las principales ciudades de Colombia.\
            Información obtenida de la página web ', html.A('https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data', href='https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr/data')
            ,' recopilada por el Instituto Nacional de Salud'],
            style ={
                'font-size': '15px', 'text-align': 'justify'
            }),
            html.Label(['Fecha de última carga, ', last_update]),
            html.Label(['Número de días correspondiente a la fecha de última carga (t), ', las_t])
            ])],id='title')    
        ],id = 'header'),

    # dash_table.DataTable(
    #         id = 'table',
    #         columns = [{'name':i, 'id':i} for i in originales.columns],
    #         data=originales.to_dict('records')
    #     ),

    html.A(html.Button('Recarga de información'),href='/',style={
        'margin-left': '0px',
        }),

    html.Div([
        html.Div([
            html.P('Seleccione las ciudades a analizar: ',style={'font-weight': 'bold'}),
        dcc.RadioItems(
            id='ciudades_checklist',
            options = [{'label': str(city), 'value': str(city)} for city in originales['Ciudad de ubicación'].unique()],
            value = 'Medellín')],
            style = {
            'width': '300px',#'calc(100%-40px)',
            'border-radius': '5px',
            'background-color': '#FFFFFF',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
            })
            # labelStyle={'display': 'inline-block'}    
        ],id='filter'),

    dcc.Graph(
        id='g0',
        style = {
        'width': 'calc(100%-40px)',
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'}
    ),

    html.Div([
        html.Div([dcc.Graph(id='g1')],
        style = {
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'},        
        className="six columns"),

        html.Div([
            dcc.Graph(id='g2')
        ], 
        style = {
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'},
        className="six columns"),

        html.Div([
            dcc.Graph(id='g3')
        ], 
        style = {
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'},
        className="six columns"),

        html.Div([
            dcc.Graph(id='g4')
        ], 
        style = {
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'},
        className="six columns"),

        html.Div([
            dcc.Graph(id='g5')
        ], 
        style = {
        'border-radius': '5px',
        'background-color': '#FFFFFF',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'},
        className="six columns"),

        # html.Div([
        # dcc.Graph(id='g6', figure={'data': 
        #         [
        #             go.Scatter(

        #         x = plazos.iloc[i]['t'],
        #         y = plazos.iloc[i]['activo'],
        #         mode = "lines",
        #         # name = rowname
        #         )for i in plazos.index
        # ]
        # })]), 
        

    ], style = {
        'width': '100%',
        'border-radius': '5px',
        'padding': '15px',
        
        }, className="row"),

    html.Div([
        html.Div([
            html.P('Elaborado por:'),    
        
            html.Ul(children=[
            html.Li('Arboleda Santiago', style={'float':'left'}), 
            html.Li('Montoya Olga Lucía', style={'float':'left'}),
            html.Li('Ramirez Alberto'  , style={'float':'left'}),
            html.Li('Tangarife Juan David', style={'float':'left'})])
            ], style = {'fontSize': '12px'})
        ],style = {
            # 'width': 'calc(100%-40px)',
            'border-radius': '5px',
            'background-color': '#FFFFFF', #'#f9f9f9',
            'margin': '10px',
            'padding': '15px',
            'position': 'relative',
            'box-shadow': '2px 2px 2px lightgrey'
        })
],style = {
        'width': 'calc(100%-40px)',
        'border-radius': '5px',
        'background-color': '#f9f9f9',
        'margin': '10px',
        'padding': '15px',
        'position': 'relative',
        'box-shadow': '2px 2px 2px lightgrey'})

@app.callback(Output('g0', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):

    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]

        fig = px.line(filtered_df_orig, x='t', y='activo', 
            labels={
            "t": "Tiempo (t)",
            "activo": "Estimación"}, title='Comportamiento del modelo SIR a partir de la data original a lo largo del tiempo del Covid-19')
        fig.add_scatter(x=filtered_df_orig['t'], y=filtered_df_orig['confirmado'], mode = 'lines', name='Nuevos Casos')
        fig.add_scatter(x=filtered_df_orig['t'], y=filtered_df_orig['total_rec'], mode = 'lines', name='Recuperados')
        fig.add_scatter(x=filtered_df_orig['t'], y=filtered_df_orig['muertos'], mode = 'lines', name='Muertos')


        fig.update_layout(
            legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            bgcolor="aliceblue",
            bordercolor="aliceblue",
            borderwidth=2
            )
        )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig

@app.callback(Output('g1', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):

    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]
        filtered_df_pred = predichos[predichos['Ciudad de ubicación'] == selected_city]

        if selected_city == 'Bogotá D.C.' or  selected_city == 'Barranquilla':
            alto = 10000
        else:
            alto = 4000

        fig = px.line(filtered_df_orig, x='t', y='activo', 
        labels={
                     "t": "Tiempo (t)",
                     "activo": "Estimación"
            }, title='Casos Activos')
        fig.add_traces(go.Scatter(x=filtered_df_pred['t'], y=filtered_df_pred['activo'], mode = 'lines',name='Predicho'))
        fig.add_trace(go.Scatter(x=[int(corto_plazo), int(corto_plazo)], y=[0, alto], mode="lines", name="Corto Plazo", line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(mediano_plano), int(mediano_plano)], y=[0, alto], mode="lines", name="Mediano Plazo",line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(largo_plazo), int(largo_plazo)], y=[0, alto], mode="lines", name="Largo Plazo",line = dict(dash='dot')))

        fig.update_layout(
            legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            bgcolor="aliceblue",
            bordercolor="aliceblue",
            borderwidth=2
            )
        )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig



@app.callback(Output('g2', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):
    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]
        filtered_df_pred = predichos[predichos['Ciudad de ubicación'] == selected_city]

        if selected_city == 'Bogotá D.C.':
            alto = 20000
        else:
            alto = 6000

        fig = px.line(filtered_df_orig, x='t', y='confirmado', 
            labels={
                     "t": "Tiempo (t)",
                     "confirmado": "Estimación"
            }, title='Casos Confirmados')
        fig.add_traces(go.Scatter(x=filtered_df_pred['t'], y=filtered_df_pred['confirmado'], name='Predicho'))
        fig.add_trace(go.Scatter(x=[int(corto_plazo), int(corto_plazo)], y=[0, alto], mode="lines", name="Corto Plazo", line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(mediano_plano), int(mediano_plano)], y=[0, alto], mode="lines", name="Mediano Plazo",line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(largo_plazo), int(largo_plazo)], y=[0, alto], mode="lines", name="Largo Plazo",line = dict(dash='dot')))

        fig.update_layout(
            legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            bgcolor="aliceblue",
            bordercolor="aliceblue",
            borderwidth=2
            )
        )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig

@app.callback(Output('g3', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):
    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]
        filtered_df_pred = predichos[predichos['Ciudad de ubicación'] == selected_city]

        if selected_city == 'Bogotá D.C.' or  selected_city == 'Barranquilla':
            alto = 15000
        else:
            alto = 4000

        fig = px.line(filtered_df_orig, x='t', y='total_rec', 
        labels={
                     "t": "Tiempo (t)",
                     "total_rec": "Estimación"
            }, title= 'Recuperados')
        fig.add_traces(go.Scatter(x=filtered_df_pred['t'], y=filtered_df_pred['total_rec'], name='Predicho'))
        fig.add_trace(go.Scatter(x=[int(corto_plazo), int(corto_plazo)], y=[0, 4000], mode="lines", name="Corto Plazo", line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(mediano_plano), int(mediano_plano)], y=[0, 4000], mode="lines", name="Mediano Plazo",line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(largo_plazo), int(largo_plazo)], y=[0, 4000], mode="lines", name="Largo Plazo",line = dict(dash='dot')))

        fig.update_layout(
        legend=dict(
        # x=0,
        # y=1,
        traceorder="reversed",
        bgcolor="aliceblue",
        bordercolor="aliceblue",
        borderwidth=2
        )
    )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig

@app.callback(Output('g4', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):
    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]
        filtered_df_pred = predichos[predichos['Ciudad de ubicación'] == selected_city]

        fig = px.line(filtered_df_orig, x='t', y='muertos', 
        labels={
                     "t": "Tiempo (t)",
                     "muertos": "Estimación"
            }, title= 'Muertos')
        fig.add_traces(go.Scatter(x=filtered_df_pred['t'], y=filtered_df_pred['muertos'], name='Predicho'))
        fig.add_trace(go.Scatter(x=[int(corto_plazo), int(corto_plazo)], y=[0, 8], mode="lines", name="Corto Plazo", line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(mediano_plano), int(mediano_plano)], y=[0, 8], mode="lines", name="Mediano Plazo",line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(largo_plazo), int(largo_plazo)], y=[0, 8], mode="lines", name="Largo Plazo",line = dict(dash='dot')))

        fig.update_layout(
            legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            bgcolor="aliceblue",
            bordercolor="aliceblue",
            borderwidth=2
            )
        )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig

@app.callback(Output('g5', 'figure'), [Input('ciudades_checklist', 'value')])
def update_figure(selected_city):
    if file_status == 'sucess':
        filtered_df_orig = originales[originales['Ciudad de ubicación'] == selected_city]
        filtered_df_pred = predichos[predichos['Ciudad de ubicación'] == selected_city]

        fig = px.line(filtered_df_orig, x='t', y='contagio', 
        labels={
                     "t": "Tiempo (t)",
                     "contagio": "Estimación"
            }, title='Nuevos Casos')
        fig.add_traces(go.Scatter(x=filtered_df_pred['t'], y=filtered_df_pred['contagio'], name='Predicho'))
        fig.add_trace(go.Scatter(x=[int(corto_plazo), int(corto_plazo)], y=[0, 400], mode="lines", name="Corto Plazo", line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(mediano_plano), int(mediano_plano)], y=[0, 400], mode="lines", name="Mediano Plazo",line = dict(dash='dot')))
        fig.add_trace(go.Scatter(x=[int(largo_plazo), int(largo_plazo)], y=[0, 400], mode="lines", name="Largo Plazo",line = dict(dash='dot')))

        fig.update_layout(
            legend=dict(
            # x=0,
            # y=1,
            traceorder="reversed",
            bgcolor="aliceblue",
            bordercolor="aliceblue",
            borderwidth=2
            )
        )

        fig.layout.plot_bgcolor = '#FFFFFF'##DCDCDC'
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

# %%
