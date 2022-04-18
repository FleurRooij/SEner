# -*- coding: utf-8 -*-
"""
Created on Sun 7th Jul 12:12:59 2021

@author: Joana Bugalho
"""

#import libraries
import dash
import dash_bootstrap_components as dbc
import dash_gif_component as gif
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp
import dash_table


from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
#pip install pycountry-convert


#import libraries for regression
from sklearn.model_selection import train_test_split
from sklearn import  metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn import  linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.neural_network import MLPRegressor





app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True #callback to ids outside layout
pd.options.plotting.backend = "plotly"

config = {'responsive': True}
autosize=True

#get all csv files to use
df=pd.read_csv('energy_consumption_by_source_final.csv')
df1=pd.read_csv('generation_energy_final.csv')
df2=pd.read_csv('share_energy_final.csv')
df_no_data=pd.read_csv('no_data.csv')
df_india=pd.read_csv('power_generation_india.csv')


#define all arrays to select certain columns
Regions =[]
Regions = ['World', 'Africa', 'Asia Pacific','Central America', 'Eastern Africa',
           'Europe', 'Europe (other)', 'Ivory Coast', 'Middle East', 'North America',
           'OPEC', 'Other Asia & Pacific', 'CIS', 'Other CIS', 'Other Caribbean',
           'Caribbean', 'Other Middle East', 'Other Northern Africa', 'Other Africa',
           'Other South America', 'Other Southern Africa', 'South & Central America',
           'United States Pacific Islands', 'Western Africa', 'Middle Africa', 'Netherlands Antilles', 'North America',
          'Reunion', 'Asia and Oceania', 'Central and South America', 'EU-28', 'Eurasia', 'OECD', 'OPEC', 
          'Other S. & Cent. America', 'Persian Gulf', 'Central and South America']


columns_consumption = ['Total', 'Coal', 'Fossil Fuels', 'Gas', 'Hydro', 'Nuclear',
                       'Oil', 'Renewables', 'Solar', 'Wind']

columns_generation = ['Coal', 'Gas', 'Oil', 'Electricity',
                       'Wind', 'Solar', 'Geo Biomass Other', 'Hydro']

columns_share = ['Fossil fuels', 'Coal', 'Gas', 'Hydro', 'Nuclear',
                       'Oil', 'Renewables', 'Solar', 'Wind']


#Define a function to get the continent from the name of country using pycountry_convert ----
def get_continent(col):

    cn_a2_code =  country_name_to_country_alpha2(col.Entity)

    cn_continent = country_alpha2_to_continent_code(cn_a2_code)
 
    return cn_continent

#define all elements
# CONSUMPTION ------------------------
world_cons = px.choropleth(df, 
                    locations=df["Entity"], locationmode='country names',
                    color=df['Total'], hover_name=df["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=['Total'],
                    animation_frame = df['Year'],
                    range_color=(0, 40000))


chart_cons = px.line(df, x=df['Year'], y=df['Total'], color = df['Entity'],
                     hover_name=df['Entity'])

# GENERATION ------------------------
world_gen = px.choropleth(df1, 
                    locations=df1["Entity"], locationmode='country names',
                    color=df1['Electricity'], hover_name=df1["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=['Electricity'],
                    animation_frame = df1['Year'],
                    range_color=(0, 40000))


chart_gen = px.line(df1, x=df1['Year'], y=df1['Electricity'], color = df1['Entity'],
                     hover_name=df1['Entity'])

# SHARE ------------------------
world_share = px.choropleth(df2, 
                    locations=df2["Entity"], locationmode='country names',
                    color=df2['Fossil fuels'], hover_name=df2["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=['Fossil fuels'],
                    animation_frame = df2['Year'],
                    range_color=(0, 40000))


chart_share = px.line(df2, x=df2['Year'], y=df2['Fossil fuels'], color = df2['Entity'],
                     hover_name=df2['Entity'])


# COUNTRY ------------------------
df_country = df[df['Entity'] == 'Portugal']
df_country_pie = df2[df2['Entity'] == 'Portugal']
df_country_pie = df_country_pie.set_index('Year')

df_melt = pd.melt(df_country, id_vars='Year', value_vars=columns_consumption)

country_share = go.Figure(go.Sunburst(
                            labels=["Fossil fuels", "Coal", "Gas", "Oil", "Nuclear", "Renewables", "Hydro", "Solar", "Wind"],
                            parents=["", "Fossil fuels", "Fossil fuels", "Fossil fuels", "", "", "Renewables", "Renewables", "Renewables" ],
                            values=[df_country_pie.at[2015, 'Fossil fuels'],
                                    df_country_pie.at[2015, 'Coal'],
                                    df_country_pie.at[2015, 'Gas'],
                                    df_country_pie.at[2015, 'Oil'],
                                    df_country_pie.at[2015, 'Nuclear'],
                                    df_country_pie.at[2015, 'Renewables'],
                                    df_country_pie.at[2015, 'Hydro'],
                                    df_country_pie.at[2015, 'Solar'],
                                    df_country_pie.at[2015, 'Wind']]                           
                        ))


chart_country = px.line(df_melt, x='Year', y='value', color = 'variable')

chart_country.update_xaxes(title_text="Year"),
chart_country.update_yaxes(title_text="Consumption"),

df_table = df_country.drop(columns = ['Entity']) #df to fill initial table

#FORECAST --------------------------------------
india_forecast_graph_1 = px.line(df_no_data, x='name', y='errors')



# STYLING ----------------------------
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "10rem",
    "padding": "2rem 1rem",
    "background-color": "#0096c7",
    "fontWeight": "bold",
}


# padding for the page content
CONTENT_STYLE = {
    "margin": 0,
    "margin-left": "8rem",
    "margin-right": "0rem",
    "marginBottom" : 0,
    #'height': '2000px', #'200vh',
    #"background-size": "cover",
    "padding": "2rem 1rem",
    "background-color" : "#caf0f8",
    "responsive" : True,
    "autosize" : True
}

#define SIDEBAR
sidebar = html.Div(
    [
        html.H2("Menu", className="display-5", style={'fontWeight': 'bold', 'color':'white'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home",style={'color':'white'}, href="/", active="exact"),
                dbc.NavLink("Consumption",style={'color':'white'}, href="/consumption", active="exact"),
                dbc.NavLink("Generation",style={'color':'white'}, href="/generation", active="exact"),
                dbc.NavLink("Share",style={'color':'white'}, href="/share", active="exact"),
                dbc.NavLink("Country",style={'color':'white'}, href="/country", active="exact"),
                dbc.NavLink("Forecast",style={'color':'white'}, href="/forecast", active="exact"),
                dbc.NavLink("About",style={'color':'white'}, href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#define PAGE CONTENT
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


#LAYOUT -----------------------
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
    
])

# RENDER EACH PAGE ---------------------
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def render_page_content(pathname):
    if pathname == "/":
        return [
            
                 html.Div([html.Img(src=app.get_asset_url('IST.png'),
        style = {'height': '25%', 'width': '15%', 'marginTop': 10})], style={'textAlign': 'right'}),

            
                html.H1('Energy Worldwide',
                        style={'font-size': '60px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "3rem"}),
            
                html.Div([html.H3('Explore how the energy consumption and generation has changed all over the world!',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                
                html.Div([html.H3('Here you can find the energy discriminated by country and by type: fossil fuels, renewables and nuclear.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                
                html.Div([html.H3('Go to another tab, presented in the Menu, to see some results.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                
                html.Div([
                    gif.GifPlayer(
                        gif='assets/menu_gif.gif',
                        still='assets/menu_png.png',
                    )
                ], style={ 'textAlign': 'right', 'marginTop': 30}),
                
                     
                
                ]
    
#------------------- 
    elif pathname == "/consumption":
        return [
            
                 html.H1('Energy Consumption',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
                 html.Div([html.H3('What would you like to see?',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                 
                 html.Div([
                     html.Div([
                                dcc.Dropdown(
                                    id='menu_dropdown_1',
                                    options=[
                                    {'label': 'Total', 'value': 'Total'},
                                    {'label': 'Coal', 'value': 'Coal'},
                                    {'label': 'Fossil Fuels', 'value': 'Fossil Fuels'},
                                    {'label': 'Gas', 'value': 'Gas'},
                                    {'label': 'Hydro', 'value': 'Hydro'},
                                    {'label': 'Nuclear', 'value': 'Nuclear'},
                                    {'label': 'Oil', 'value': 'Oil'},
                                    {'label': 'Renewables', 'value': 'Renewables'},
                                    {'label': 'Solar', 'value': 'Solar'},
                                    {'label': 'Wind', 'value': 'Wind'}],
                                    placeholder = "Select a source...",
                                    value='Total'
                                ),
                        ], className="six columns", style = {"width": "30%", "margin-left": "4rem"},),
                     
                     html.Div([
                         dcc.RadioItems(id = 'regions_cons',
                                            options=[
                                                {'label': 'All', 'value': 'All'},
                                                {'label': 'Only Regions', 'value': 'reg'},
                                                {'label': 'Europe', 'value': 'EU'},
                                                {'label': 'Africa', 'value': 'AF'},
                                                {'label': 'Asia', 'value': 'AS'},
                                                {'label': 'North America', 'value': 'NA'},
                                                {'label': 'South America', 'value': 'SA'},
                                            ],
                                            value='All',
                                            labelStyle={'display': 'inline-block'}
                                        ),
                         ], className="six columns", style = {"margin-left": "10rem"}),
                     
                     ], className="row"),


                    html.Div([
                        html.Div([
                            dcc.Graph(id = 'world_cons', figure=world_cons)
                        ], className="six columns", style = {'width': '45%','textAlign': 'left', "margin-left": "4rem", 'marginTop': 20},),
                        
                        
                         html.Div([                             
                            dcc.Graph(id = 'chart_cons', figure=chart_cons)
                        ], className="six columns", style = {'width': '45%','textAlign': 'right', "margin-left": "2rem", 'marginTop': 20},),
                        
                      ], className="row"),


                html.Div([html.H3('(*) The countries left in gray do not have the data recorded.',
                         style={'font-size': '10px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),

                ]
    

    
    
#----------------    
    elif pathname == "/generation":
        return [
                   
                 html.H1('Energy Generation',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
                 html.Div([html.H3('What would you like to see?',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                 
                 html.Div([
                     html.Div([
                                dcc.Dropdown(
                                    id='menu_dropdown_2',
                                    options=[
                                    {'label': 'Electricity', 'value': 'Electricity'},
                                    {'label': 'Coal', 'value': 'Coal'},
                                    {'label': 'Gas', 'value': 'Gas'},
                                    {'label': 'Oil', 'value': 'Oil'},
                                    {'label': 'Wind', 'value': 'Wind'},
                                    {'label': 'Solar', 'value': 'Solar'},
                                    {'label': 'Geo Biomass Other', 'value': 'Geo Biomass Other'},
                                    {'label': 'Hydro', 'value': 'Hydro'}],
                                    placeholder = "Select a source...",
                                    value='Electricity'
                                ),
                        ], className="six columns", style = {"width": "30%", "margin-left": "4rem"},),
                     
                     html.Div([
                         dcc.RadioItems(id = 'regions_gen',
                                            options=[
                                                {'label': 'All', 'value': 'All'},
                                                {'label': 'Only Regions', 'value': 'Regions'},
                                                {'label': 'Europe', 'value': 'EU'},
                                                {'label': 'Africa', 'value': 'AF'},
                                                {'label': 'Asia', 'value': 'AS'},
                                                {'label': 'North America', 'value': 'NA'},
                                                {'label': 'South America', 'value': 'SA'},
                                            ],
                                            value='All',
                                            labelStyle={'display': 'inline-block'}
                                        ),
                         ], className="six columns", style = {"margin-left": "10rem"}),
                     
                     ], className="row"),


                    html.Div([
                        html.Div([
                            dcc.Graph(id = 'world_gen', figure=world_gen)
                        ], className="six columns", style = {'width': '45%','textAlign': 'left', "margin-left": "4rem", 'marginTop': 20},),
                        
                        
                         html.Div([                             
                            dcc.Graph(id = 'chart_gen', figure=chart_gen)
                        ], className="six columns", style = {'width': '45%','textAlign': 'right', "margin-left": "2rem", 'marginTop': 20},),
                        
                      ], className="row"),


                html.Div([html.H3('(*) The countries left in gray do not have the data recorded.',
                         style={'font-size': '10px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
      

                ]
    
#----------------    
    elif pathname == "/share":
        return [
            
                 html.H1('Share by type (in %)',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
                html.Div([html.H3('Consumption',
                         style={'font-size': '30px','marginTop': 5,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"})],
                         style = {'textAlign': 'left'}),
                
                 html.Div([html.H3('What would you like to see?',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                 
                 html.Div([
                     html.Div([
                                dcc.Dropdown(
                                    id='menu_dropdown_3',
                                    options=[
                                    {'label': 'Fossil Fuels', 'value': 'Fossil fuels'},
                                    {'label': 'Coal', 'value': 'Coal'},
                                    {'label': 'Gas', 'value': 'Gas'},
                                    {'label': 'Oil', 'value': 'Oil'},
                                    {'label': 'Renewables', 'value': 'Renewables'},
                                    {'label': 'Wind', 'value': 'Wind'},
                                    {'label': 'Solar', 'value': 'Solar'},
                                    {'label': 'Hydro', 'value': 'Hydro'},
                                    {'label': 'Nuclear', 'value': 'Nuclear'}],
                                    placeholder = "Select a source...",
                                    value='Fossil fuels'
                                ),
                        ], className="six columns", style = {"width": "30%", "margin-left": "4rem"},),
                     
                     html.Div([
                         dcc.RadioItems(id = 'regions_share',
                                            options=[
                                                {'label': 'All', 'value': 'All'},
                                                {'label': 'Only Regions', 'value': 'Regions'},
                                                {'label': 'Europe', 'value': 'EU'},
                                                {'label': 'Africa', 'value': 'AF'},
                                                {'label': 'Asia', 'value': 'AS'},
                                                {'label': 'North America', 'value': 'NA'},
                                                {'label': 'South America', 'value': 'SA'},
                                            ],
                                            value='All',
                                            labelStyle={'display': 'inline-block'}
                                        ),
                         ], className="six columns", style = {"margin-left": "10rem"}),
                     
                     ], className="row"),


                    html.Div([
                        html.Div([
                            dcc.Graph(id = 'world_share', figure=world_share)
                        ], className="six columns", style = {'width': '45%','textAlign': 'left', "margin-left": "4rem", 'marginTop': 20},),
                        
                        
                         html.Div([                             
                            dcc.Graph(id = 'chart_share', figure=chart_share)
                        ], className="six columns", style = {'width': '45%','textAlign': 'right', "margin-left": "2rem", 'marginTop': 20},),
                        
                      ], className="row"),


                html.Div([html.H3('(*) The countries left in gray do not have the data recorded.',
                         style={'font-size': '10px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
            
            
            

                ]
    
    
#----------------    
    elif pathname == "/country":
        return [
            
                 html.H1('Country',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
                 html.Div([html.H3('Which country would you like to see?',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                 
                 html.Div([
                                dcc.Dropdown(
                                    id='menu_dropdown_4',
                                    options=[
                                                {'label': i, 'value': i}
                                                for i in df['Entity'].unique()
                                            ],
                                    placeholder = "Select a country or region...",
                                    value='Portugal'
                                ),
                        ], style = {"width": "30%", "margin-left": "4rem"}),
                 
                 html.Div([
                     html.Div([
                         
                         dcc.Dropdown(
                                    id='menu_dropdown_year',
                                    options=[
                                                {'label': i, 'value': i}
                                                for i in df2['Year'].unique()
                                            ],
                                    placeholder = "Select a year...",
                                    value=2015
                                ),
                         ], className="six columns", style = {'width': '15%', 'marginTop': 10, "margin-left": "10rem"}),
                     
                     html.Div([
                         dcc.RadioItems(id = 'country_opt',
                                            options=[
                                                {'label': 'Consumption', 'value': 'Consumption'},
                                                {'label': 'Generation', 'value': 'Generation'},
                                                #{'label': 'bla', 'value': 'MTL'},
                                            ],
                                            value='Consumption',
                                            labelStyle={'display': 'inline-block'}
                                        ),
                         ], className="six columns", style = {'marginTop': 10, "margin-left": "20rem"}),
                     
                     ], className="row"),
                     
                    
                  html.Div([
                        html.Div([
                            dcc.Graph(id = 'country_share', figure=country_share)
                        ], className="six columns", style = {'width': '40%', 'textAlign': 'left', "margin-left": "4rem", 'marginTop': 20},),
                        
                        
                         html.Div([                             
                            dcc.Graph(id = 'chart_country', figure=chart_country)
                        ], className="six columns", style = {'width': '50%','textAlign': 'right', "margin-left": "2rem", 'marginTop': 20},),
                        
                      ], className="row", style = {autosize: True}),
                  
                  html.Div([html.H3('(*) Blank means that there is no data recorded.',
                         style={'font-size': '10px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                  
                   html.Div([html.H3('Choose a dataset to see:',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         style = {'textAlign': 'left'}),
                  
                 html.Div([
                                dcc.Dropdown(
                                    id='menu_dropdown_5',
                                    options=[
                                    {'label': 'Consumption', 'value':'Consumption'},
                                    {'label': 'Generation', 'value': 'Generation'},
                                    {'label': 'Share', 'value': 'Share'}],
                                    placeholder = "Select what data you wish to see...",
                                    value='Consumption'
                                ),
                        ], className="six columns", style = {"width": "30%", "margin-left": "4rem", 'marginTop': 20}),
                
                
                
                html.Div([
                    
                    dash_table.DataTable(
                                        id='mydatatable_country',
                                        columns=[{'name': str(i), 'id': str(i)} for i in df_table.columns],
                                        data = df_table.to_dict('records'),
                                        style_header={
                                                    'backgroundColor': '#89c2d9',
                                                    'fontWeight': 'bold'
                                                }),
                    ], style = {'width': '50%','textAlign': 'right', "margin-left": "4rem", 'marginTop': 20}),
            
            

                ]
    
    
#----------------    
    elif pathname == "/forecast":
        return [
                
            html.H1('Solar Power Generation',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
            html.H2('Forecast for a Power Plant in India',
                        style={'font-size': '30px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
            
            html.Div([html.H3('We will analyse the data recovered at a power plant in India over a 34 day period. There are two datasets, one regarding the power generation and the other the sensor readings.',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9',"fontWeight": "bold","margin-left": "2rem"})],
                         style = {'textAlign': 'left'}),
             
            html.H2('Visualization of the raw data',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
             dcc.Graph(
                id='clean-data',
                figure={
                    'data': [
                        {'x': df_india.Date, 'y': df_india.AMBIENT_TEMPERATURE, 'type': 'line', 'name': 'Ambient Temperature (ºC)', 'opacity': 0.7},
                        {'x': df_india.Date, 'y': df_india.MODULE_TEMPERATURE, 'type': 'line', 'name': 'Module Temperature (ºC)', 'opacity': 0.7},
                        {'x': df_india.Date, 'y': df_india.IRRADIATION, 'type': 'line', 'name': 'Irradiation', 'opacity': 0.7},
                        {'x': df_india.Date, 'y': df_india.DC_POWER, 'type': 'line', 'name': 'DC Power (kW)', 'opacity': 0.7},
                        {'x': df_india.Date, 'y': df_india.AC_POWER, 'type': 'line', 'name': 'AC Power (kW)', 'opacity': 0.7},
                    ],            
                    'layout': {
                        'xaxis' : {'tickformat':' %d %b %Y'}
                    }
                },  style = {'width': '90%', 'textAlign': 'left', "margin-left": "3rem", 'marginTop': 10}
            ),
             
             
             html.Div([html.H3('There is information on the AC and DC power generated and the sensor readings: Ambient Temperature, Module Temperature - sensor attached to the panel - and Irradiation.',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"})],
                         style = {'textAlign': 'left'}),
               
             html.H2('Regression Model',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
            
            html.Div([html.H3('Here, you can choose what model you wish to see and what features would you like to apply.',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"})],
                         style = {'textAlign': 'left'}),
            
            
            
             html.Div([
                 
                 html.Div([html.H3('Choose which power would you like to model:',
                         style={'font-size': '20px','marginTop': 20,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold", "margin-left": "4rem"})],
                         className="six columns", style = {'textAlign': 'left'}),
                 
                 html.Div([
                 
                                dcc.Dropdown(
                                    id='menu_dropdown_india',
                                    options=[
                                    {'label': 'AC Power', 'value':'AC_POWER'},
                                    {'label': 'DC Power', 'value': 'DC_POWER'}],
                                    placeholder = "Select a power...",
                                    value='AC_POWER'
                                ),
                        ], className="six columns", style = {"width": "15%", "margin-left": "3rem", 'marginTop': 20}),
                 
                 ], className="row"),
              
            
            html.Div([
                
                html.Div([html.H3('Features:',
                         style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "4rem"})],
                         className = "six columns"),
                
                html.Div([html.H3('Model:',
                                 style={'font-size': '20px','marginTop': 30,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "38rem"})],
                                 className = "six columns"),
                
                
                ], className="row", style = {autosize: True}),
            
            
            
               html.Div([
                
                   
                        html.Div([
                         dcc.Dropdown(id = 'india_opt_feat',
                                            options=[
                                                {'label': 'Ambient Temperature', 'value': 'AMBIENT_TEMPERATURE'},
                                                {'label': 'Module Temperature', 'value': 'MODULE_TEMPERATURE'},
                                                {'label': 'Irradiation', 'value': 'IRRADIATION'},
                                                {'label': 'AC Power-1', 'value': 'AC_POWER-1'},
                                                {'label': 'DC Power-1', 'value': 'DC_POWER-1'},
                                                {'label': 'Hour', 'value': 'hour'},
                                                #{'label': 'bla', 'value': 'MTL'},
                                            ],
                                            value=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION', 'AC_POWER-1'],
                                            multi = True,
                                        ),
                         ], className="six columns", style = {"width": "55%",'marginTop': 10, "margin-left": "4rem"}),
                
                        
                        
                        html.Div([
                                 dcc.Dropdown(id = 'india_opt_model',
                                                    options=[
                                                        {'label': 'Linear Regressor', 'value': 'Linear Regressor'},
                                                        {'label': 'Support Vector Regressor', 'value': 'Support Vector Regressor'},
                                                        {'label': 'Decision Tree Regressor', 'value': 'Decision Tree Regressor'},
                                                        {'label': 'Random Forest Regressor', 'value': 'Random Forest Regressor'},
                                                        {'label': 'Gradient Boosting Regressor', 'value': 'Gradient Boosting Regressor'},
                                                        {'label': 'Extreme Gradient Boosting Regressor', 'value': 'Extreme Gradient Boosting Regressor'},
                                                        {'label': 'Boot Strappping Regressor', 'value': 'Boot Strappping Regressor'},
                                                        {'label': 'Neural Networks', 'value': 'Neural Networks'},
                                                        #{'label': 'bla', 'value': 'MTL'},
                                                    ],
                                                    value='Linear Regressor',
                                                ),
                                 ], className="six columns", style = {"width": "30%",'marginTop': 10, "margin-left": "4rem"}),
                           
                        
                        ], className="row"),
               
               
               html.Div([
                   
                   html.Div([
                            dcc.Graph(id = 'india_forecast_1', figure=india_forecast_graph_1)
                        ], className="six columns", style = {'width': '80%', 'textAlign': 'left', "margin-left": "4rem", 'marginTop': 20},),
                        
                   
                   
                    html.Div([
                        
                        dash_table.DataTable(
                                        id='india_forecast_results',
                                        columns=[{'id' : 'name', 'name': ''},
                                                 {'id': 'error', 'name': 'error', 'type': 'numeric'},],
                                        data = df_no_data.to_dict('rows'),
                                        style_header={
                                                    'backgroundColor': '#89c2d9',
                                                    'fontWeight': 'bold'
                                                }),
                    

                        ], className="six columns", style = {'width': '15%','textAlign': 'right', "margin-left": "4rem", 'marginTop': 20})
            
                   
                   ], className="row"),
               
       
            
              

                ]

#----------------    
    elif pathname == "/about":
        return [

             html.H1('About',
                        style={'font-size': '50px','marginTop': 10,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
            
            html.H2('The objective of this project is to show how the consumption and generation of energy has changed in the last 40 years (detailed by the type of energy), as well as a forecasting model for the generation of energy at a power plant in India.',
                        style={'font-size': '20px','marginTop': 20,'textAlign':'left', 'color': '#61a5c2', "fontWeight": "bold","margin-left": "2rem"}),
            
            
            
            
            html.Div([
                html.H2('Consumption, Generation and Share',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
                
                html.H3('The user can view how the values of energy have changed.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                html.H3('First, you can choose what type of energy you would like to see. The available data is presented by year in two ways, in a world map and in a graph. In addition, in order to visualize only a portion of the countries presented at the graph, you can select which fraction you would like to see.',
                         style={'font-size': '20px','marginTop': 5,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                         
                ]),
             
             html.Div([
                html.H2('Country',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
                
                html.H3('The user can view all the information about a particular country.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                html.H3('By selecting a country, it is presented a pie chart with the share of energy consumption by type (the year can also be defined). Next to it, there is a graph with the evolution of the share of energy, also by type. One can select to see the consumption or generation. At last, all the data is provided in a table below.',
                         style={'font-size': '20px','marginTop': 5,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                         
                ]),
             
             html.Div([
                html.H2('Forecast',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
                
                html.H3('In this page, an analysis of the energy generation at a power plant in India is presented.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                html.H3('The raw data is shown. To see only one feature, press two times on top of the name. For the forecast model, you can select what power to forecast, AC or DC power, what features to include and what regressor to use. Ultimately, the results are presented below.',
                         style={'font-size': '20px','marginTop': 5,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                         
                ]),
             
             html.Div([
                html.H2('Download',
                        style={'font-size': '25px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
                
                html.H3('Click below to download all the datasets used to complete this project.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                      
                html.Button("Download Datasets", id="btn", n_clicks = 0, style= {'margin-left': '3rem', 'background-color': 'white'}), 
                dcc.Download(id="download"),
                
                html.H3('For a more detailed analysis about the forecast, download the jupyter file below.',
                         style={'font-size': '20px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                      
                html.Button("Download Forecast", id="btn1", n_clicks = 0, style= {'margin-left': '3rem', 'background-color': 'white'}), 
                dcc.Download(id="download1")
                
                ]),
             
             html.H3('Sources:',
                         style={'font-size': '20px','marginTop': 20,'textAlign':'left', 'color': '#0077b6', "fontWeight": "bold","margin-left": "2rem"}),
             
             html.H3(html.A("BP Statistical Review of World Energy", href='https://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy.html', target="_blank"),
                     style={'font-size': '15px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),

             html.H3(html.A("Shift Energy Data Portal", href='https://www.theshiftdataportal.org/energy', target="_blank"),
                     style={'font-size': '15px','marginTop': 10,'textAlign':'left', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),

             
             
              html.H3('Author: Joana Bugalho, e-mail: joana.bugalho@tecnico.ulisboa.pt',
                         style={'font-size': '12px','marginTop': 10,'textAlign':'right', 'color': '#89c2d9', "fontWeight": "bold","margin-left": "2rem"}),
                  

            
                ]
    
    
    
    
#-----------------    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised. Please try again."),
        ]
    )


# CONSUMPTION ------------------------------------------
@app.callback(
    dash.dependencies.Output(component_id='world_cons', component_property='figure'),
    dash.dependencies.Output(component_id='chart_cons', component_property='figure'),
    dash.dependencies.Input(component_id="menu_dropdown_1", component_property="value"),
    dash.dependencies.Input(component_id="regions_cons", component_property="value"))

def update_world_cons(source, regions):
    
    a = df[source][df['Entity'].isin(Regions) == False].max()
    df_cont =  df[df['Entity'].isin(Regions) == False]
    df_cont['Continent'] = df_cont.apply(get_continent, axis = 1)
    
    world_cons = px.choropleth(df, 
                    locations=df["Entity"], locationmode='country names',
                    color=df[source], hover_name=df["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=[source],
                    animation_frame = df['Year'],
                    range_color=(0, a))
    
    
    if regions == 'reg':
        chart_cons = px.line(df, x=df['Year'][df['Entity'].isin(Regions)], y=df[source][df['Entity'].isin(Regions)], color = df['Entity'][df['Entity'].isin(Regions)],
                     hover_name=df['Entity'][df['Entity'].isin(Regions)])
    if regions == 'EU':
        chart_cons = px.line(df_cont, x=df_cont['Year'][df_cont['Continent'] == regions] , y=df_cont[source][df_cont['Continent'] == regions], color = df_cont['Entity'][df_cont['Continent'] == regions],
                     hover_name=df_cont['Entity'][df_cont['Continent'] == regions])
    if regions == 'AF':
        chart_cons = px.line(df_cont, x=df_cont['Year'][df_cont['Continent'] == regions] , y=df_cont[source][df_cont['Continent'] == regions], color = df_cont['Entity'][df_cont['Continent'] == regions],
                     hover_name=df_cont['Entity'][df_cont['Continent'] == regions])
    if regions == 'AS':
        chart_cons = px.line(df_cont, x=df_cont['Year'][df_cont['Continent'] == regions] , y=df_cont[source][df_cont['Continent'] == regions], color = df_cont['Entity'][df_cont['Continent'] == regions],
                     hover_name=df_cont['Entity'][df_cont['Continent'] == regions])
    if regions == 'NA':
        chart_cons = px.line(df_cont, x=df_cont['Year'][df_cont['Continent'] == regions] , y=df_cont[source][df_cont['Continent'] == regions], color = df_cont['Entity'][df_cont['Continent'] == regions],
                     hover_name=df_cont['Entity'][df_cont['Continent'] == regions])
    if regions == 'SA':
        chart_cons = px.line(df_cont, x=df_cont['Year'][df_cont['Continent'] == regions] , y=df_cont[source][df_cont['Continent'] == regions], color = df_cont['Entity'][df_cont['Continent'] == regions],
                     hover_name=df_cont['Entity'][df_cont['Continent'] == regions])
    if regions == 'All':
        chart_cons = px.line(df, x=df['Year'], y=df[source], color = df['Entity'],
                     hover_name=df['Entity'])
    

    chart_cons.update_xaxes(title_text="Year"),
    chart_cons.update_yaxes(title_text=source),

    
    return world_cons, chart_cons


# GENERATION --------------------------------
@app.callback(
    dash.dependencies.Output(component_id='world_gen', component_property='figure'),
    dash.dependencies.Output(component_id='chart_gen', component_property='figure'),
    dash.dependencies.Input(component_id="menu_dropdown_2", component_property="value"),
    dash.dependencies.Input(component_id="regions_gen", component_property="value"))

def update_world_gen(source, regions):
    
    b = df1[source][df1['Entity'].isin(Regions) == False].max()
    
    df_cont1 =  df1[df1['Entity'].isin(Regions) == False]
    df_cont1['Continent'] = df_cont1.apply(get_continent, axis = 1)
    
    world_gen = px.choropleth(df1, 
                    locations=df1["Entity"], locationmode='country names',
                    color=df1[source], hover_name=df1["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=[source],
                    animation_frame = df1['Year'],
                    range_color=(0, b))
    
    if regions == 'Regions':
        chart_gen = px.line(df1, x=df1['Year'][df1['Entity'].isin(Regions)], y=df1[source][df1['Entity'].isin(Regions)], color = df1['Entity'][df1['Entity'].isin(Regions)],
                     hover_name=df1['Entity'][df1['Entity'].isin(Regions)])
    if regions == 'All':
        chart_gen = px.line(df1, x=df1['Year'], y=df1[source], color = df1['Entity'],
                     hover_name=df1['Entity'])
    if regions == 'EU':
        chart_gen = px.line(df_cont1, x=df_cont1['Year'][df_cont1['Continent'] == regions] , y=df_cont1[source][df_cont1['Continent'] == regions], color = df_cont1['Entity'][df_cont1['Continent'] == regions],
                     hover_name=df_cont1['Entity'][df_cont1['Continent'] == regions])
    if regions == 'AF':
        chart_gen = px.line(df_cont1, x=df_cont1['Year'][df_cont1['Continent'] == regions] , y=df_cont1[source][df_cont1['Continent'] == regions], color = df_cont1['Entity'][df_cont1['Continent'] == regions],
                     hover_name=df_cont1['Entity'][df_cont1['Continent'] == regions])
    if regions == 'AS':
        chart_gen = px.line(df_cont1, x=df_cont1['Year'][df_cont1['Continent'] == regions] , y=df_cont1[source][df_cont1['Continent'] == regions], color = df_cont1['Entity'][df_cont1['Continent'] == regions],
                     hover_name=df_cont1['Entity'][df_cont1['Continent'] == regions])
    if regions == 'NA':
        chart_gen = px.line(df_cont1, x=df_cont1['Year'][df_cont1['Continent'] == regions] , y=df_cont1[source][df_cont1['Continent'] == regions], color = df_cont1['Entity'][df_cont1['Continent'] == regions],
                     hover_name=df_cont1['Entity'][df_cont1['Continent'] == regions])
    if regions == 'SA':
        chart_gen = px.line(df_cont1, x=df_cont1['Year'][df_cont1['Continent'] == regions] , y=df_cont1[source][df_cont1['Continent'] == regions], color = df_cont1['Entity'][df_cont1['Continent'] == regions],
                     hover_name=df_cont1['Entity'][df_cont1['Continent'] == regions])
 
        
    
    chart_gen.update_xaxes(title_text="Year"),
    chart_gen.update_yaxes(title_text=source),

    
    return world_gen, chart_gen



# SHARE --------------------------------
@app.callback(
    dash.dependencies.Output(component_id='world_share', component_property='figure'),
    dash.dependencies.Output(component_id='chart_share', component_property='figure'),
    dash.dependencies.Input(component_id="menu_dropdown_3", component_property="value"),
    dash.dependencies.Input(component_id="regions_share", component_property="value"))

def update_world_share(source, regions):
    
    c = df2[source][df2['Entity'].isin(Regions) == False].max()
    
    df_cont2 =  df2[df2['Entity'].isin(Regions) == False]
    df_cont2['Continent'] = df_cont2.apply(get_continent, axis = 1)
    
    world_share = px.choropleth(df2, 
                    locations=df2["Entity"], locationmode='country names',
                    color=df2[source], hover_name=df2["Entity"], 
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_data=[source],
                    animation_frame = df2['Year'],
                    range_color=(0, c))
    
    if regions == 'Regions':
        chart_share = px.line(df2, x=df2['Year'][df2['Entity'].isin(Regions)], y=df2[source][df2['Entity'].isin(Regions)], color = df2['Entity'][df2['Entity'].isin(Regions)],
                     hover_name=df2['Entity'][df2['Entity'].isin(Regions)])
    if regions == 'All':
        chart_share = px.line(df2, x=df2['Year'], y=df2[source], color = df2['Entity'],
                     hover_name=df2['Entity'])
    if regions == 'EU':
         chart_share = px.line(df_cont2, x=df_cont2['Year'][df_cont2['Continent'] == regions] , y=df_cont2[source][df_cont2['Continent'] == regions], color = df_cont2['Entity'][df_cont2['Continent'] == regions],
                     hover_name=df_cont2['Entity'][df_cont2['Continent'] == regions])
    if regions == 'AF':
         chart_share = px.line(df_cont2, x=df_cont2['Year'][df_cont2['Continent'] == regions] , y=df_cont2[source][df_cont2['Continent'] == regions], color = df_cont2['Entity'][df_cont2['Continent'] == regions],
                     hover_name=df_cont2['Entity'][df_cont2['Continent'] == regions])
    if regions == 'AS':
         chart_share = px.line(df_cont2, x=df_cont2['Year'][df_cont2['Continent'] == regions] , y=df_cont2[source][df_cont2['Continent'] == regions], color = df_cont2['Entity'][df_cont2['Continent'] == regions],
                     hover_name=df_cont2['Entity'][df_cont2['Continent'] == regions])
    if regions == 'NA':
         chart_share = px.line(df_cont2, x=df_cont2['Year'][df_cont2['Continent'] == regions] , y=df_cont2[source][df_cont2['Continent'] == regions], color = df_cont2['Entity'][df_cont2['Continent'] == regions],
                     hover_name=df_cont2['Entity'][df_cont2['Continent'] == regions])
    if regions == 'SA':
         chart_share = px.line(df_cont2, x=df_cont2['Year'][df_cont2['Continent'] == regions] , y=df_cont2[source][df_cont2['Continent'] == regions], color = df_cont2['Entity'][df_cont2['Continent'] == regions],
                     hover_name=df_cont2['Entity'][df_cont2['Continent'] == regions])
        
    
    chart_share.update_xaxes(title_text="Year"),
    chart_share.update_yaxes(title_text=source),

    
    return world_share, chart_share


# COUNTRY --------------------------------

@app.callback(
    dash.dependencies.Output(component_id='country_share', component_property='figure'),
    dash.dependencies.Output(component_id='chart_country', component_property='figure'),
    dash.dependencies.Input(component_id="menu_dropdown_4", component_property="value"),
    dash.dependencies.Input(component_id="country_opt", component_property="value"),
     dash.dependencies.Input(component_id="menu_dropdown_year", component_property="value"))

def update_country(country, ttype, year):
    
    df_country_cons = df[df['Entity'] == country]
    df_country_gen = df1[df1['Entity'] == country]
    
    
    df_country_pie = df2[df2['Entity'] == country]
    df_country_pie = df_country_pie.set_index('Year')
    
    
    
    if df_country_pie.empty:
        
        country_share = go.Figure(go.Sunburst(
                                    labels=["No Data Found!"],
                                    parents=[""],
                                    values=[0],                         
                                ))
        
        
    else:
        country_share = go.Figure(go.Sunburst(
                                    labels=["Fossil fuels", "Coal", "Gas", "Oil", "Nuclear", "Renewables", "Hydro", "Solar", "Wind"],
                                    parents=["", "Fossil fuels", "Fossil fuels", "Fossil fuels", "", "", "Renewables", "Renewables", "Renewables" ],
                                    values=[df_country_pie.at[year, 'Fossil fuels'],
                                            df_country_pie.at[year, 'Coal'],
                                            df_country_pie.at[year, 'Gas'],
                                            df_country_pie.at[year, 'Oil'],
                                            df_country_pie.at[year, 'Nuclear'],
                                            df_country_pie.at[year, 'Renewables'],
                                            df_country_pie.at[year, 'Hydro'],
                                            df_country_pie.at[year, 'Solar'],
                                            df_country_pie.at[year, 'Wind']]
                                                              
                                ))
            
    
    if ttype == 'Consumption':
        df_melt = pd.melt(df_country_cons, id_vars='Year', value_vars=columns_consumption)
        
        if df_melt.empty:
            chart_country = px.line(df_no_data, x = 'x', y = 'y')
            
            
        else:
            chart_country = px.line(df_melt, x='Year', y='value', color = 'variable')
            
        
    if ttype == 'Generation':
        
        df_melt1 = pd.melt(df_country_gen, id_vars='Year', value_vars=columns_generation)
        
        if df_melt1.empty:
            chart_country = px.line(df_no_data, x = 'x', y = 'y')
            
            
        else:
            chart_country = px.line(df_melt1, x='Year', y='value', color = 'variable')
           


    chart_country.update_xaxes(title_text="Year"),
    chart_country.update_yaxes(title_text=ttype),
    
    return country_share, chart_country


@app.callback(
    dash.dependencies.Output(component_id='mydatatable_country', component_property='data'),
    dash.dependencies.Output(component_id='mydatatable_country', component_property='columns'),
    dash.dependencies.Input(component_id="menu_dropdown_5", component_property="value"),
    dash.dependencies.Input(component_id="menu_dropdown_4", component_property="value"))

    
def update_table_country(ttype, country):

    
    if ttype == 'Consumption':
        df_table = df[df['Entity'] == country]
    if ttype == 'Generation':
        df_table = df1[df1['Entity'] == country]
    if ttype == 'Share':
        df_table = df2[df2['Entity'] == country]
        
    df_table = df_table.drop(columns = ['Entity'])
    
    columns=[{'name': str(i), 'id': str(i)} for i in df_table.columns]
    
    data = df_table.to_dict('records')
    
    return data, columns


# FORECAST ------------------------------------------
@app.callback(
    dash.dependencies.Output(component_id='india_forecast_1', component_property='figure'),
    dash.dependencies.Output(component_id='india_forecast_results', component_property='data'),
    dash.dependencies.Output(component_id='india_forecast_results', component_property='columns'),
    dash.dependencies.Input(component_id="menu_dropdown_india", component_property="value"),
    dash.dependencies.Input(component_id="india_opt_feat", component_property="value"),
    dash.dependencies.Input(component_id="india_opt_model", component_property="value"))

def update_india_results(power, features, model):
    
    all_lists = sum([[power], features], [])
    df_model = df_india[all_lists]
    
    #define our features and slipt into test and train
    
    X = df_model.values
    Y = X[:,0]
    X = X[:,1:len(X)] 

    X_train, X_test, y_train, y_test = train_test_split(X,Y)
    
    #prediction in each model -----
        
    if model == 'Linear Regressor':
    
        regr = linear_model.LinearRegression() # creates linear regression object
        regr.fit(X_train,y_train) # trains the model using the training set
        y_pred = regr.predict(X_test) # tests the model using the test set
        
    if model == 'Support Vector Regressor':
    
        sc_X = StandardScaler()
        sc_y = StandardScaler()
        X_train_SVR = sc_X.fit_transform(X_train)
        y_train_SVR = sc_y.fit_transform(y_train.reshape(-1,1))
        y_train_SVR
        
        regr = SVR(kernel='rbf')
        regr.fit(X_train_SVR,y_train_SVR)
        
        y_pred_SVR = regr.predict(sc_X.fit_transform(X_test))
        y_pred=sc_y.inverse_transform(y_pred_SVR)
    
    
    if model == 'Decision Tree Regressor':
        
        DT_regr_model = DecisionTreeRegressor()
        
        DT_regr_model.fit(X_train, y_train)
        
        y_pred = DT_regr_model.predict(X_test)       
    
    if model == 'Random Forest Regressor':
        
        parameters = {'bootstrap': True,
              'min_samples_leaf': 3,
              'n_estimators': 100, 
              'min_samples_split': 15,
              'max_features': 'sqrt',
              'max_depth': 10,
              'max_leaf_nodes': None}
        RF_model = RandomForestRegressor(**parameters)
        RF_model.fit(X_train, y_train)
        y_pred = RF_model.predict(X_test)    
        
        
    if model == 'Gradient Boosting Regressor':
        
        GB_model = GradientBoostingRegressor()
        GB_model.fit(X_train, y_train)
        y_pred =GB_model.predict(X_test)
        
    if model == 'Extreme Gradient Boosting Regressor':
        
        XGB_model = XGBRegressor()
        XGB_model.fit(X_train, y_train)
        y_pred =XGB_model.predict(X_test)
            
        
    if model == 'Boot Strappping Regressor':
        
        BT_model = BaggingRegressor()
        BT_model.fit(X_train, y_train)
        y_pred =BT_model.predict(X_test)
        
        
    if model == 'Neural Networks':
        
        NN_model = MLPRegressor(hidden_layer_sizes=(10,10,10))
        NN_model.fit(X_train,y_train)
        y_pred = NN_model.predict(X_test)
            

        
    #graphs and table
    
    india_forecast_graph_1 = sp.make_subplots(rows = 1, cols=2)


    india_forecast_graph_1.append_trace(
        go.Scatter( y = y_test, line=dict(color='blue', width=2),name = 'Real', opacity = 0.5),
        row=1, col=1
    )
    
    india_forecast_graph_1.append_trace(
        go.Scatter(y = y_pred, line=dict(color='orange', width=2), name = 'Expected', opacity = 0.7),
        row=1, col=1
    )


    india_forecast_graph_1.append_trace(
        go.Scatter(x = y_test, y = y_pred, mode= 'markers', name = 'Power Generation'),
        row=1, col=2
    )
    
    india_forecast_graph_1.update_xaxes(title_text="N", row=1, col=1)
    india_forecast_graph_1.update_yaxes(title_text="Power Generation", row=1, col=1)
    india_forecast_graph_1.update_xaxes(title_text="Real Power Generation", row=1, col=2)
    india_forecast_graph_1.update_yaxes(title_text="Expected Power Generation", row=1, col=2)
    
    india_forecast_graph_1.update_layout(legend = dict(orientation = "h", y = -0.15))
        
        

        
    #Evaluate errors
    MAE=metrics.mean_absolute_error(y_test,y_pred) 
    MSE=metrics.mean_squared_error(y_test,y_pred)  
    RMSE= np.sqrt(metrics.mean_squared_error(y_test,y_pred))
    cvRMSE=RMSE/np.mean(y_test)
    errors_ = np.array([MAE, MSE, RMSE,cvRMSE]) 
    
    df_errors = pd.DataFrame(data = {'': ['MAE', 'MSE', 'RMSE', 'cvRMSE'], 'error': errors_})
    
    columns=[{'name':str(i), 'id': str(i)} for i in df_errors.columns]
    
    data = df_errors.to_dict('rows')



    return india_forecast_graph_1, data, columns


#DOWNLOAD csv -------------------------------
@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])

def generate_zip(n_clicks):
    
    if n_clicks !=0:
    
        zipp = "datasets.zip"
        
        return dcc.send_file(zipp,filename="dataset.zip")
    
#DOWNLOAD forecast -------------------------------
@app.callback(Output("download1", "data"), [Input("btn1", "n_clicks")])

def generate_jup(n_clicks):
    
    if n_clicks !=0:
    
        zipp = "Forecast.zip"
        
        return dcc.send_file(zipp,filename="Forecast.zip")


# ---------------------

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
    
    

    





