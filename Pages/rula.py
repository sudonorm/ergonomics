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
sys.path.append(r"/Users/ayo/Documents/repos/ergonomics")
from utils import drop_box, send_mail
from dotenv import load_dotenv
import dropbox

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS")
SENDER_EMAIL = os.environ.get("EMAIL_USERNAME")
SENDER_PASS = os.environ.get("EMAIL_PASSWORD")
PORT_NUMBER = os.environ.get("SMTP_PORT")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")

dbx_cls = drop_box.DBXUpDown()
    
email = send_mail.EmailSender()

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

par_ids = ['PAR01', 'PAR02', 'PAR03', 'PAR04', 'PAR05', 'PAR06', 'PAR07', 'PAR08', 'PAR09', 'PAR10', 'test1', 'test2', 'test3']
neck_score_ids = ['1', '2', '3', '4']
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
wrist_pos_ids = ['1', '2', '3']
wrist_pos_adjust = ['0', '1']
wrist_twist_pos_ids = ['1', '2']

force_score_ids = ['0', '1', '2', '3']
muscle_score_ids = ['0', '1']

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

output_template_rula = {'Participant_ID': '',
 'Assessment': '',
 'Procedure_and_Mouth_Quadrant': '',
 'Variable_ID': '',
 'Step_1:_Locate_upper_arm_position': '',
 'If_shoulder_is_raised': '',
 'If_upper_arm_is_abducted': '',
 'If_arm_is_supported_or_person_is_leaning': '',
 'Step_1_score': '',
 'Step_2:_Locate_lower_arm_position': '',
 'If_either_arm_is_working_across_midline_or_out_to_side_of_body': '',
 'Step_2_score': '',
 'Step_3:_Locate_wrist_position': '',
 'If_wrist_is_bent_from_midline': '',
 'Wrist_score': '',
 'Step_4:_Wrist_twist._Wrist_Twist_Score': '',
 'Step_5:_Look_Posture_Score_in_Table_A': '',
 'Step_6:_Add_muscle_use_score': '',
 'Step_7:_Add_force_load_score': '',
 'Step_8': '',
 'Step_9:_Locate_neck_position': '',
 'If_neck_is_twisted': '',
 'If_neck_is_side_bending': '',
 'Neck_score': '',
 'Step_10:_Locate_trunk_posture': '',
 'If_trunk_is_twisted': '',
 'If_trunk_is_side_bending': '',
 'Trunk_score': '',
 'Step_11:_Legs._Leg_score': '',
 'Step_12:_Look-up_posture_score_in_Table_B_Posture_B_Score': '',
 'Step_13:_Add_Muscle_Use_Score': '',
 'Step_14:_Add_Force_Lead_Score': '',
 'Step_15:_Find_Column_in_Table_C_Neck,_Trunk,_Leg_Score': '',
 'RULA_Score': '',
 'Scoring': ''}

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
                    id='date-change-rula',
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
                        id='par-id-rula',
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
                        id='procedure-id-rula',
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

    ### Table A: Arm and Wrist Analysis
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Upper arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/1. Locate Upper Arm Position.PNG', height=200, width=400)
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
                                                    id="collapse-button-upper-arm-score-rula",
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
                                                    id="collapse-upper-arm-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='upper-arm-score-rula',
                                    options=[{'label':x, 'value': x} for x in upper_arm_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 1a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the shoulder raised? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='shoulder-raised-rula',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the upper arm abducted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='upper-arm-abducted-rula',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the arm supported or is the person leaning? If yes, select 1 (this will be subtracted)', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='upper-arm-supported-rula',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 1: Locate upper arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Lower arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/2. Lower Arm Score.PNG', height=200, width=450)
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
                                                    id="collapse-button-lower-arm-score-rula",
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
                                                    id="collapse-lower-arm-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='lower-arm-score-rula',
                                    options=[{'label':x, 'value': x} for x in lower_arm_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 2a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is either arm working across the midline or out to side of body? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='lower-arm-moving-rula',
                                    options=[{'label':x, 'value': x} for x in score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 2: Locate lower arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Wrist position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/3. Wrist position.PNG', height=200, width=450)
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
                                                    id="collapse-button-wrist-score-rula",
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
                                                    id="collapse-wrist-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='wrist-score-rula',
                                    options=[{'label':x, 'value': x} for x in wrist_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 3a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the wrist bent from the midline or twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='wrist-adjust-rula',
                                    options=[{'label':x, 'value': x} for x in wrist_pos_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 3: Locate wrist posture",), ],start_collapsed=True , style={"margin": 10}),

            ### Wrist twist position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/4. Wrist twist.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Wrist Twist score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-wrist-twist-score-rula",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("If wrist is twisted in mid-range: +1 ", 
                                                            
                                                            className="card-text"),
                                                        html.P("If wrist is at or near end of range: +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-wrist-twist-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='wrist-twist-score-rula',
                                    options=[{'label':x, 'value': x} for x in wrist_twist_pos_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 4: Wrist twist score",), ],start_collapsed=True , style={"margin": 10}),

            ### Add muscle use score
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/6. Add muscle use score.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Select muscle use score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-muscle-use-score",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("If posture is mainly static (i.e. held >10 minutes), or if action repeated occurs 4X per minute: Add +1", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-muscle-use-score",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='muscle-use-score',
                                    options=[{'label':x, 'value': x} for x in muscle_score_ids],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 6: Add muscle use score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            ### Force adjusting
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/7. Add force or load score.PNG', height=200, width=450)
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
                                                    id="collapse-button-force-load-score-rula",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("If load <4.4 Ibs. (intermittent): +0", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load 4.4 to 22 Ibs. (intermittent): +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load 4.44 to 22 Ibs. (static or repeated): +2", 
                                                            
                                                            className="card-text"),
                                                            
                                                        html.P("If more than 22 Ibs. or repeated or shocks: +3", 
                                                            
                                                            className="card-text"),
                                                        ])),
                                                    id="collapse-force-load-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='force-load-score-rula',
                                    options=[{'label':x, 'value': x} for x in force_score_ids],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 7: Add force/ load score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            dbc.Button(
                "View total score", id="fade-button-a-rula", className="mb-3", n_clicks=0
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(children=[
                        html.P(
                            "The score for section A, based on the RULA table, and steps 1-7 is: 0", id = "table-a-out-one-rula", className="card-text-sec-a"
                        ),
                        html.P(
                            "The total score for section A with the muscle and force/load score, is: 0", id="table-a-out-two-rula", className="card-text-sec-ab"
                        )]
                    )
                ),
                id="fade-a-rula",
                is_in=False,
                appear=False,
            ),

        ],  style={"marginBottom": 30}),
    ], title="2. Section A: Arm and Wrist Analysis",), ],start_collapsed=True , style={"margin": 30}),

    ### Table B: neck, trunk, leg
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Neck position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/9. Neck position.PNG', height=200, width=400)
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
                                                    id="collapse-button-neck-score-rula",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("0-10° (flexion) = +1", 
                                                            
                                                            className="card-text"),

                                                        html.P("10-20° (flexion) = +2", 
                                                            
                                                            className="card-text"),

                                                        html.P("20°+ (flexion)= +3", 
                                                            
                                                            className="card-text"),
                                                        html.P("In extension (neck bent backward)= +4", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-neck-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='neck-score-rula',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 9a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the neck twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='neck-twisted-rula',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the neck side bending? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='neck-bending-rula',
                                    options=[{'label':x, 'value': x} for x in neck_score_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 9: Locate the neck position",), ],start_collapsed=True , style={"margin": 10}),

            ### Trunk position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/10. Trunk position.PNG', height=200, width=450)
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
                                                    id="collapse-button-trunk-score-rula",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("0° = +1", 
                                                            
                                                            className="card-text"),

                                                        html.P("0° - 20° (flexion i.e. forward neck motion):   +2", 
                                                            
                                                            className="card-text"),
                                                        html.P("20° - 60° (flexion): +3", 
                                                            
                                                            className="card-text"),

                                                        html.P("60°+ (flexion): +4", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-trunk-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='trunk-posture-score-rula',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 10a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the trunk twisted? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='trunk-twisted-rula',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the trunk side bending? If yes, select 1', style={"marginTop": 20}),
                                dcc.Dropdown(
                                    id='trunk-bending-rula',
                                    options=[{'label':x, 'value': x} for x in trunk_posture_ids_adjust],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 10: Locate the trunk posture",), ],start_collapsed=True , style={"margin": 10}),

            ### Leg position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/11. Legs.PNG', height=200, width=450)
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
                                                    id="collapse-button-leg-pos-score-rula",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("If legs and feet are spotted: Add +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("If not: Add +2", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-leg-pos-score-rula",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='leg-posture-score-rula',
                                    options=[{'label':x, 'value': x} for x in leg_posture_score_ids],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 11: Leg score",), ],start_collapsed=True , style={"margin": 10}),

            ### Add muscle use score
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/13. Add muscle use score.PNG', height=200, width=450)
                    ], xs=12, sm=12, md=7, lg=7, xl=7,
                            ),

                        dbc.Col(
                            [
                                dbc.Row([
                                    dbc.Col([
                                        html.Label('Select muscle use score:'),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,
                                    ),
                                    dbc.Col([
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Open description",
                                                    id="collapse-button-muscle-use-score-13",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                  
                                                        html.P("If posture is mainly static (i.e. held >10 minutes), or if action repeated occurs 4X per minute: Add +1", 
                                                            
                                                            className="card-text"),
                                                        
                                                        ])),
                                                    id="collapse-muscle-use-score-13",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='muscle-use-score-13',
                                    options=[{'label':x, 'value': x} for x in muscle_score_ids],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 13: Add muscle use score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            ### Force adjusting
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/14. Add force or load score.PNG', height=200, width=450)
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
                                                    id="collapse-button-force-load-score-rula-14",
                                                    className="mb-3",
                                                    color="primary",
                                                    n_clicks=0,
                                                    size="sm"
                                                ),
                                                dbc.Collapse(
                                                    dbc.Card(dbc.CardBody([
                                                        html.P("If load <4.4 Ibs. (intermittent): +0", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load 4.4 to 22 Ibs. (intermittent): +1", 
                                                            
                                                            className="card-text"),
                                                        html.P("If load 4.44 to 22 Ibs. (static or repeated): +2", 
                                                            
                                                            className="card-text"),
                                                            
                                                        html.P("If more than 22 Ibs. or repeated or shocks: +3", 
                                                            
                                                            className="card-text"),
                                                        ])),
                                                    id="collapse-force-load-score-rula-14",
                                                    is_open=False,
                                                    style={"marginBottom": 20},
                                                ),
                                            ], className='d-grid',
                                        ),
                                        ], xs=12, sm=12, md=6, lg=6, xl=6
                                    ),
                                ]),

                                dcc.Dropdown(
                                    id='force-load-score-rula-14',
                                    options=[{'label':x, 'value': x} for x in force_score_ids],
                                    multi=False,
                                    value='0',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=5, lg=5, xl=5,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 14: Add force/ load score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            dbc.Button(
                "View total score", id="fade-button-b-rula", className="mb-3", n_clicks=0
            ),
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(children=[
                        html.P(
                            "The score for section B, based on the RULA table, and steps 9-11 is: 0", id = "table-b-out-one-rula", className="card-text-sec-a"
                        ),
                        # html.P(
                        #     "The total posture score for section B is: 0", id="table-b-out-two-rula", className="card-text-sec-ab"
                        # ),
                        html.P(
                            "The total neck, leg and trunk score for section B is: 0", id="table-b-out-two-rula", className="card-text-sec-ab"
                        )]
                    )
                ),
                id="fade-b-rula",
                is_in=False,
                appear=False,
            ),

        ],  style={"marginBottom": 30}),
    ], title="3. Section B: Neck, Trunk and Leg",), ],start_collapsed=True , style={"margin": 30}),


    ### Table C: total acore
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Table C lookup
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                        dbc.Col(
                            [
                                html.Img(src='assets/images/rula/Table C.PNG', height=300, width=600)
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
                                            dbc.Badge(children=[""],id="badge-a-rula", color="light", text_color="primary", className="ms-1"),
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
                                            dbc.Badge(children=[""],id="badge-b-rula", color="light", text_color="primary", className="ms-1"),
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
                                            dbc.Badge(children=[""],id="badge-c-rula", color="light", text_color="primary", className="ms-1"),
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

            dbc.Card(
                dbc.CardBody(children=[
                    html.P(
                        "The total Rula score, based on Table C, is: 0", id = "rula-out", className="card-text-sec-a"
                    ),
                    ]
                )
                , style={"margin": 10}),

        ],  style={"marginBottom": 30}),
    ], title="4. Section C: Rula Score",), ],start_collapsed=True , style={"margin": 30}),
  
])


@callback(
    Output("collapse-neck-score-rula", "is_open"),
    [Input("collapse-button-neck-score-rula", "n_clicks")],
    [State("collapse-neck-score-rula", "is_open")],
)
def toggle_collapse_neck_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-trunk-score-rula", "is_open"),
    [Input("collapse-button-trunk-score-rula", "n_clicks")],
    [State("collapse-trunk-score-rula", "is_open")],
)
def toggle_collapse_trunk_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-leg-pos-score-rula", "is_open"),
    [Input("collapse-button-leg-pos-score-rula", "n_clicks")],
    [State("collapse-leg-pos-score-rula", "is_open")],
)
def toggle_collapse_leg_pos_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-muscle-use-score", "is_open"),
    [Input("collapse-button-muscle-use-score", "n_clicks")],
    [State("collapse-muscle-use-score", "is_open")],
)
def toggle_collapse_muscle_use_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-muscle-use-score-13", "is_open"),
    [Input("collapse-button-muscle-use-score-13", "n_clicks")],
    [State("collapse-muscle-use-score-13", "is_open")],
)
def toggle_collapse_muscle_use_score_rula_thir(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-force-load-score-rula", "is_open"),
    [Input("collapse-button-force-load-score-rula", "n_clicks")],
    [State("collapse-force-load-score-rula", "is_open")],
)
def toggle_collapse_force_load_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-force-load-score-rula-14", "is_open"),
    [Input("collapse-button-force-load-score-rula-14", "n_clicks")],
    [State("collapse-force-load-score-rula-14", "is_open")],
)
def toggle_collapse_force_load_score_rula_four(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-upper-arm-score-rula", "is_open"),
    [Input("collapse-button-upper-arm-score-rula", "n_clicks")],
    [State("collapse-upper-arm-score-rula", "is_open")],
)
def toggle_collapse_upper_arm_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-lower-arm-score-rula", "is_open"),
    [Input("collapse-button-lower-arm-score-rula", "n_clicks")],
    [State("collapse-lower-arm-score-rula", "is_open")],
)
def toggle_collapse_lower_arm_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("collapse-wrist-score-rula", "is_open"),
    [Input("collapse-button-wrist-score-rula", "n_clicks")],
    [State("collapse-wrist-score-rula", "is_open")],
)
def toggle_collapse_wrist_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output('collapse-wrist-twist-score-rula', "is_open"),
    [Input('collapse-button-wrist-twist-score-rula', "n_clicks")],
    [State('collapse-wrist-twist-score-rula', "is_open")],
)
def toggle_collapse_wrist_trist_score_rula(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output("fade-a-rula", "is_in"),
    [Input("fade-button-a-rula", "n_clicks")],
    [State("fade-a-rula", "is_in")],
)
def toggle_fade_a(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

@callback(
    Output("fade-b-rula", "is_in"),
    [Input("fade-button-b-rula", "n_clicks")],
    [State("fade-b-rula", "is_in")],
)
def toggle_fade_b(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

# ###### disable neck dropdown #######
# @callback(
#     [Output("neck-twisted", "disabled"),
#      Output("neck-bending", "disabled"),
#      Output("neck-twisted", "value"),
#     Output("neck-bending", "value")],
#     [Input("neck-twisted", "value"), Input("neck-bending", "value")],
# )
# def neck_adjust(nck_twisted, nck_bending):

#     if nck_twisted in [None, ''] or nck_bending in [None, '']:
#         return False, False, '0', '0'

#     if nck_twisted[0] in ['1', 1]:
#         return False, True, '1', '0'
#     elif nck_bending[0] in ['1', 1]:
#         return True, False, '0', '1'
#     else:
#         return False, False, '0', '0'

# ###### disable trunk dropdown #######
# @callback(
#     [Output("trunk-twisted", "disabled"),
#      Output("trunk-bending", "disabled"),
#      Output("trunk-twisted", "value"),
#     Output("trunk-bending", "value")],
#     [Input("trunk-twisted", "value"), Input("trunk-bending", "value")],
# )
# def trunk_adjust(trnk_twisted, trnk_bending):

#     if trnk_twisted in [None, ''] or trnk_bending in [None, '']:
#         return False, False, '0', '0'

#     if trnk_twisted[0] in ['1', 1]:
#         return False, True, '1', '0'
#     elif trnk_bending[0] in ['1', 1]:
#         return True, False, '0', '1'
#     else:
#         return False, False, '0', '0'
    
# ************************  callback Table A *****************************

@callback(
    [Output("table-a-out-one-rula", "children"),
     Output("table-a-out-two-rula", "children"),], 
    [Input("upper-arm-score-rula", "value"),
     Input("shoulder-raised-rula", "value"),
    Input("upper-arm-abducted-rula", "value"),
     Input("upper-arm-supported-rula", "value"),
     Input("lower-arm-score-rula", "value"),
     Input("lower-arm-moving-rula", "value"),
    Input("wrist-score-rula", "value"),
     Input("wrist-adjust-rula", "value"),
     Input("wrist-twist-score-rula", "value"),
     Input("muscle-use-score", "value"),
    Input("force-load-score-rula", "value"),
     Input("fade-button-a-rula", "n_clicks")],
    prevent_initial_call=True,
)
def table_a(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, lower_arm_moving_score, wrist_score, wrist_adjust, wrist_score_twisted, muscle_use_score, force_load_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if upper_arm_score in [None]:
        return no_update

    if lower_arm_score in [None]:
        return no_update
    
    if wrist_score in [None]:
        return no_update
    
    if wrist_score_twisted in [None]:
        return no_update
    
    str_one = "The score for section A, based on the RULA table, and steps 1-7 is: "
    str_two = "The total score for section A with the muscle and force/load score, is: "

    assets_table_a = 'assets/data/rula_tableA.json' ### UpperArm_1|LowerArm_1|Wrist_1|WristTwist_1

    with open(assets_table_a) as f:
        rula_tableA_dict = json.load(f)
    
    if trigger_id == 'fade-button-a-rula':
        ### UpperArm_1|LowerArm_1|Wrist_1|WristTwist_1
        if len(upper_arm_score) > 0 and len(lower_arm_score) > 0 and len(wrist_score) > 0 and len(wrist_score_twisted) > 0:

            upr_arm_scr = int(upper_arm_score[0]) + int(shoulder_raised[0]) + int(upper_arm_abducted[0]) - int(upper_arm_supported[0])
            lwr_arm_scr = int(lower_arm_score[0]) + int(lower_arm_moving_score[0])
            wrst_scr = int(wrist_score[0]) + int(wrist_adjust[0])
            wrst_twstd_scr = int(wrist_score_twisted[0])
            muscle_scr = int(muscle_use_score[0])
            frce_scr = int(force_load_score[0])
            
            lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}{"_"}{str(wrst_twstd_scr)}'

            final_score = int(rula_tableA_dict.get(lookup_ky, "0")) + muscle_scr + frce_scr
            return f'{str_one}{rula_tableA_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""

# ************************  callback Table B *****************************

@callback(
    [Output("table-b-out-one-rula", "children"),
     Output("table-b-out-two-rula", "children"),], 
    [Input("neck-score-rula", "value"),
     Input("neck-twisted-rula", "value"),
    Input("neck-bending-rula", "value"),
     Input("trunk-posture-score-rula", "value"),
     Input("trunk-twisted-rula", "value"),
    Input("trunk-bending-rula", "value"),
     Input("leg-posture-score-rula", "value"),
    Input("muscle-use-score-13", "value"),
     Input("force-load-score-rula-14", "value"),
     Input("fade-button-b-rula", "n_clicks")],
    prevent_initial_call=True,
)
def table_b(neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, muscle_score_thir, force_load_score_fourt, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if neck_score in [None]:
        return no_update

    if trunk_posture_score in [None]:
        return no_update
    
    if leg_posture_score in [None]:
        return no_update
      
    str_one = "The score for section B, based on the RULA table, and steps 9-11 is: "
    str_two = "The total neck, leg and trunk score for section B is: "
    # str_three = "The total neck, leg and trunk score for section B is: "

    assets_table_a = 'assets/data/rula_tableB.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_a) as f:
        rula_tableB_dict = json.load(f)
    
    if trigger_id == 'fade-button-b-rula':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if len(neck_score) > 0 and len(trunk_posture_score) > 0 and len(leg_posture_score) > 0:

            nck_scr = int(neck_score[0]) + int(neck_twisted[0]) + int(neck_bending[0])
            trnck_scr = int(trunk_posture_score[0]) + int(trunk_twisted[0]) + int(trunk_bending[0])
            leg_scr = int(leg_posture_score[0])
            muscle_scr = int(muscle_score_thir[0])
            frce_scr = int(force_load_score_fourt[0])

            lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
            final_score = int(rula_tableB_dict.get(lookup_ky, "0")) + muscle_scr + frce_scr
            return f'{str_one}{rula_tableB_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""

# ************************  callback Table C *****************************
@callback(
    [Output("badge-a-rula", "children"),
     Output("badge-b-rula", "children"),
     Output("badge-c-rula", "children"),
     Output("rula-out", "children")], 
    [Input("upper-arm-score-rula", "value"),
     Input("shoulder-raised-rula", "value"),
    Input("upper-arm-abducted-rula", "value"),
     Input("upper-arm-supported-rula", "value"),
     Input("lower-arm-score-rula", "value"),
     Input("lower-arm-moving-rula", "value"),
    Input("wrist-score-rula", "value"),
     Input("wrist-adjust-rula", "value"),
     Input("wrist-twist-score-rula", "value"),
     Input("muscle-use-score", "value"),
    Input("force-load-score-rula", "value"),
    Input("neck-score-rula", "value"),
     Input("neck-twisted-rula", "value"),
    Input("neck-bending-rula", "value"),
     Input("trunk-posture-score-rula", "value"),
     Input("trunk-twisted-rula", "value"),
    Input("trunk-bending-rula", "value"),
     Input("leg-posture-score-rula", "value"),
    Input("muscle-use-score-13", "value"),
     Input("force-load-score-rula-14", "value"),
    Input("date-change-rula", "date"),
    Input("par-id-rula", "value"),
    Input("procedure-id-rula", "value"),
    ],
    # prevent_initial_call=True,
)
def table_c(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, lower_arm_moving_score, wrist_score, wrist_adjust, wrist_score_twisted, muscle_use_score, force_load_score, neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, muscle_score_thir, force_load_score_fourt, date_value, par_id, procedure_id):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
    assessment = 'RU'
    file_path_stem = '/rula/'

    if neck_score in [None]:
        return no_update

    if trunk_posture_score in [None]:
        return no_update
    
    if leg_posture_score in [None]:
        return no_update
    
    if wrist_score_twisted in [None]:
        return no_update
    
    if upper_arm_score in [None]:
        return no_update

    if lower_arm_score in [None]:
        return no_update
    
    if wrist_score in [None]:
        return no_update
    
    if date_value in [None]:
        return no_update
    
    if par_id in [None]:
        return no_update
    
    if procedure_id in [None]:
        return no_update
    
    str_one = "The total RULA score, based on Table C is: "

    assets_table_a = 'assets/data/rula_tableA.json' ### UpperArm_1|LowerArm_1|Wrist_1|WristTwist_1

    with open(assets_table_a) as f:
        rula_tableA_dict = json.load(f)

    assets_table_b = 'assets/data/rula_tableB.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_b) as f:
        rula_tableB_dict = json.load(f)
    
    assets_table_c = 'assets/data/rula_tableC.json' ### armWrist_1|neckTrunkLeg_1

    with open(assets_table_c) as f:
        rula_tableC_dict = json.load(f)

    if len(upper_arm_score) > 0 and len(lower_arm_score) > 0 and len(wrist_score) > 0 and len(wrist_score_twisted) > 0 and len(neck_score) > 0 and len(trunk_posture_score) > 0 and len(leg_posture_score) > 0:
        
        nck_scr = int(neck_score[0]) + int(neck_twisted[0]) + int(neck_bending[0])
        trnck_scr = int(trunk_posture_score[0]) + int(trunk_twisted[0]) + int(trunk_bending[0])
        leg_scr = int(leg_posture_score[0])
        muscle_scr_b = int(muscle_score_thir[0])
        frce_scr_b = int(force_load_score_fourt[0])
        lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
        score_b_interim = int(rula_tableB_dict.get(lookup_ky, "0"))
        final_score_b =  score_b_interim + muscle_scr_b + frce_scr_b
        
        upr_arm_scr = int(upper_arm_score[0]) + int(shoulder_raised[0]) + int(upper_arm_abducted[0]) - int(upper_arm_supported[0])
        lwr_arm_scr = int(lower_arm_score[0]) + int(lower_arm_moving_score[0])
        wrst_scr = int(wrist_score[0]) + int(wrist_adjust[0])
        wrst_twstd_scr = int(wrist_score_twisted[0])
        muscle_scr = int(muscle_use_score[0])
        frce_scr = int(force_load_score[0])

        lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}{"_"}{str(wrst_twstd_scr)}'
        score_a_interim = int(rula_tableA_dict.get(lookup_ky, "0"))
        final_score_a = score_a_interim + muscle_scr + frce_scr

        lookup_ky = f'{str(final_score_a)}{"_"}{str(final_score_b)}'
        final_score_c = int(rula_tableC_dict.get(lookup_ky, "0"))
        
        rula_score = final_score_c

        rula_temp = output_template_rula.copy()

        rula_temp['Participant_ID'] = par_id
        rula_temp['Assessment'] = assessment
        rula_temp['Procedure_and_Mouth_Quadrant'] = procedure_id
        rula_temp['Variable_ID'] = f'{par_id}{assessment}{procedure_id}'
        rula_temp['Step_1:_Locate_upper_arm_position'] = int(upper_arm_score[0])
        rula_temp['If_shoulder_is_raised'] = int(shoulder_raised[0])
        rula_temp['If_upper_arm_is_abducted'] = int(upper_arm_abducted[0])
        rula_temp['If_arm_is_supported_or_person_is_leaning'] = int(upper_arm_supported[0])
        rula_temp['Step_1_score'] = upr_arm_scr
        rula_temp['Step_2:_Locate_lower_arm_position'] = int(lower_arm_score[0])
        rula_temp['If_either_arm_is_working_across_midline_or_out_to_side_of_body'] = int(lower_arm_moving_score[0])
        rula_temp['Step_2_score'] = lwr_arm_scr
        rula_temp['Step_3:_Locate_wrist_position'] = int(wrist_score[0])
        rula_temp['If_wrist_is_bent_from_midline'] = int(wrist_adjust[0])
        rula_temp['Wrist_score'] = wrst_scr
        rula_temp['Step_4:_Wrist_twist._Wrist_Twist_Score'] = wrst_twstd_scr
        rula_temp['Step_5:_Look_Posture_Score_in_Table_A'] = score_a_interim
        rula_temp['Step_6:_Add_muscle_use_score'] = muscle_scr
        rula_temp['Step_7:_Add_force_load_score'] = frce_scr
        rula_temp['Step_8'] = final_score_a
        rula_temp['Step_9:_Locate_neck_position'] = int(neck_score[0])
        rula_temp['If_neck_is_twisted'] = int(neck_twisted[0])
        rula_temp['If_neck_is_side_bending'] = int(neck_bending[0])
        rula_temp['Neck_score'] = nck_scr
        rula_temp['Step_10:_Locate_trunk_posture'] = int(trunk_posture_score[0])
        rula_temp['If_trunk_is_twisted'] = int(trunk_twisted[0])
        rula_temp['If_trunk_is_side_bending'] = int(trunk_bending[0])
        rula_temp['Trunk_score'] = trnck_scr
        rula_temp['Step_11:_Legs._Leg_score'] = leg_scr
        rula_temp['Step_12:_Look-up_posture_score_in_Table_B_Posture_B_Score'] = score_b_interim
        rula_temp['Step_13:_Add_Muscle_Use_Score'] = muscle_scr_b
        rula_temp['Step_14:_Add_Force_Lead_Score'] = frce_scr_b
        rula_temp['Step_15:_Find_Column_in_Table_C_Neck,_Trunk,_Leg_Score'] = final_score_b
        rula_temp['RULA_Score'] = rula_score

        if rula_score <= 2:
            rula_conclusion = 'Acceptable posture' ### 1-2: Negligible risk 
        elif rula_score > 2 and rula_score <5:
            rula_conclusion = 'Further investigation. Change may be needed' ### 2-3: Low risk. Change may be needed 
        elif rula_score >= 5 and rula_score <7:
            rula_conclusion = 'Further investigation. Change soon' ### 4-7: Medium risk. Further investigate. Change soon. 
        elif rula_score >= 7:
            rula_conclusion = 'Investigate and implement change' ### 11+: Very high risk. Implement change
        
        rula_temp['Scoring'] = rula_conclusion
        rula_temp['date_assessed'] = date_value

        # file_name = f'{file_path_stem}{par_id}{assessment}{procedure_id}{".json"}'
        # data = dbx_cls.dictionary_to_bytes(rula_temp, 'utf-8')
        # dbx_cls.add_to_dropbox(data, file_name)

        return [str(final_score_a)], [str(final_score_b)], [str(final_score_c)], f'{str_one}{str(rula_score)}'
    
    else:
        return no_update