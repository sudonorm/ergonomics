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
neck_score_ids = ['1', '2']
neck_score_ids_adjust = ['0', '1']
trunk_posture_score_ids = ['1', '2', '3', '4']
trunk_posture_ids_adjust = ['0', '1']
leg_posture_score_ids = ['1', '2']
leg_posture_score_adjust = ['0', '1', '2']
force_load_score_ids = ['0', '1', '2']
force_load_score_adjust = ['0', '1']

score_ids_adjust = ['0', '1']
score_ids_adjust_neg = ['0', '1']

upper_arm_pos_ids = ['1', '2', '3', '4']
lower_arm_pos_ids = ['1', '2']
wrist_pos_ids = ['1', '2']
wrist_pos_adjust = ['0', '1']

coupling_score_ids = ['0', '1', '2', '3']

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

output_template_reba = {'Participant_ID': '',
 'Assessment': '',
 'Procedure_and_Mouth_Quadrant': '',
 'Variable_ID': '',
 'Step_1:_Locate_the_neck_position': '',
 'If_neck_is_twisted': '',
 'If_neck_is_side_bending': '',
 'Neck_score': '',
 'Step_2:_Locate_trunk_position': '',
 'If_trunk_is_twisted': '',
 'If_trunk_is_side_bending': '',
 'Trunk_Posture_score': '',
 'Step_3:_Legs': '',
 'step_3_Adjust': '',
 'Leg_Score': '',
 'Step_4:_Look-up_Posture_Score_in_Table_A._Posture_Score_A': '',
 'Step_5:_Add_fore_load_score': '',
 'If_shock_or_rapid_build_up_of_force': '',
 'Force_Load_score': '',
 'Step_6:_Score_A,_Find_Row_in_Table_C_(Steps_4+5_scores)._Score_A': '',
 'Step_7:_Locate_upper_arm_position': '',
 'If_shoulder_is_raised': '',
 'If_upper_arm_is_abducted': '',
 'If_arm_is_supported_or_person_is_leaning': '',
 'Upper_arm_score': '',
 'Step_8:_Locate_lower_arm_position': '',
 'Step_9:_Locate_wrist_posture': '',
 'If_wrist_is_bent_from_midline_or_twisted': '',
 'Wrist_posture_score': '',
 'Step_10:_Look-up_posture_score_in_Table_B._Postue_Score_B': '',
 'Step_11:Add_coupling_score_Coupling_Score': '',
 'Step_12:_Score_B,_Find_column_in_Table_C._Score_B': '',
 'Table_C_Score': '',
 '1_or_more_body_parts_are_held_for_longer_than_1_minute_(static)': '',
 'Repeat_small_range_actions_more_than_4X_per_minute)': '',
 'Action_causes_rapid_large_range_changes_in_postures_or_unstable_base': '',
 'Activity_score': '',
 'REBA_Score': '',
 'REBA_Score_conclusion': ''}

badge_a = dbc.Button(
    [
        "Table A score: ",
        dbc.Badge(children=["4"],id="badge-a", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

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

    ### Table A: neck, trunk, leg
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

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Neck score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-neck-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("0-20° (flexion) = +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("20°+ (flexion/forward motion)= +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("In extension (backward)= +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-neck-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='neck-score',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 1a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the neck twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='neck-twisted',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the neck side bending? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='neck-bending',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids_adjust],
                                    multi=False,
                                    value='0',
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
                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Trunk Posture score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-trunk-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("0° = +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("0° - 20° (in extension i.e. backward neck motion): +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("0° - 20° (flexion i.e. forward neck motion):   +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("20° - 60° (flexion): +3", 
                                                            
                                                            className="card-text"),
                                                        html.P(">20° (in extension or backward): +3", 
                                                            
                                                            className="card-text"),
                                                        html.P("60°+ (flexion): +4", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-trunk-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='trunk-posture-score',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 2a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the trunk twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='trunk-twisted',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the trunk side bending? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='trunk-bending',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_ids_adjust],
                                    multi=False,
                                    value='0',
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
                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Leg Posture score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-leg-pos-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("Both legs down: +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("One leg raised: +2  ", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-leg-pos-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='leg-posture-score',
                                    options=[{'label':x, 'value': x} for x in leg_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 3a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Adjust legs score: select 1 for 30-60° and 2 for 60°+', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='leg-posture-adjust',
                                    options=[{'label':x, 'value': x} for x in leg_posture_score_adjust],
                                    multi=False,
                                    value='0',
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

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Add force or load score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-force-load-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("If load is <11 Ibs: +0", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load is 11 to 22 Ibs,: +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load is >22 Ibs.: +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-force-load-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='force-load-score',
                                    options=[{'label':x, 'value': x} for x in force_load_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 5a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Adjust if shock or rapid build up of force: add +1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='force-adjust',
                                    options=[{'label':x, 'value': x} for x in force_load_score_adjust],
                                    multi=False,
                                    value='0',
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


    ### Table B: arm and wrist
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Upper arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/7. Upper arm position.PNG', height=200, width=400)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
   
                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Upper arm position:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-upper-arm-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("20-20°: +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("20° (in extension i.e. downward and backward): Add +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("20-45° (flexion): +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("45-90° (flexion):  +3", 
                                                            
                                                            className="card-text"),
                                                        html.P("90°+: +4", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-upper-arm-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='upper-arm-score',
                                    options=[{'label':x, 'value': x} for x in upper_arm_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 7a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the shoulder raised? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='shoulder-raised',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the upper arm abducted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='upper-arm-abducted',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the arm supported or is the person leaning? If yes, select 1 (this will be subtracted)', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='upper-arm-supported',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust_neg],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 7: Locate upper arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Lower arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/8. Lower arm position.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Lower arm score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-lower-arm-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("60-100°: Add +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("0-60°: +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("100°+ (in the upward direction): +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-lower-arm-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='lower-arm-score',
                                    options=[{'label':x, 'value': x} for x in lower_arm_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 8: Locate lower arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Wrist position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/9. Wrist score.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Wrist score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-wrist-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("15-15°: +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("15°+ (in the upward position): +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("15°+ (in the downward position): +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-wrist-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='wrist-score',
                                    options=[{'label':x, 'value': x} for x in wrist_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 9a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the wrist bent from the midline or twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='wrist-adjust',
                                    options=[{'label':x, 'value': x} for x in wrist_pos_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 9: Locate wrist posture",), ],start_collapsed=True , style={"margin": 10}),


            ### Add coupling score
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/11. Coupling score.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Select coupling score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-coupling-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("Well fitting handle and mid rsnge powet grip, good: +0", 
                                                            
                                                            className="card-text"),
                                                        html.P("Acceptable but not ideal hand hold or coupling acceptable with another body part, fair: +1 ", 
                                                            
                                                            className="card-text"),
                                                        html.P("Hand hold not acceptable but possible, poor: +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("Unacceptable: +3", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-coupling-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='coupling-score',
                                    options=[{'label':x, 'value': x} for x in coupling_score_ids],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 11: Add coupling score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            dbc.Button(
                "View total score", id="fade-button-b", className="mb-3", n_clicks=0
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(children=[
                        html.P(
                            "The score for section B, based on the REBA table, and steps 7-11 is: 0", id = "table-b-out-one", className="card-text-sec-a"
                        ),
                        html.P(
                            "The total score for section B with the coupling score, is: 0", id="table-b-out-two", className="card-text-sec-ab"
                        )]
                    )
                ),
                id="fade-b",
                is_in=False,
                appear=False,
            ),

        ],  style={"marginBottom": 30}),
    ], title="3. Section B: Arm and Wrist",), ],start_collapsed=True , style={"margin": 30}),


    ### Table C: total acore
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Table C lookup
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/12b. Table C score.PNG', height=300, width=600)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
   
                        dbc.Col(
                            [


                                dbc.Row([

                                    dbc.Col(
                            [
                                
                                dbc.Button(
                                        [
                                            "Table A score: ",
                                            dbc.Badge(children=[""],id="badge-a", color="light", text_color="primary", className="ms-1"),
                                        ],
                                        color="primary", style={"marginTop": 20}
                                    ),

                            ], xs=12, sm=12, md=6, lg=6, xl=6, className="d-grid",
                            ),
                            dbc.Col(
                            [

                                dbc.Button(
                                        [
                                            "Table B score: ",
                                            dbc.Badge(children=[""],id="badge-b", color="light", text_color="primary", className="ms-1"),
                                        ],
                                        color="primary", style={"marginTop": 20}
                                    ),

                            ], xs=12, sm=12, md=6, lg=6, xl=6, className="d-grid",
                            ),

                                ]),

                            dbc.Row([

                                dbc.Col(
                            [

                                dbc.Button(
                                        [
                                            "Table C score: ",
                                            dbc.Badge(children=[""],id="badge-c", color="light", text_color="primary", className="ms-1"),
                                        ],
                                        color="primary", style={"marginTop": 20}
                                    ),

                                ], xs=12, sm=12, md=12, lg=12, xl=12, className="d-grid",
                            ),

                                ]),
\
                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Table C score",), ],start_collapsed=True , style={"margin": 10}),


            ### Upper arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/13. Activity score.PNG', height=200, width=600)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),
   
                        dbc.Col(
                            [
    
                                html.Label('1 or more body parts are held for longer than 1 minute (static). If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='activity-score-one',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Repeat small range actions more than 4X per minute)', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='activity-score-two',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Action causes rapid large range changes in postures or unstable base', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='activity-score-three',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust_neg],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 13: Activity Score",), ],start_collapsed=True, style={"margin": 10}),


            dbc.Card(
                dbc.CardBody(children=[
                    html.P(
                        "The total Reba score, based on Table C and the Activity Score, is: 0", id = "reba-out", className="card-text-sec-a"
                    ),
                    ]
                )
                , style={"margin": 10}),

        ],  style={"marginBottom": 30}),
    ], title="4. Section C,  Activity Score, and Reba Score",), ],start_collapsed=True , style={"margin": 30}),

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


    # html.Div(children='My First App with Data and a Graph'),
    # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    # dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg')),


    
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
    Output("collapse-neck-score", "is_open"),
    [Input("collapse-button-neck-score", "n_clicks")],
    [State("collapse-neck-score", "is_open")],
)
def toggle_collapse_neck_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-trunk-score", "is_open"),
    [Input("collapse-button-trunk-score", "n_clicks")],
    [State("collapse-trunk-score", "is_open")],
)
def toggle_collapse_trunk_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-leg-pos-score", "is_open"),
    [Input("collapse-button-leg-pos-score", "n_clicks")],
    [State("collapse-leg-pos-score", "is_open")],
)
def toggle_collapse_leg_pos_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-force-load-score", "is_open"),
    [Input("collapse-button-force-load-score", "n_clicks")],
    [State("collapse-force-load-score", "is_open")],
)
def toggle_collapse_force_load_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-upper-arm-score", "is_open"),
    [Input("collapse-button-upper-arm-score", "n_clicks")],
    [State("collapse-upper-arm-score", "is_open")],
)
def toggle_collapse_upper_arm_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-lower-arm-score", "is_open"),
    [Input("collapse-button-lower-arm-score", "n_clicks")],
    [State("collapse-lower-arm-score", "is_open")],
)
def toggle_collapse_lower_arm_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-wrist-score", "is_open"),
    [Input("collapse-button-wrist-score", "n_clicks")],
    [State("collapse-wrist-score", "is_open")],
)
def toggle_collapse_wrist_score(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-coupling-score", "is_open"),
    [Input("collapse-button-coupling-score", "n_clicks")],
    [State("collapse-coupling-score", "is_open")],
)
def toggle_collapse_coupling_score(n, is_open):
    if n:
        return not is_open
    return is_open

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

@callback(
    Output("fade-b", "is_in"),
    [Input("fade-button-b", "n_clicks")],
    [State("fade-b", "is_in")],
)
def toggle_fade_b(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

###### disable neck dropdown #######
@callback(
    [Output("neck-twisted", "disabled"),
     Output("neck-bending", "disabled"),
     Output("neck-twisted", "value"),
    Output("neck-bending", "value")],
    [Input("neck-twisted", "value"), Input("neck-bending", "value")],
)
def neck_adjust(nck_twisted, nck_bending):

    if nck_twisted in [None, ''] or nck_bending in [None, '']:
        return False, False, '0', '0'

    if nck_twisted[0] in ['1', 1]:
        return False, True, '1', '0'
    elif nck_bending[0] in ['1', 1]:
        return True, False, '0', '1'
    else:
        return False, False, '0', '0'

###### disable trunk dropdown #######
@callback(
    [Output("trunk-twisted", "disabled"),
     Output("trunk-bending", "disabled"),
     Output("trunk-twisted", "value"),
    Output("trunk-bending", "value")],
    [Input("trunk-twisted", "value"), Input("trunk-bending", "value")],
)
def trunk_adjust(trnk_twisted, trnk_bending):

    if trnk_twisted in [None, ''] or trnk_bending in [None, '']:
        return False, False, '0', '0'

    if trnk_twisted[0] in ['1', 1]:
        return False, True, '1', '0'
    elif trnk_bending[0] in ['1', 1]:
        return True, False, '0', '1'
    else:
        return False, False, '0', '0'
    
# ************************  callback Table A *****************************
@callback(
    [Output("table-a-out-one", "children"),
     Output("table-a-out-two", "children"),], 
    [Input("neck-score", "value"),
     Input("neck-twisted", "value"),
    Input("neck-bending", "value"),
     Input("trunk-posture-score", "value"),
     Input("trunk-twisted", "value"),
    Input("trunk-bending", "value"),
     Input("leg-posture-score", "value"),
    Input("leg-posture-adjust", "value"),
     Input("force-load-score", "value"),
    Input("force-adjust", "value"),
     Input("fade-button-a", "n_clicks")],
    prevent_initial_call=True,
)
def table_a(neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, leg_posture_adjust, force_load_score, force_adjust, n_clicks_show_res):

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

    assets_table_a = 'assets/data/reba_tableA.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_a) as f:
        reba_tableA_dict = json.load(f)
    
    if trigger_id == 'fade-button-a':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if len(neck_score) > 0 and len(trunk_posture_score) > 0 and len(leg_posture_score) > 0 and len(force_load_score) > 0:
            print(reba_tableA_dict)
            print(neck_score[0], trunk_posture_score[0], leg_posture_score[0], force_load_score[0])

            nck_scr = int(neck_score[0]) + int(neck_twisted[0]) + int(neck_bending[0])
            trnck_scr = int(trunk_posture_score[0]) + int(trunk_twisted[0]) + int(trunk_bending[0])
            leg_scr = int(leg_posture_score[0]) + int(leg_posture_adjust[0])
            frce_scr = int(force_load_score[0]) + int(force_adjust[0])
            

            print(nck_scr, trnck_scr, leg_scr, frce_scr)

            lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
            final_score = int(reba_tableA_dict.get(lookup_ky, "0")) + frce_scr
            return f'{str_one}{reba_tableA_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""


# ************************  callback Table B *****************************
@callback(
    [Output("table-b-out-one", "children"),
     Output("table-b-out-two", "children"),], 
    [Input("upper-arm-score", "value"),
     Input("shoulder-raised", "value"),
    Input("upper-arm-abducted", "value"),
     Input("upper-arm-supported", "value"),
     Input("lower-arm-score", "value"),
    Input("wrist-score", "value"),
     Input("wrist-adjust", "value"),
    Input("coupling-score", "value"),
     Input("fade-button-b", "n_clicks")],
    prevent_initial_call=True,
)
def table_b(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, wrist_score, wrist_adjust, coupling_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if upper_arm_score in [None]:
        return no_update

    if lower_arm_score in [None]:
        return no_update
    
    if wrist_score in [None]:
        return no_update
    
    str_one = "The score for section B, based on the REBA table, and steps 7-11, is: "
    str_two = "The total score for section B, after adding the coupling score, is: "

    assets_table_b = 'assets/data/reba_tableB.json' ###UpperArmScore_1|LowerArm_1|Wrist_1

    with open(assets_table_b) as f:
        reba_tableB_dict = json.load(f)
    
    if trigger_id == 'fade-button-b':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if len(upper_arm_score) > 0 and len(lower_arm_score) > 0 and len(wrist_score) > 0 and len(coupling_score) > 0:
            print(reba_tableB_dict)
            print(upper_arm_score[0], lower_arm_score[0], wrist_score[0], coupling_score[0])

            upr_arm_scr = int(upper_arm_score[0]) + int(shoulder_raised[0]) + int(upper_arm_abducted[0]) - int(upper_arm_supported[0])
            lwr_arm_scr = int(lower_arm_score[0])
            wrst_scr = int(wrist_score[0]) + int(wrist_adjust[0])
            coup_scr = int(coupling_score[0])
            

            print(upr_arm_scr, lwr_arm_scr, wrst_scr, coup_scr)

            lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}'
            final_score = int(reba_tableB_dict.get(lookup_ky, "0")) + coup_scr
            return f'{str_one}{reba_tableB_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""

# ************************  callback Table B *****************************
@callback(
    [Output("badge-a", "children"),
     Output("badge-b", "children"),
     Output("badge-c", "children"),
     Output("reba-out", "children")], 
    [Input("upper-arm-score", "value"),
     Input("shoulder-raised", "value"),
    Input("upper-arm-abducted", "value"),
     Input("upper-arm-supported", "value"),
     Input("lower-arm-score", "value"),
    Input("wrist-score", "value"),
     Input("wrist-adjust", "value"),
    Input("coupling-score", "value"),
     Input("neck-score", "value"),
     Input("neck-twisted", "value"),
    Input("neck-bending", "value"),
     Input("trunk-posture-score", "value"),
     Input("trunk-twisted", "value"),
    Input("trunk-bending", "value"),
     Input("leg-posture-score", "value"),
    Input("leg-posture-adjust", "value"),
     Input("force-load-score", "value"),
    Input("force-adjust", "value"),
    Input("activity-score-one", "value"),
     Input("activity-score-two", "value"),
    Input("activity-score-three", "value")],
    # prevent_initial_call=True,
)
def table_c(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, wrist_score, wrist_adjust, coupling_score, neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, leg_posture_adjust, force_load_score, force_adjust, act_scr_one, act_scr_two, act_scr_three):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if neck_score in [None]:
        return no_update

    if trunk_posture_score in [None]:
        return no_update
    
    if leg_posture_score in [None]:
        return no_update
    
    if force_load_score in [None]:
        return no_update
    
    if upper_arm_score in [None]:
        return no_update

    if lower_arm_score in [None]:
        return no_update
    
    if wrist_score in [None]:
        return no_update
    
    str_one = "The total Reba score, based on Table C and the Activity Score, is: "

    assets_table_a = 'assets/data/reba_tableA.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_a) as f:
        reba_tableA_dict = json.load(f)

    assets_table_b = 'assets/data/reba_tableB.json' ### UpperArmScore_1|LowerArm_1|Wrist_1

    with open(assets_table_b) as f:
        reba_tableB_dict = json.load(f)
    
    assets_table_c = 'assets/data/reba_tableC.json' ### ScoreA_1|ScoreB_1

    with open(assets_table_c) as f:
        reba_tableC_dict = json.load(f)

    if len(upper_arm_score) > 0 and len(lower_arm_score) > 0 and len(wrist_score) > 0 and len(coupling_score) > 0 and len(neck_score) > 0 and len(trunk_posture_score) > 0 and len(leg_posture_score) > 0 and len(force_load_score) > 0:
        nck_scr = int(neck_score[0]) + int(neck_twisted[0]) + int(neck_bending[0])
        trnck_scr = int(trunk_posture_score[0]) + int(trunk_twisted[0]) + int(trunk_bending[0])
        leg_scr = int(leg_posture_score[0]) + int(leg_posture_adjust[0])
        frce_scr = int(force_load_score[0]) + int(force_adjust[0])
        lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
        final_score_a = int(reba_tableA_dict.get(lookup_ky, "0")) + frce_scr
        
        upr_arm_scr = int(upper_arm_score[0]) + int(shoulder_raised[0]) + int(upper_arm_abducted[0]) - int(upper_arm_supported[0])
        lwr_arm_scr = int(lower_arm_score[0])
        wrst_scr = int(wrist_score[0]) + int(wrist_adjust[0])
        coup_scr = int(coupling_score[0])
        lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}'
        final_score_b = int(reba_tableB_dict.get(lookup_ky, "0")) + coup_scr

        lookup_ky = f'{str(final_score_a)}{"_"}{str(final_score_b)}'
        final_score_c = int(reba_tableC_dict.get(lookup_ky, "0"))
        

        reba_score = final_score_c + int(act_scr_one[0]) + int(act_scr_two[0]) + int(act_scr_three[0])

        return [str(final_score_a)], [str(final_score_b)], [str(final_score_c)], f'{str_one}{str(reba_score)}'
    
    else:
        return no_update

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
