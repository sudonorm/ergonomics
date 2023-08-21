import dash
from dash import dcc, html, Input, Output, callback, dash_table, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

import json
import os
import shutil
from pathlib import Path
import builtins

from datetime import date

import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from utils import folderPaths

LINUX_MNT = folderPaths.LINUX_MNT
USER_DRIVE = folderPaths.USER_DRIVE
USER = folderPaths.USER

NETWORK_ROOT_FOLDER = folderPaths.NETWORK_ROOT_FOLDER
WIN_FOLDER =  folderPaths.WIN_FOLDER
ROOT_FOLDER = folderPaths.ROOT_FOLDER
SLSH = folderPaths.SLSH
BKSLH = folderPaths.BKSLH 

BASEPATH_NETWORK = folderPaths.BASEPATH_NETWORK

BASEPATH_USER = folderPaths.BASEPATH_USER

BASEPATH = BASEPATH_NETWORK


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

par_ids = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
neck_score_ids = ['1', '2', '3', '4']
trunk_posture_score_ids = ['1', '2', '3', '4', '5']
leg_posture_score_ids = ['1', '2', '3', '4']
force_load_score_ids = ['0', '1', '2', '3']

procedure_ids = ['ProbeQ1T1',
 'ProbeQ2T1',
 'ProbeQ3T1',
 'ProbeQ4T1',
 'ProbeAllQT1',
 'ScalingQ1T1',
 'ScalingQ2T1',
 'ScalingQ3T1',
 'ScalingQ4T1',
 'ScalingAllQT1',
 'PolishQ1T1',
 'PolishQ2T1',
 'PolishQ3T1',
 'PolishQ4T1',
 'PolishAllQT1',
 'FlossQ1T1',
 'FlossQ2T1',
 'FlossQ3T1',
 'FlossQ4T1',
 'FlossAllQT1',
 'ProbeQ1T2',
 'ProbeQ2T2',
 'ProbeQ3T2',
 'ProbeQ4T2',
 'ProbeAllQT2',
 'ScalingQ1T2',
 'ScalingQ2T2',
 'ScalingQ3T2',
 'ScalingQ4T2',
 'ScalingAllQT2',
 'PolishQ1T2',
 'PolishQ2T2',
 'PolishQ3T2',
 'PolishQ4T2',
 'PolishAllQT2',
 'FlossQ1T2',
 'FlossQ2T2',
 'FlossQ3T2',
 'FlossQ4T2',
 'FlossAllQT2']



# layout
layout = html.Div([

    ### date, participants, and procedure
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([
            dbc.Row([

                dbc.Col(
                [
                
                html.Label("Select the ergo assessment date: ", style={'margin': 20, 'text-align':'right'}),
                dcc.DatePickerSingle(
                    id='date-change',
                    min_date_allowed=date(int(str(date.today()).split('-')[0]) - 1, int(str(date.today()).split('-')[1]), int(str(date.today()).split('-')[2])),
                    max_date_allowed=date(int(str(date.today()).split('-')[0]), int(str(date.today()).split('-')[1]), int(str(date.today()).split('-')[2])),
                    date=date(int(str(date.today()).split('-')[0]), int(str(date.today()).split('-')[1]), int(str(date.today()).split('-')[2])), style={'margin': 20, 'text-align':'left'}
                ),

                # dbc.Button("Add Selection", id="btn_add_selection", className="me-1", style={"margin": 10}),
    
            ], xs=12, sm=12, md=12, lg=12, xl=12,
                ),

                    ], style={"marginBottom": 20}, justify='center'),

            dbc.Row([
                dbc.Col(
                    [
                    
                    html.Label('Select Participant ID: '),
                    dcc.Dropdown(
                        id='par-id',
                        options=[{'label':x, 'value': x} for x in par_ids],
                        multi=False,
                        value='',
                        searchable=False,
                        disabled=False
                    ),

            ], xs=12, sm=12, md=5, lg=5, xl=5,
                        style={"marginLeft": 5},
                    ),

                    dbc.Col(
                    [
                    
                    html.Label('Select Procedure: '),
                    dcc.Dropdown(
                        id='procedure-id',
                        options=[{'label':x, 'value': x} for x in procedure_ids],
                        multi=False,
                        value='',
                        searchable=False,
                        disabled=False
                    ),

            ], xs=12, sm=12, md=5, lg=5, xl=5,
                        style={"marginLeft": 5},
                    ),

                    ], style={"marginBottom": 20}, justify='center'),

        ],  style={"marginBottom": 30}),
    ], title="1. Select assessment date, participant ID and procedure",), ],start_collapsed=True , style={"margin": 30}),

    ### Table A
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Neck position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/1. Neck posture.PNG', height=200, width=400)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
                    #     dbc.Col(
                    #         [
                    #             html.Label('Neck score:'),
                    # ], xs=12, sm=12, md=3, lg=3, xl=3,
                    #         ),
                        dbc.Col(
                            [
                                html.Label('Neck score:'),
                                dcc.Dropdown(
                                    id='neck-score',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 1: Locate the neck position",), ],start_collapsed=True , style={"margin": 10}),

            ### Trunk position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/2. Trunk Posture.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
                    #     dbc.Col(
                    #         [
                    #             html.Label('Neck score:'),
                    # ], xs=12, sm=12, md=3, lg=3, xl=3,
                    #         ),
                        dbc.Col(
                            [
                                html.Label('Trunk Posture score:'),
                                dcc.Dropdown(
                                    id='trunk-posture-score',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 2: Locate the trunk position",), ],start_collapsed=True , style={"margin": 10}),

            ### Leg position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/3. Leg posture.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
                    #     dbc.Col(
                    #         [
                    #             html.Label('Neck score:'),
                    # ], xs=12, sm=12, md=3, lg=3, xl=3,
                    #         ),
                        dbc.Col(
                            [
                                html.Label('Leg Posture score:'),
                                dcc.Dropdown(
                                    id='leg-posture-score',
                                    options=[{'label':x, 'value': x} for x in leg_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 3: Locate the leg position",), ],start_collapsed=True , style={"margin": 10}),

            ### Force adjusting
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/5. Add force or load score.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
                    #     dbc.Col(
                    #         [
                    #             html.Label('Neck score:'),
                    # ], xs=12, sm=12, md=3, lg=3, xl=3,
                    #         ),
                        dbc.Col(
                            [
                                html.Label('Add force or load score:'),
                                dcc.Dropdown(
                                    id='force-load-score',
                                    options=[{'label':x, 'value': x} for x in force_load_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 5: Add force/ load score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            dbc.Button(
                "View total score", id="fade-button-a", className="mb-3", n_clicks=0
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(children=[
                        html.P(
                            "The score for section A, based on the REBA table, and steps 1-3 is: 0", id = "table-a-out-one", className="card-text-sec-a"
                        ),
                        html.P(
                            "The total score for section A with the force/load score, is: 0", id="table-a-out-two", className="card-text-sec-ab"
                        )]
                    )
                ),
                id="fade-a",
                is_in=False,
                appear=False,
            ),

        ],  style={"marginBottom": 30}),
    ], title="2. Section A: Neck, Trunk and Leg",), ],start_collapsed=True , style={"margin": 30}),



    # dbc.Accordion([ dbc.AccordionItem([

    #     dbc.Row([
    #             dbc.Col(
    #                 [
    #                     html.Label('Select Procedure: '),
    #         ], xs=12, sm=12, md=3, lg=3, xl=3,
    #                 ),
    #             dbc.Col(
    #                 [
    #                     html.Label('Select Procedure: '),
    #         ], xs=12, sm=12, md=3, lg=3, xl=3,
    #                 ),
    #             dbc.Col(
    #                 [
    #                     html.Label('Select Procedure: '),
    #         ], xs=12, sm=12, md=3, lg=3, xl=3,
    #                 ),

    #         ], style={"marginBottom": 20}, justify='center'),

    # ], title="sample",), ],start_collapsed=True , style={"margin": 30}),


    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg')),


    
])

####template
# dbc.Accordion([ dbc.AccordionItem([

#                 dbc.Row([
#                         dbc.Col(
#                             [
#                                 html.Img(src='assets/images/test_img.jpg', height=100, width=100)
#                     ], xs=12, sm=12, md=7, lg=7, xl=7,
#                             ),
#                     #     dbc.Col(
#                     #         [
#                     #             html.Label('Neck score:'),
#                     # ], xs=12, sm=12, md=3, lg=3, xl=3,
#                     #         ),
#                         dbc.Col(
#                             [
#                                 html.Label('xx:'),
#                                 dcc.Dropdown(
#                                     id='xx',
#                                     options=[{'label':x, 'value': x} for x in procedure_ids],
#                                     multi=False,
#                                     value='',
#                                     searchable=False,
#                                     disabled=False
#                                 ),

#                     ], xs=12, sm=12, md=5, lg=5, xl=5,
#                             ),

#                 ], style={"marginBottom": 20}, justify='center'),

#             ], title="Step 1: Locate the neck position",), ],start_collapsed=True , style={"margin": 30}),



@callback(
    Output("fade-a", "is_in"),
    [Input("fade-button-a", "n_clicks")],
    [State("fade-a", "is_in")],
)
def toggle_fade_a(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

# ************************  callback Table A *****************************
@callback(
    [Output("table-a-out-one", "children"),
     Output("table-a-out-two", "children")], 
    [Input("neck-score", "value"),
     Input("trunk-posture-score", "value"),
     Input("leg-posture-score", "value"),
     Input("force-load-score", "value"),
     Input("fade-button-a", "n_clicks")],
    prevent_initial_call=True,
)
def table_a(neck_score, trunk_posture_score, leg_posture_score, force_load_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if neck_score in [None]:
        return no_update

    if trunk_posture_score in [None]:
        return no_update
    
    if leg_posture_score in [None]:
        return no_update
    
    if force_load_score in [None]:
        return no_update
    
    str_one = "The score for section A, based on the REBA table, and steps 1-3, is: "
    str_two = "The total score for section A, after adding the force/load score, is: "

    assets_table_a = 'assets/data/reba_tableA.json'

    with open(assets_table_a) as f:
        reba_tableA_dict = json.load(f)
    
    if trigger_id == 'fade-button-a':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if len(neck_score) > 0 and len(trunk_posture_score) > 0 and len(leg_posture_score) > 0 and len(force_load_score) > 0:
            print(reba_tableA_dict)
            print(neck_score[0], trunk_posture_score[0], leg_posture_score[0], force_load_score[0])

            lookup_ky = f'{str(neck_score[0])}{"_"}{str(trunk_posture_score[0])}{"_"}{str(leg_posture_score[0])}'
            final_score = int(reba_tableA_dict.get(lookup_ky, "0")) + int(force_load_score[0])
            return f'{str_one}{reba_tableA_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""

## ************************  callback example *****************************
# @callback(
#     Output("some-id", "options"), 
#     [Input("some-other-id", "value")],
#     prevent_initial_call=True,
# )
# def some_function(id):

#     trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
#     if trigger_id == "some-other-id":
#         print("some logic here")    

#         return [{'label':x, 'value':x} for x in ["tmp"]]

#     return [{'label':x, 'value':x} for x in ["tmp"]]
