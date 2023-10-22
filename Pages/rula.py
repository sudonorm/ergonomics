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

from utils.components.app_components import AppComponents

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS")
SENDER_EMAIL = os.environ.get("EMAIL_USERNAME")
SENDER_PASS = os.environ.get("EMAIL_PASSWORD")
PORT_NUMBER = os.environ.get("SMTP_PORT")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
# RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
RECEIVER_EMAIL = 'brainihac@gmail.com'

dbx_cls = drop_box.DBXUpDown()
components = AppComponents() 
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

par_ids = ['PAR01', 'PAR02', 'PAR03', 'PAR04', 'PAR05', 'PAR06', 'PAR07', 'PAR08', 'PAR09', 'PAR10', 'Test01', 'Test02', 'Test03']

neck_score_ids = ['1', '2']
neck_score_ids_description = {'A. 0-20°neck flexion': 1, 'B. More than 20° forward flexion of the neck': 2, 'C. Neck extended (bent backward)':2}
neck_score_ids_dict = {'A': 1, 'B': 2, 'C': 2}

neck_score_ids_rula = ['1', '2', '3', '4']

neck_score_ids_rula_description = {'A. 0°-10° - Neck flexion': 1, 'B. 10°-20° - Neck flexion': 2, 'C. More than 20° - Neck is flexion':3, 'D. Neck is extended (bent posteriorly)':4}

neck_score_ids_adjust_description = {'A. Neck is side bending':1, 'B. Neck is twisted':1, 'C. Neck is not twisted OR not side bending':0}
neck_score_ids_adjust_dict = {'A': 1, 'B': 1, 'C': 0}
neck_score_ids_adjust = ['0', '1']

trunk_posture_score_ids = ['1', '2', '3', '4']
trunk_posture_score_ids_description = {'A. 0° - Trunk is straight at no angle to the horizontal':1, 
                                       'B. 0° - 20° - Trunk extended backward': 2,
                                       'C. 0° - 20° - Trunk flexed forward': 2,
                                       'D. 20° - 60° - Trunk flexed forward': 3,
                                       'E. More than 20° - Trunk in extension (bent backward)': 3,
                                       'F. More than 60° - Trunk flexed forward': 4}

trunk_posture_score_ids_rula_description = {'A. 0° - Trunk is held upright in neutral posture':1, 
                                       'B. 0°-20° - Trunk flexion': 2,
                                       'C. 20°-60° - Trunk is flexion': 3,
                                       'D. More than 60° - Trunk flexion': 4}

trunk_posture_ids_adjust = ['0', '1']
trunk_posture_ids_adjust_description = {'A. Trunk is twisted': 1, 'B. Trunk is bent to the side': 1, 'C. Trunk is not twisted OR not bent to the side': 0}

leg_posture_score_ids = ['1', '2']
leg_posture_score_ids_description = {'A. Both legs are straight and the feet are flat on the ground': 1, 'B. One leg is raised or lifted off the ground': 2}
leg_posture_score_adjust_description = {'A. 30-60° angle at the knee joint':1, 'B. >60° angle at the knee joint': 2, 'C. 0° - No angle at the knee joint': 0}
leg_posture_score_adjust = ['0', '1', '2']

force_load_score_ids = ['0', '1', '2']
force_load_score_adjust = ['0', '1']

score_ids_adjust = ['0', '1']
score_ids_adjust_description = {'Yes':1, 'No':0}
score_ids_adjust_neg = ['0', '1']
score_ids_adjust_neg_description = {'Yes':1, 'No':0}

upper_arm_pos_ids = ['1', '2', '3', '4']
upper_arm_pos_ids_description = {'A. 20° to 20° - Upper arm flexion or extension':1, 
                                       'B. More than 20° - Upper arm extension': 2,
                                       'C. 20°-45° - Upper arm flexion': 2,
                                       'D. 45°-90° - Upper arm flexion': 3,
                                       'E. More than 90° - Upper arm flexion': 4}
lower_arm_pos_ids = ['1', '2']
lower_arm_pos_ids_description = {'A. 60°-100° - Lower arm flexion':1, 
                                       'B. 0°-60° - Lower arm flexion': 2,
                                       'C. More than 100° - Lower arm flexion': 2}


wrist_pos_ids = ['1', '2']
wrist_pos_ids_description = {'A. 15°-15° - Wrist flexion or extension':1, 
                                       'B. More than 15° - Wrist extension': 2,
                                       'C. More than 15° - Wrist flexion': 2}

wrist_pos_ids_rula = ['1', '2', '3']
wrist_pos_ids_rula_description = {'A. 0° - Wrist is in the neutral position':1, ### TODO: ask if this should be there
                                       'B. 15°-15° - Wrist flexion or extension': 1,
                                       'C. More than 15° - Wrist extension': 2,
                                       'D. More than 15° - Wrist flexion':2}

wrist_pos_adjust = ['0', '1']
wrist_pos_adjust_description = {'Yes':1, 'No':0}

wrist_twist_pos_ids = ['1', '2']
wrist_twist_pos_ids_description = {'A. Wrist twisted in mid range':1,
                                       'B. Wrist is at or near the end of range': 2,
                                       'C. Wrist is not twisted in mid range OR at or near the end of range': 0}

force_score_ids = ['0', '1', '2', '3']
muscle_score_ids = ['0', '1']
muscle_score_ids_description = {'A. Posture is mainly static (i.e. held >1 minute)':1,
                                       'B. Action repeated occurs 4x per minute': 1,
                                       'C. None of the above': 0}

coupling_score_ids = ['0', '1', '2', '3']
coupling_score_ids_description = {'A. Good - The hand tool have a well fitting handle and mid range power grip':0, 
                                       'B. Fair - Acceptable but not ideal hand hold or coupling acceptable with other body part': 1,
                                       'C. Poor - Hand hold not acceptable but possible': 2,
                                       'D. Unacceptable - No handles, awkward, unsafe with any body part': 3}



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


### Strain Index items

items_speed_work = {"Very slow - Extremely relaxed pace":1,
 "Slow - Taking one's own time":1,
 "Fair - Normal speed of motion":1,
 "Fast - Rushed, but able to keep up":1.5,
 "Very fast - Rushed and barely or unable to keep up":2,
 }

items_hand_wrist = {"Very good - perfectly neutral":1,
 "Good - Near neutral":1,
 "Fair - Non-neutral":1.5,
 "Bad - Marked deviation":2,
 "Very bad - Near extreme":3,
 }


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
                    
                    dbc.Label("Name", html_for="rater-name"),
                    dbc.Input(
                        type="text",
                        id="rater-name",
                        placeholder="Enter your firstname",
                    ),


            ], xs=12, sm=12, md=5, lg=5, xl=5,
                        style={"marginLeft": 5},
                    ),

                    dbc.Col(
                    [
                    
                    dbc.Label("Email", html_for="rater-email"),
                dbc.Input(
                    type="email",
                    id="rater-email",
                    placeholder="Enter email",
                ),

            ], xs=12, sm=12, md=5, lg=5, xl=5,
                        style={"marginLeft": 5},
                    ),

                    ], className="g-3", style={"marginBottom": 20}, justify='center'),

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

    ##### REBA
    dbc.Accordion([ dbc.AccordionItem([
    html.Label("REBA assessment is used to “rapidly” evaluate risk of musculoskeletal disorders (MSD) associated with certain job tasks."),
        ### Table A: neck, trunk, leg
        dbc.Accordion([ dbc.AccordionItem([
            dbc.Card([

                ### Neck position
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([
                            dbc.Col(
                                [
                                    
                                    html.Label('Locate the neck posture:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Neck posture.PNG', height=200, width=400, style={"marginBottom": 20}),

                                    dcc.Dropdown(
                                        id='neck-score',
                                        options=[{'label':x, 'value': x} for x in list(neck_score_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Br(),
                                    html.Hr(),

                                    html.Label('Step 1a: Neck posture (Adjust)', className='fw-bold'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Neck twisted or side bending.PNG', height=200, width=400),

                                    dcc.Dropdown(
                                        id='neck-twisted',
                                        options=[{'label':x, 'value': x} for x in list(neck_score_ids_adjust_description.keys())],
                                        multi=False,
                                        value='C. Neck is not twisted OR not side bending',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 1: Locate the neck position",), ],start_collapsed=True , style={"margin": 10}),

                ### Trunk position
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([

                            dbc.Col(
                                [
                                    html.Label('Locate the trunk posture:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Trunk posture.PNG', height=200, width=450, style={"marginBottom": 20}),

                                    dcc.Dropdown(
                                        id='trunk-posture-score',
                                        options=[{'label':x, 'value': x} for x in list(trunk_posture_score_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Br(),
                                    html.Hr(),

                                    html.Label('Step 2a: Trunk posture (Adjust)', className='fw-bold'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Trunk is twisted or side bending.PNG', height=200, width=400),

                                    dcc.Dropdown(
                                        id='trunk-twisted',
                                        options=[{'label':x, 'value': x} for x in list(trunk_posture_ids_adjust_description.keys())],
                                        multi=False,
                                        value='C. Trunk is not twisted OR not bent to the side',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 2: Locate the trunk position",), ],start_collapsed=True , style={"margin": 10}),

                ### Leg position
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([

                            dbc.Col(
                                [
                                    html.Label('Locate the leg posture:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Leg posture.PNG', height=200, width=450, style={"marginBottom": 20}),

                                    dcc.Dropdown(
                                        id='leg-posture-score',
                                        options=[{'label':x, 'value': x} for x in list(leg_posture_score_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Br(),
                                    html.Hr(),

                                    html.Label('Step 3a: Leg posture (Adjust)', className='fw-bold'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Leg posture (adjust).PNG', height=200, width=400),


                                    # html.Label('Adjust legs score: select 1 for 30-60° and 2 for 60°+', style={"marginTop": 20}),
                                    dcc.Dropdown(
                                        id='leg-posture-adjust',
                                        options=[{'label':x, 'value': x} for x in list(leg_posture_score_adjust_description.keys())],
                                        multi=False,
                                        value='C. 0° - No angle at the knee joint',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
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
                                    
                                    html.Label('Locate Upper Arm Position:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Upper arm posture.PNG', height=200, width=600),
                                    

                                    dcc.Dropdown(
                                        id='upper-arm-score',
                                        options=[{'label':x, 'value': x} for x in list(upper_arm_pos_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Br(),
                                    html.Hr(),

                                    html.Label('Step 7a: Upper Arm Position (Adjust)', className='fw-bold'),
                                    html.Br(),

                                    html.Label('Is the shoulder raised?', className='fw-bold', style={"marginTop": 20}),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Shoulder raised.PNG', height=400, width=200),
                                    dcc.Dropdown(
                                        id='shoulder-raised',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Hr(),

                                    html.Label('Is the upper arm abducted?', className='fw-bold', style={"marginTop": 20}),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Upper arm is abducted.PNG', height=400, width=200),
                                    dcc.Dropdown(
                                        id='upper-arm-abducted',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Hr(),

                                    html.Label('Is the arm supported, or is the person leaning?', className='fw-bold', style={"marginTop": 20}),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Upper arm supported or leaning.PNG', height=400, width=200),
                                    dcc.Dropdown(
                                        id='upper-arm-supported',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_neg_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 7: Locate upper arm position",), ],start_collapsed=True , style={"margin": 10}),

                ### Lower arm position
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([
                            
                            dbc.Col(
                                [

                                    html.Label('Locate Lower Arm Position:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Lower arm posture.PNG', height=200, width=450),

                                    dcc.Dropdown(
                                        id='lower-arm-score',
                                        options=[{'label':x, 'value': x} for x in list(lower_arm_pos_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 8: Locate lower arm position",), ],start_collapsed=True , style={"margin": 10}),

                ### Wrist position
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([

                            dbc.Col(
                                [
                                    
                                    html.Label('Wrist score:'),
                                    html.Br(),
                                    html.Img(src='assets/images/reba/Wrist posture.PNG', height=200, width=450),

                                    dcc.Dropdown(
                                        id='wrist-score',
                                        options=[{'label':x, 'value': x} for x in list(wrist_pos_ids_description.keys())],
                                        multi=False,
                                        value='',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Br(),
                                    html.Hr(),

                                    html.Label('Step 9a: Adjust', className='fw-bold'),
                                    html.Br(),

                                    html.Label('Is the wrist bent from the midline or twisted?', style={"marginTop": 20}),
                                    html.Img(src='assets/images/reba/Wrist bent from the midline or twisted.PNG', height=200, width=450),
                                    dcc.Dropdown(
                                        id='wrist-adjust',
                                        options=[{'label':x, 'value': x} for x in list(wrist_pos_adjust_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 9: Locate wrist posture",), ],start_collapsed=True , style={"margin": 10}),


                ### Add coupling score
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([

                            dbc.Col(
                                [
  
                                    html.Label('Select coupling score:', className='fw-bold'),
                                    html.Br(),
                                    
                                    dcc.Dropdown(
                                        id='coupling-score',
                                        options=[{'label':x, 'value': x} for x in list(coupling_score_ids_description.keys())],
                                        multi=False,
                                        value='A. Good - The hand tool have a well fitting handle and mid range power grip',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 11: Add coupling score",), ],start_collapsed=True , style={"margin": 10}),

                ### Activity score
                dbc.Accordion([ dbc.AccordionItem([

                    dbc.Row([
    
                            dbc.Col(
                                [
        
                                    html.Label('1 or more body parts are held for longer than 1 minute (static). If yes, select 1', style={"marginTop": 20}),
                                    dcc.Dropdown(
                                        id='activity-score-one',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Label('Repeat small range actions more than 4X per minute)', style={"marginTop": 20}),
                                    dcc.Dropdown(
                                        id='activity-score-two',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                                    html.Label('Action causes rapid large range changes in postures or unstable base', style={"marginTop": 20}),
                                    dcc.Dropdown(
                                        id='activity-score-three',
                                        options=[{'label':x, 'value': x} for x in list(score_ids_adjust_neg_description.keys())],
                                        multi=False,
                                        value='No',
                                        searchable=False,
                                        disabled=False
                                    ),

                        ], xs=12, sm=12, md=12, lg=12, xl=12,
                                ),

                    ], style={"marginBottom": 20}, justify='center'),

                ], title="Step 13: Activity Score",), ], start_collapsed=True, style={"margin": 10, 'marginBottom':20}),

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
                                                dbc.Badge(children=[""],id="badge-a-reba", color="light", text_color="primary", className="ms-1"),
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
                                                dbc.Badge(children=[""],id="badge-b-reba", color="light", text_color="primary", className="ms-1"),
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
                                                dbc.Badge(children=[""],id="badge-c-reba", color="light", text_color="primary", className="ms-1"),
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


                # ### Activity score
                # dbc.Accordion([ dbc.AccordionItem([

                #     dbc.Row([
                #             dbc.Col(
                #                 [
                #                     html.Img(src='assets/images/13. Activity score.PNG', height=200, width=600)
                #         ], xs=12, sm=12, md=7, lg=7, xl=7,
                #                 ),
    
                #             dbc.Col(
                #                 [
        
                #                     html.Label('1 or more body parts are held for longer than 1 minute (static). If yes, select 1', style={"marginTop": 20}),
                #                     dcc.Dropdown(
                #                         id='activity-score-one',
                #                         options=[{'label':x, 'value': x} for x in score_ids_adjust],
                #                         multi=False,
                #                         value='0',
                #                         searchable=False,
                #                         disabled=False
                #                     ),

                #                     html.Label('Repeat small range actions more than 4X per minute)', style={"marginTop": 20}),
                #                     dcc.Dropdown(
                #                         id='activity-score-two',
                #                         options=[{'label':x, 'value': x} for x in score_ids_adjust],
                #                         multi=False,
                #                         value='0',
                #                         searchable=False,
                #                         disabled=False
                #                     ),

                #                     html.Label('Action causes rapid large range changes in postures or unstable base', style={"marginTop": 20}),
                #                     dcc.Dropdown(
                #                         id='activity-score-three',
                #                         options=[{'label':x, 'value': x} for x in score_ids_adjust_neg],
                #                         multi=False,
                #                         value='0',
                #                         searchable=False,
                #                         disabled=False
                #                     ),

                #         ], xs=12, sm=12, md=5, lg=5, xl=5,
                #                 ),

                #     ], style={"marginBottom": 20}, justify='center'),

                # ], title="Step 13: Activity Score",), ],start_collapsed=True, style={"margin": 10}),


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

    ], title="Rapid Entire Body Assessment (REBA) Ergonomic Assessment",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

    ##### RULA
    dbc.Accordion([ dbc.AccordionItem([
    html.Label("RULA was developed to “rapidly” evaluate the exposure of individual workers to ergonomic risk factors associated with upper extremity MSD."),
    ### Table A: Arm and Wrist Analysis
    dbc.Accordion([ dbc.AccordionItem([
        dbc.Card([

            ### Upper arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/1. Locate Upper Arm Position.PNG', height=200, width=400)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),
   
                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Upper arm position:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-upper-arm-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                  
                                #                         html.P("20-20°: +1", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("20° (in extension i.e. downward and backward): Add +2", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("20-45° (flexion): +2", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("45-90° (flexion):  +3", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("90°+: +4", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-upper-arm-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                html.Label('Upper arm position:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/Upper arm posture.PNG', height=200, width=700),

                                dcc.Dropdown(
                                    id='upper-arm-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(upper_arm_pos_ids_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 1a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the shoulder raised?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Shoulder raised.PNG', height=400, width=250),
                                dcc.Dropdown(
                                    id='shoulder-raised-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the upper arm abducted?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Upper arm is abducted.PNG', height=400, width=250),
                                dcc.Dropdown(
                                    id='upper-arm-abducted-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the arm supported or is the person leaning?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Upper arm supported or leaning.PNG', height=400, width=250),
                                dcc.Dropdown(
                                    id='upper-arm-supported-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 1: Locate upper arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Lower arm position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/2. Lower Arm Score.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),

                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Lower arm score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-lower-arm-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                  
                                #                         html.P("60-100°: Add +1", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("0-60°: +2", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("100°+ (in the upward direction): +2", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-lower-arm-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                html.Label('Lower arm score:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/Lower arm posture.PNG', height=200, width=450),

                                dcc.Dropdown(
                                    id='lower-arm-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(lower_arm_pos_ids_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 2a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is either arm working across the midline or out to side of body?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Lower arm cross midline or side of body.PNG', height=200, width=450),
                                dcc.Dropdown(
                                    id='lower-arm-moving-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 2: Locate lower arm position",), ],start_collapsed=True , style={"margin": 10}),

            ### Wrist position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/3. Wrist position.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),

                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Wrist score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-wrist-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                  
                                #                         html.P("15-15°: +1", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("15°+ (in the upward position): +2", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("15°+ (in the downward position): +2", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-wrist-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                
                                html.Label('Wrist score:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/Wrist posture.PNG', height=200, width=450), 

                                dcc.Dropdown(
                                    id='wrist-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(wrist_pos_ids_rula_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 3a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the wrist bent from the midline or twisted?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Wrist bent from midline.PNG', height=400, width=250),
                                dcc.Dropdown(
                                    id='wrist-adjust-rula',
                                    options=[{'label':x, 'value': x} for x in list(wrist_pos_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 3: Locate wrist posture",), ],start_collapsed=True , style={"margin": 10}),

            ### Wrist twist position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/4. Wrist twist.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),

                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Wrist Twist score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-wrist-twist-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                  
                                #                         html.P("If wrist is twisted in mid-range: +1 ", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("If wrist is at or near end of range: +2", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-wrist-twist-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                html.Label('Wrist Twist score:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/4. Wrist twist.PNG', height=200, width=450), ## TODO: change image

                                dcc.Dropdown(
                                    id='wrist-twist-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(wrist_twist_pos_ids_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 4: Wrist twist score",), ],start_collapsed=True , style={"margin": 10}),

            ### Add muscle use score
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/6. Add muscle use score.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),

                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Select muscle use score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-muscle-use-score",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                  
                                #                         html.P("If posture is mainly static (i.e. held >10 minutes), or if action repeated occurs 4X per minute: Add +1", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-muscle-use-score",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                html.Label('Select muscle use:'),

                                dcc.Dropdown(
                                    id='muscle-use-score',
                                    options=[{'label':x, 'value': x} for x in list(muscle_score_ids_description.keys())],
                                    multi=False,
                                    value='C. None of the above',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 6: Add muscle use score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            # ### Force adjusting
            # dbc.Accordion([ dbc.AccordionItem([

            #     dbc.Row([
            #             dbc.Col(
            #                 [
            #                     html.Img(src='assets/images/rula/7. Add force or load score.PNG', height=200, width=450)
            #         ], xs=12, sm=12, md=7, lg=7, xl=7,
            #                 ),

            #             dbc.Col(
            #                 [
            #                     dbc.Row([
            #                         dbc.Col([
            #                             html.Label('Add force or load score:'),
            #                         ], xs=12, sm=12, md=6, lg=6, xl=6,
            #                         ),
            #                         dbc.Col([
            #                             html.Div(
            #                                 [
            #                                     dbc.Button(
            #                                         "Open description",
            #                                         id="collapse-button-force-load-score-rula",
            #                                         className="mb-3",
            #                                         color="primary",
            #                                         n_clicks=0,
            #                                         size="sm"
            #                                     ),
            #                                     dbc.Collapse(
            #                                         dbc.Card(dbc.CardBody([
            #                                             html.P("If load <4.4 Ibs. (intermittent): +0", 
                                                            
            #                                                 className="card-text"),
            #                                             html.P("If load 4.4 to 22 Ibs. (intermittent): +1", 
                                                            
            #                                                 className="card-text"),
            #                                             html.P("If load 4.44 to 22 Ibs. (static or repeated): +2", 
                                                            
            #                                                 className="card-text"),
                                                            
            #                                             html.P("If more than 22 Ibs. or repeated or shocks: +3", 
                                                            
            #                                                 className="card-text"),
            #                                             ])),
            #                                         id="collapse-force-load-score-rula",
            #                                         is_open=False,
            #                                         style={"marginBottom": 20},
            #                                     ),
            #                                 ], className='d-grid',
            #                             ),
            #                             ], xs=12, sm=12, md=6, lg=6, xl=6
            #                         ),
            #                     ]),

            #                     dcc.Dropdown(
            #                         id='force-load-score-rula',
            #                         options=[{'label':x, 'value': x} for x in force_score_ids],
            #                         multi=False,
            #                         value='0',
            #                         searchable=False,
            #                         disabled=False
            #                     ),

            #         ], xs=12, sm=12, md=5, lg=5, xl=5,
            #                 ),

            #     ], style={"marginBottom": 20}, justify='center'),

            # ], title="Step 7: Add force/ load score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

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
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/9. Neck position.PNG', height=200, width=400)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),

                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Neck score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-neck-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                #                         html.P("0-10° (flexion) = +1", 
                                                            
                                #                             className="card-text"),

                                #                         html.P("10-20° (flexion) = +2", 
                                                            
                                #                             className="card-text"),

                                #                         html.P("20°+ (flexion)= +3", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("In extension (neck bent backward)= +4", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-neck-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),


                                html.Label('Neck score:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/Neck posture.PNG', height=200, width=600),

                                dcc.Dropdown(
                                    id='neck-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(neck_score_ids_rula_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 9a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the neck twisted?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Neck twisted (updated).PNG', height=400, width=350),
                                dcc.Dropdown(
                                    id='neck-twisted-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the neck side bending?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Neck side bending.PNG', height=400, width=350),
                                dcc.Dropdown(
                                    id='neck-bending-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 9: Locate the neck position",), ],start_collapsed=True , style={"margin": 10}),

            ### Trunk position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/10. Trunk position.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),
                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Trunk Posture score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-trunk-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                #                         html.P("0° = +1", 
                                                            
                                #                             className="card-text"),

                                #                         html.P("0° - 20° (flexion i.e. forward neck motion):   +2", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("20° - 60° (flexion): +3", 
                                                            
                                #                             className="card-text"),

                                #                         html.P("60°+ (flexion): +4", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-trunk-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                

                                html.Label('Trunk Posture score:'),
                                html.Br(),
                                html.Img(src='assets/images/rula/Trunk posture.PNG', height=200, width=450),

                                dcc.Dropdown(
                                    id='trunk-posture-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(trunk_posture_score_ids_rula_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Br(),
                                html.Hr(),

                                html.Label('Step 10a: Adjust', className='fw-bold'),
                                html.Br(),

                                html.Label('Is the trunk twisted?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Trunk twisted.PNG', height=400, width=350),

                                dcc.Dropdown(
                                    id='trunk-twisted-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                                html.Label('Is the trunk side bending?', style={"marginTop": 20}),
                                html.Br(),
                                html.Img(src='assets/images/rula/Trunk side bending.PNG', height=400, width=350),

                                dcc.Dropdown(
                                    id='trunk-bending-rula',
                                    options=[{'label':x, 'value': x} for x in list(score_ids_adjust_description.keys())],
                                    multi=False,
                                    value='No',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 10: Locate the trunk posture",), ],start_collapsed=True , style={"margin": 10}),

            ### Leg position
            dbc.Accordion([ dbc.AccordionItem([

                dbc.Row([
                    #     dbc.Col(
                    #         [
                    #             html.Img(src='assets/images/rula/11. Legs.PNG', height=200, width=450)
                    # ], xs=12, sm=12, md=7, lg=7, xl=7,
                    #         ),
                        dbc.Col(
                            [
                                # dbc.Row([
                                #     dbc.Col([
                                #         html.Label('Leg Posture score:'),
                                #     ], xs=12, sm=12, md=6, lg=6, xl=6,
                                #     ),
                                #     dbc.Col([
                                #         html.Div(
                                #             [
                                #                 dbc.Button(
                                #                     "Open description",
                                #                     id="collapse-button-leg-pos-score-rula",
                                #                     className="mb-3",
                                #                     color="primary",
                                #                     n_clicks=0,
                                #                     size="sm"
                                #                 ),
                                #                 dbc.Collapse(
                                #                     dbc.Card(dbc.CardBody([
                                #                         html.P("If legs and feet are spotted: Add +1", 
                                                            
                                #                             className="card-text"),
                                #                         html.P("If not: Add +2", 
                                                            
                                #                             className="card-text"),
                                                        
                                #                         ])),
                                #                     id="collapse-leg-pos-score-rula",
                                #                     is_open=False,
                                #                     style={"marginBottom": 20},
                                #                 ),
                                #             ], className='d-grid',
                                #         ),
                                #         ], xs=12, sm=12, md=6, lg=6, xl=6
                                #     ),
                                # ]),

                                html.Label('Leg Posture score:'),
                                html.Br(),

                                dbc.Row([

                                    dbc.Col([
                                        html.Img(src='assets/images/rula/Leg - bilateral weight bearing.PNG', height=200, width=250),
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,),

                                    dbc.Col([
                                        html.Img(src='assets/images/rula/Leg - One leg raised.PNG', height=200, width=250),  
                                    ], xs=12, sm=12, md=6, lg=6, xl=6,),
                                ]),
                                
                                dcc.Dropdown(
                                    id='leg-posture-score-rula',
                                    options=[{'label':x, 'value': x} for x in list(leg_posture_score_ids_description.keys())],
                                    multi=False,
                                    value='',
                                    searchable=False,
                                    disabled=False
                                ),

                    ], xs=12, sm=12, md=12, lg=12, xl=12,
                            ),

                ], style={"marginBottom": 20}, justify='center'),

            ], title="Step 11: Leg score",), ],start_collapsed=True , style={"margin": 10}),

            # ### Add muscle use score
            # dbc.Accordion([ dbc.AccordionItem([

            #     dbc.Row([
            #             dbc.Col(
            #                 [
            #                     html.Img(src='assets/images/rula/13. Add muscle use score.PNG', height=200, width=450)
            #         ], xs=12, sm=12, md=7, lg=7, xl=7,
            #                 ),

            #             dbc.Col(
            #                 [
            #                     dbc.Row([
            #                         dbc.Col([
            #                             html.Label('Select muscle use score:'),
            #                         ], xs=12, sm=12, md=6, lg=6, xl=6,
            #                         ),
            #                         dbc.Col([
            #                             html.Div(
            #                                 [
            #                                     dbc.Button(
            #                                         "Open description",
            #                                         id="collapse-button-muscle-use-score-13",
            #                                         className="mb-3",
            #                                         color="primary",
            #                                         n_clicks=0,
            #                                         size="sm"
            #                                     ),
            #                                     dbc.Collapse(
            #                                         dbc.Card(dbc.CardBody([
                                  
            #                                             html.P("If posture is mainly static (i.e. held >10 minutes), or if action repeated occurs 4X per minute: Add +1", 
                                                            
            #                                                 className="card-text"),
                                                        
            #                                             ])),
            #                                         id="collapse-muscle-use-score-13",
            #                                         is_open=False,
            #                                         style={"marginBottom": 20},
            #                                     ),
            #                                 ], className='d-grid',
            #                             ),
            #                             ], xs=12, sm=12, md=6, lg=6, xl=6
            #                         ),
            #                     ]),

            #                     dcc.Dropdown(
            #                         id='muscle-use-score-13',
            #                         options=[{'label':x, 'value': x} for x in muscle_score_ids],
            #                         multi=False,
            #                         value='0',
            #                         searchable=False,
            #                         disabled=False
            #                     ),

            #         ], xs=12, sm=12, md=5, lg=5, xl=5,
            #                 ),

            #     ], style={"marginBottom": 20}, justify='center'),

            # ], title="Step 13: Add muscle use score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

            # ### Force adjusting
            # dbc.Accordion([ dbc.AccordionItem([

            #     dbc.Row([
            #             dbc.Col(
            #                 [
            #                     html.Img(src='assets/images/rula/14. Add force or load score.PNG', height=200, width=450)
            #         ], xs=12, sm=12, md=7, lg=7, xl=7,
            #                 ),

            #             dbc.Col(
            #                 [
            #                     dbc.Row([
            #                         dbc.Col([
            #                             html.Label('Add force or load score:'),
            #                         ], xs=12, sm=12, md=6, lg=6, xl=6,
            #                         ),
            #                         dbc.Col([
            #                             html.Div(
            #                                 [
            #                                     dbc.Button(
            #                                         "Open description",
            #                                         id="collapse-button-force-load-score-rula-14",
            #                                         className="mb-3",
            #                                         color="primary",
            #                                         n_clicks=0,
            #                                         size="sm"
            #                                     ),
            #                                     dbc.Collapse(
            #                                         dbc.Card(dbc.CardBody([
            #                                             html.P("If load <4.4 Ibs. (intermittent): +0", 
                                                            
            #                                                 className="card-text"),
            #                                             html.P("If load 4.4 to 22 Ibs. (intermittent): +1", 
                                                            
            #                                                 className="card-text"),
            #                                             html.P("If load 4.44 to 22 Ibs. (static or repeated): +2", 
                                                            
            #                                                 className="card-text"),
                                                            
            #                                             html.P("If more than 22 Ibs. or repeated or shocks: +3", 
                                                            
            #                                                 className="card-text"),
            #                                             ])),
            #                                         id="collapse-force-load-score-rula-14",
            #                                         is_open=False,
            #                                         style={"marginBottom": 20},
            #                                     ),
            #                                 ], className='d-grid',
            #                             ),
            #                             ], xs=12, sm=12, md=6, lg=6, xl=6
            #                         ),
            #                     ]),

            #                     dcc.Dropdown(
            #                         id='force-load-score-rula-14',
            #                         options=[{'label':x, 'value': x} for x in force_score_ids],
            #                         multi=False,
            #                         value='0',
            #                         searchable=False,
            #                         disabled=False
            #                     ),

            #         ], xs=12, sm=12, md=5, lg=5, xl=5,
            #                 ),

            #     ], style={"marginBottom": 20}, justify='center'),

            # ], title="Step 14: Add force/ load score",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

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
  
], title="Rapid Upper Limb Assessment (RULA) Ergonomic Assessment",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),

### Strain Index
dbc.Accordion([ dbc.AccordionItem([

    components.create_strain_index_ui(accordion_title="RIGHT Upper Extremity", dpn_borg_intensity_id="borg-intensity-right", dpn_items_borg_intensity = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10},
        total_observations_id = "total-observations-right", total_number_of_exertion_id = "total-number-of-exertion-right", duration_of_exertion_id = "duration-of-exertion-right",
        dpn_hand_wrist_id = "hand-wrist-right", dpn_items_hand_wrist = items_hand_wrist, dpn_speed_work_id="speed-work-right", dpn_items_speed_work=items_speed_work,
        dpn_dur_task_per_day_id="dur-task-per-day-right", dpn_items_dur_task_per_day={"<1":0.25, "1-2":0.50, "2-4":0.75, "4-8":1.00, ">8":1.50}, strain_index_result_id="strain-index-right"),

    components.create_strain_index_ui(accordion_title="LEFT Upper Extremity", dpn_borg_intensity_id="borg-intensity-left", dpn_items_borg_intensity = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10},
        total_observations_id = "total-observations-left", total_number_of_exertion_id = "total-number-of-exertion-left", duration_of_exertion_id = "duration-of-exertion-left",
        dpn_hand_wrist_id = "hand-wrist-left", dpn_items_hand_wrist = items_hand_wrist, dpn_speed_work_id="speed-work-left", dpn_items_speed_work=items_speed_work,                               
        dpn_dur_task_per_day_id="dur-task-per-day-left", dpn_items_dur_task_per_day={"<1":0.25, "1-2":0.50, "2-4":0.75, "4-8":1.00, ">8":1.50}, strain_index_result_id="strain-index-left"),
    
    
], title="Strain Index",), ],start_collapsed=True , style={"margin": 10, 'marginBottom':20}),


])


"borg-intensity-right"
"total-observations-right"
"total-number-of-exertion-right"
"duration-of-exertion-right"
"hand-wrist-right"
"speed-work-right"
"dur-task-per-day-right"



#####calculate strain index Right
@callback(
    Output("strain-index-right", "children"),
    [Input("borg-intensity-right", "value"),
     Input("total-observations-right", "value"),
     Input("total-number-of-exertion-right", "value"),
     Input("duration-of-exertion-right", "value"),
     Input("hand-wrist-right", "value"),
     Input("speed-work-right", "value"),
     Input("dur-task-per-day-right", "value"),],
)
def calculate_strain_index_right(borg_intensity, total_observations, total_number_of_exertion, duration_of_exertion, hand_wrist, speed_work, dur_task_per_day):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if borg_intensity in [None, ""]:
        return no_update 
    if total_observations in [None, ""]:
        return no_update 
    if total_number_of_exertion in [None, ""]:
        return no_update
    if duration_of_exertion in [None, ""]:
        return no_update
    if hand_wrist in [None, ""]:
        return no_update
    if speed_work in [None, ""]:
        return no_update 
    if dur_task_per_day in [None, ""]:
        return no_update
    
    print(borg_intensity, total_observations, total_number_of_exertion, duration_of_exertion, hand_wrist, speed_work, dur_task_per_day)

    calculated_duration_of_exertion = total_number_of_exertion / total_observations
    calculated_efforts_per_minute = calculated_duration_of_exertion * 60

    if calculated_efforts_per_minute >= 20:
        effort_per_minute = 3
    elif calculated_efforts_per_minute >= 15:
        effort_per_minute = 2
    elif calculated_efforts_per_minute >= 9:
        effort_per_minute = 1.5
    elif calculated_efforts_per_minute >= 4:
        effort_per_minute = 1
    elif calculated_efforts_per_minute < 4:
        effort_per_minute = 0.5

    strain_index = borg_intensity * duration_of_exertion * effort_per_minute * hand_wrist * speed_work * dur_task_per_day

    msg = f'{"The Strain Index is "}{strain_index}{" and based on this number the job "}'
    
    if strain_index < 3: 
        msg += "is probably safe"
    elif strain_index >=3 and strain_index <= 7:
        msg += "may place individual at increased risk for distal upper extremety disorders"
    else:
        msg += "is probably hazardous"


    return [str(msg)]

#####calculate strain index Right
@callback(
    Output("strain-index-left", "children"),
    [Input("borg-intensity-left", "value"),
     Input("total-observations-left", "value"),
     Input("total-number-of-exertion-left", "value"),
     Input("duration-of-exertion-left", "value"),
     Input("hand-wrist-left", "value"),
     Input("speed-work-left", "value"),
     Input("dur-task-per-day-left", "value"),],
)
def calculate_strain_index_left(borg_intensity, total_observations, total_number_of_exertion, duration_of_exertion, hand_wrist, speed_work, dur_task_per_day):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if borg_intensity in [None, ""]:
        return no_update 
    if total_observations in [None, ""]:
        return no_update 
    if total_number_of_exertion in [None, ""]:
        return no_update
    if duration_of_exertion in [None, ""]:
        return no_update
    if hand_wrist in [None, ""]:
        return no_update
    if speed_work in [None, ""]:
        return no_update 
    if dur_task_per_day in [None, ""]:
        return no_update
    
    # print(borg_intensity, total_observations, total_number_of_exertion, duration_of_exertion, hand_wrist, speed_work, dur_task_per_day)

    calculated_duration_of_exertion = total_number_of_exertion / total_observations
    calculated_efforts_per_minute = calculated_duration_of_exertion * 60

    if calculated_efforts_per_minute >= 20:
        effort_per_minute = 3
    elif calculated_efforts_per_minute >= 15:
        effort_per_minute = 2
    elif calculated_efforts_per_minute >= 9:
        effort_per_minute = 1.5
    elif calculated_efforts_per_minute >= 4:
        effort_per_minute = 1
    elif calculated_efforts_per_minute < 4:
        effort_per_minute = 0.5

    strain_index = borg_intensity * duration_of_exertion * effort_per_minute * hand_wrist * speed_work * dur_task_per_day

    msg = f'{"The Strain Index is "}{strain_index}{" and based on this number the job "}'
    
    if strain_index < 3: 
        msg += "is probably safe"
    elif strain_index >=3 and strain_index <= 7:
        msg += "may place individual at increased risk for distal upper extremety disorders"
    else:
        msg += "is probably hazardous"


    return [str(msg)]

# @callback(
#     Output("collapse-neck-score-rula", "is_open"),
#     [Input("collapse-button-neck-score-rula", "n_clicks")],
#     [State("collapse-neck-score-rula", "is_open")],
# )
# def toggle_collapse_neck_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-trunk-score-rula", "is_open"),
#     [Input("collapse-button-trunk-score-rula", "n_clicks")],
#     [State("collapse-trunk-score-rula", "is_open")],
# )
# def toggle_collapse_trunk_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-leg-pos-score-rula", "is_open"),
#     [Input("collapse-button-leg-pos-score-rula", "n_clicks")],
#     [State("collapse-leg-pos-score-rula", "is_open")],
# )
# def toggle_collapse_leg_pos_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-muscle-use-score", "is_open"),
#     [Input("collapse-button-muscle-use-score", "n_clicks")],
#     [State("collapse-muscle-use-score", "is_open")],
# )
# def toggle_collapse_muscle_use_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-muscle-use-score-13", "is_open"),
#     [Input("collapse-button-muscle-use-score-13", "n_clicks")],
#     [State("collapse-muscle-use-score-13", "is_open")],
# )
# def toggle_collapse_muscle_use_score_rula_thir(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-force-load-score-rula", "is_open"),
#     [Input("collapse-button-force-load-score-rula", "n_clicks")],
#     [State("collapse-force-load-score-rula", "is_open")],
# )
# def toggle_collapse_force_load_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-force-load-score-rula-14", "is_open"),
#     [Input("collapse-button-force-load-score-rula-14", "n_clicks")],
#     [State("collapse-force-load-score-rula-14", "is_open")],
# )
# def toggle_collapse_force_load_score_rula_four(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-upper-arm-score-rula", "is_open"),
#     [Input("collapse-button-upper-arm-score-rula", "n_clicks")],
#     [State("collapse-upper-arm-score-rula", "is_open")],
# )
# def toggle_collapse_upper_arm_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-lower-arm-score-rula", "is_open"),
#     [Input("collapse-button-lower-arm-score-rula", "n_clicks")],
#     [State("collapse-lower-arm-score-rula", "is_open")],
# )
# def toggle_collapse_lower_arm_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-wrist-score-rula", "is_open"),
#     [Input("collapse-button-wrist-score-rula", "n_clicks")],
#     [State("collapse-wrist-score-rula", "is_open")],
# )
# def toggle_collapse_wrist_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output('collapse-wrist-twist-score-rula', "is_open"),
#     [Input('collapse-button-wrist-twist-score-rula', "n_clicks")],
#     [State('collapse-wrist-twist-score-rula', "is_open")],
# )
# def toggle_collapse_wrist_trist_score_rula(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@callback(
    Output("fade-a-rula", "is_in"),
    [Input("fade-button-a-rula", "n_clicks")],
    [State("fade-a-rula", "is_in")],
)
def toggle_fade_a_rula(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

@callback(
    Output("fade-b-rula", "is_in"),
    [Input("fade-button-b-rula", "n_clicks")],
    [State("fade-b-rula", "is_in")],
)
def toggle_fade_b_rula(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in
    
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
    # Input("force-load-score-rula", "value"),
     Input("fade-button-a-rula", "n_clicks")],
    prevent_initial_call=True,
)
def table_a_rula(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, lower_arm_moving_score, wrist_score, wrist_adjust, wrist_score_twisted, muscle_use_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    print(upper_arm_score ,lower_arm_score, wrist_score, wrist_score_twisted)

    if upper_arm_score in [None, ""]:
        return no_update

    if lower_arm_score in [None, ""]:
        return no_update
    
    if wrist_score in [None, ""]:
        return no_update
    
    if wrist_score_twisted in [None, ""]:
        return no_update
    
    str_one = "The score for section A, based on the RULA table, and steps 1-7 is: "
    str_two = "The total score for section A with the muscle and force/load score, is: "

    assets_table_a = 'assets/data/rula_tableA.json' ### UpperArm_1|LowerArm_1|Wrist_1|WristTwist_1

    with open(assets_table_a) as f:
        rula_tableA_dict = json.load(f)
    
    if trigger_id == 'fade-button-a-rula':
        ### UpperArm_1|LowerArm_1|Wrist_1|WristTwist_1
        if len(upper_arm_score) > 0 and len(lower_arm_score) > 0 and len(wrist_score) > 0 and len(wrist_score_twisted) > 0:

            upr_arm_scr = int(upper_arm_pos_ids_description.get(upper_arm_score)) + int(score_ids_adjust_description.get(shoulder_raised)) + int(score_ids_adjust_description.get(upper_arm_abducted)) - int(score_ids_adjust_description.get(upper_arm_supported))
            lwr_arm_scr = int(lower_arm_pos_ids_description.get(lower_arm_score)) + int(score_ids_adjust_description.get(lower_arm_moving_score))
            wrst_scr = int(wrist_pos_ids_rula_description.get(wrist_score)) + int(wrist_pos_adjust_description.get(wrist_adjust))
            wrst_twstd_scr = int(wrist_twist_pos_ids_description.get(wrist_score_twisted))
            muscle_scr = int(muscle_score_ids_description.get(muscle_use_score))
            # frce_scr = int(force_load_score[0])
            
            lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}{"_"}{str(wrst_twstd_scr)}'

            final_score = int(rula_tableA_dict.get(lookup_ky, "0")) + muscle_scr#+ frce_scr
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
    # Input("muscle-use-score-13", "value"),
    #  Input("force-load-score-rula-14", "value"),
     Input("fade-button-b-rula", "n_clicks")],
    prevent_initial_call=True,
)
def table_b_rula(neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if neck_score in [None, ""]:
        return no_update

    if trunk_posture_score in [None, ""]:
        return no_update
    
    if leg_posture_score in [None, ""]:
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

            nck_scr = int(neck_score_ids_rula_description.get(neck_score)) + int(score_ids_adjust_description.get(neck_twisted)) + int(score_ids_adjust_description.get(neck_bending))
            trnck_scr = int(trunk_posture_score_ids_rula_description.get(trunk_posture_score)) + int(score_ids_adjust_description.get(trunk_twisted)) + int(score_ids_adjust_description.get(trunk_bending))
            leg_scr = int(leg_posture_score_ids_description.get(leg_posture_score))
            # muscle_scr = int(muscle_score_thir[0])
            # frce_scr = int(force_load_score_fourt[0])

            lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
            final_score = int(rula_tableB_dict.get(lookup_ky, "0"))# + muscle_scr + frce_scr
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
    # Input("force-load-score-rula", "value"),
    Input("neck-score-rula", "value"),
     Input("neck-twisted-rula", "value"),
    Input("neck-bending-rula", "value"),
     Input("trunk-posture-score-rula", "value"),
     Input("trunk-twisted-rula", "value"),
    Input("trunk-bending-rula", "value"),
     Input("leg-posture-score-rula", "value"),
    # Input("muscle-use-score-13", "value"),
    #  Input("force-load-score-rula-14", "value"),
    Input("date-change", "date"),
    Input("par-id", "value"),
    Input("procedure-id", "value"),
    ],
    # prevent_initial_call=True,
)
def table_c_rula(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, lower_arm_moving_score, wrist_score, wrist_adjust, wrist_score_twisted, muscle_use_score, neck_score, neck_twisted, neck_bending, trunk_posture_score, trunk_twisted, trunk_bending, leg_posture_score, date_value, par_id, procedure_id):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
    assessment = 'RU'
    file_path_stem = '/rula/'

    if neck_score in [None, ""]:
        return no_update

    if trunk_posture_score in [None, ""]:
        return no_update
    
    if leg_posture_score in [None, ""]:
        return no_update
    
    if wrist_score_twisted in [None, ""]:
        return no_update
    
    if upper_arm_score in [None, ""]:
        return no_update

    if lower_arm_score in [None, ""]:
        return no_update
    
    if wrist_score in [None, ""]:
        return no_update
    
    if date_value in [None, ""]:
        return no_update
    
    if par_id in [None, ""]:
        return no_update
    
    if procedure_id in [None, ""]:
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
        
        nck_scr = int(neck_score_ids_rula_description.get(neck_score)) + int(score_ids_adjust_description.get(neck_twisted)) + int(score_ids_adjust_description.get(neck_bending))
        trnck_scr = int(trunk_posture_score_ids_rula_description.get(trunk_posture_score)) + int(score_ids_adjust_description.get(trunk_twisted)) + int(score_ids_adjust_description.get(trunk_bending))
        leg_scr = int(leg_posture_score_ids_description.get(leg_posture_score))
        # muscle_scr_b = int(muscle_score_thir[0])
        # frce_scr_b = int(force_load_score_fourt[0])
        lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
        score_b_interim = int(rula_tableB_dict.get(lookup_ky, "0"))
        final_score_b =  score_b_interim # + muscle_scr_b + frce_scr_b
        
        upr_arm_scr = int(upper_arm_pos_ids_description.get(upper_arm_score)) + int(score_ids_adjust_description.get(shoulder_raised)) + int(score_ids_adjust_description.get(upper_arm_abducted)) - int(score_ids_adjust_description.get(upper_arm_supported))
        lwr_arm_scr = int(lower_arm_pos_ids_description.get(lower_arm_score)) + int(score_ids_adjust_description.get(lower_arm_moving_score))
        wrst_scr = int(wrist_pos_ids_rula_description.get(wrist_score)) + int(wrist_pos_adjust_description.get(wrist_adjust))
        wrst_twstd_scr = int(wrist_twist_pos_ids_description.get(wrist_score_twisted))
        muscle_scr = int(muscle_score_ids_description.get(muscle_use_score))
        # frce_scr = int(force_load_score[0])

        lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}{"_"}{str(wrst_twstd_scr)}'
        score_a_interim = int(rula_tableA_dict.get(lookup_ky, "0"))
        final_score_a = score_a_interim + muscle_scr # + frce_scr

        lookup_ky = f'{str(final_score_a)}{"_"}{str(final_score_b)}'
        final_score_c = int(rula_tableC_dict.get(lookup_ky, "0"))
        
        rula_score = final_score_c

        rula_temp = output_template_rula.copy()

        rula_temp['Participant_ID'] = par_id
        rula_temp['Assessment'] = assessment
        rula_temp['Procedure_and_Mouth_Quadrant'] = procedure_id
        rula_temp['Variable_ID'] = f'{par_id}{assessment}{procedure_id}'
        rula_temp['Step_1:_Locate_upper_arm_position'] = int(upper_arm_pos_ids_description.get(upper_arm_score))
        rula_temp['If_shoulder_is_raised'] = int(score_ids_adjust_description.get(shoulder_raised))
        rula_temp['If_upper_arm_is_abducted'] = int(score_ids_adjust_description.get(upper_arm_abducted))
        rula_temp['If_arm_is_supported_or_person_is_leaning'] = int(score_ids_adjust_description.get(upper_arm_supported))
        rula_temp['Step_1_score'] = upr_arm_scr
        rula_temp['Step_2:_Locate_lower_arm_position'] = int(lower_arm_pos_ids_description.get(lower_arm_score)) 
        rula_temp['If_either_arm_is_working_across_midline_or_out_to_side_of_body'] = int(score_ids_adjust_description.get(lower_arm_moving_score))
        rula_temp['Step_2_score'] = lwr_arm_scr
        rula_temp['Step_3:_Locate_wrist_position'] = int(wrist_pos_ids_rula_description.get(wrist_score))
        rula_temp['If_wrist_is_bent_from_midline'] = int(wrist_pos_adjust_description.get(wrist_adjust))
        rula_temp['Wrist_score'] = wrst_scr
        rula_temp['Step_4:_Wrist_twist._Wrist_Twist_Score'] = wrst_twstd_scr
        rula_temp['Step_5:_Look_Posture_Score_in_Table_A'] = score_a_interim
        rula_temp['Step_6:_Add_muscle_use_score'] = muscle_scr
        rula_temp['Step_7:_Add_force_load_score'] = None #frce_scr
        rula_temp['Step_8'] = final_score_a
        rula_temp['Step_9:_Locate_neck_position'] = int(neck_score_ids_rula_description.get(neck_score))
        rula_temp['If_neck_is_twisted'] = int(score_ids_adjust_description.get(neck_twisted))
        rula_temp['If_neck_is_side_bending'] = int(score_ids_adjust_description.get(neck_bending))
        rula_temp['Neck_score'] = nck_scr
        rula_temp['Step_10:_Locate_trunk_posture'] = int(trunk_posture_score_ids_rula_description.get(trunk_posture_score))
        rula_temp['If_trunk_is_twisted'] = int(score_ids_adjust_description.get(trunk_twisted))
        rula_temp['If_trunk_is_side_bending'] = int(score_ids_adjust_description.get(trunk_bending))
        rula_temp['Trunk_score'] = trnck_scr
        rula_temp['Step_11:_Legs._Leg_score'] = leg_scr
        rula_temp['Step_12:_Look-up_posture_score_in_Table_B_Posture_B_Score'] = score_b_interim
        rula_temp['Step_13:_Add_Muscle_Use_Score'] = None #muscle_scr_b
        rula_temp['Step_14:_Add_Force_Lead_Score'] = None #frce_scr_b
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

##### REBA

# @callback(
#     Output("collapse-force-load-score", "is_open"),
#     [Input("collapse-button-force-load-score", "n_clicks")],
#     [State("collapse-force-load-score", "is_open")],
# )
# def toggle_collapse_force_load_score_reba(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-upper-arm-score", "is_open"),
#     [Input("collapse-button-upper-arm-score", "n_clicks")],
#     [State("collapse-upper-arm-score", "is_open")],
# )
# def toggle_collapse_upper_arm_score_reba(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-lower-arm-score", "is_open"),
#     [Input("collapse-button-lower-arm-score", "n_clicks")],
#     [State("collapse-lower-arm-score", "is_open")],
# )
# def toggle_collapse_lower_arm_score_reba(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-wrist-score", "is_open"),
#     [Input("collapse-button-wrist-score", "n_clicks")],
#     [State("collapse-wrist-score", "is_open")],
# )
# def toggle_collapse_wrist_score_reba(n, is_open):
#     if n:
#         return not is_open
#     return is_open

# @callback(
#     Output("collapse-coupling-score", "is_open"),
#     [Input("collapse-button-coupling-score", "n_clicks")],
#     [State("collapse-coupling-score", "is_open")],
# )
# def toggle_collapse_coupling_score_reba(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@callback(
    Output("fade-a", "is_in"),
    [Input("fade-button-a", "n_clicks")],
    [State("fade-a", "is_in")],
)
def toggle_fade_a_reba(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

@callback(
    Output("fade-b", "is_in"),
    [Input("fade-button-b", "n_clicks")],
    [State("fade-b", "is_in")],
)
def toggle_fade_b_reba(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

###### disable neck dropdown #######
# @callback(
#     [Output("neck-twisted", "disabled"),
#      Output("neck-bending", "disabled"),
#      Output("neck-twisted", "value"),
#     Output("neck-bending", "value")],
#     [Input("neck-twisted", "value"), Input("neck-bending", "value")],
# )
# def neck_adjust_reba(nck_twisted, nck_bending):

#     if nck_twisted in [None, ''] or nck_bending in [None, '']:
#         return False, False, '0', '0'

#     if nck_twisted[0] in ['1', 1]:
#         return False, True, '1', '0'
#     elif nck_bending[0] in ['1', 1]:
#         return True, False, '0', '1'
#     else:
#         return False, False, '0', '0'

###### disable trunk dropdown #######
# @callback(
#     [Output("trunk-twisted", "disabled"),
#      Output("trunk-bending", "disabled"),
#      Output("trunk-twisted", "value"),
#     Output("trunk-bending", "value")],
#     [Input("trunk-twisted", "value"), Input("trunk-bending", "value")],
# )
# def trunk_adjust_reba(trnk_twisted, trnk_bending):

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
    [Output("table-a-out-one", "children"),
     Output("table-a-out-two", "children"),], 
    [Input("neck-score", "value"),
     Input("neck-twisted", "value"),
    # Input("neck-bending", "value"),
     Input("trunk-posture-score", "value"),
     Input("trunk-twisted", "value"),
    # Input("trunk-bending", "value"),
     Input("leg-posture-score", "value"),
    Input("leg-posture-adjust", "value"),
     Input("force-load-score", "value"),
    Input("force-adjust", "value"),
     Input("fade-button-a", "n_clicks")],
    prevent_initial_call=True,
)
def table_a_reba(neck_score, neck_twisted, trunk_posture_score, trunk_twisted, leg_posture_score, leg_posture_adjust, force_load_score, force_adjust, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if neck_score in [None, ""]:
        return no_update

    if trunk_posture_score in [None, ""]:
        return no_update
    
    if leg_posture_score in [None, ""]:
        return no_update
    
    # if force_load_score in [None]:
    #     return no_update
    
    str_one = "The score for section A, based on the REBA table, and steps 1-3, is: "
    str_two = "The total score for section A, after adding the force/load score, is: "

    assets_table_a = 'assets/data/reba_tableA.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_a) as f:
        reba_tableA_dict = json.load(f)
    
    if trigger_id == 'fade-button-a':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if neck_score not in [None] and trunk_posture_score not in [None] and leg_posture_score not in [None]:
            # print(reba_tableA_dict)
            # print(neck_score[0], trunk_posture_score[0], leg_posture_score[0], force_load_score[0])

            nck_scr = int(neck_score_ids_description.get(neck_score)) + int(neck_score_ids_adjust_description.get(neck_twisted))
            trnck_scr = int(trunk_posture_score_ids_description.get(trunk_posture_score)) + int(trunk_posture_ids_adjust_description.get(trunk_twisted))
            leg_scr = int(leg_posture_score_ids_description.get(leg_posture_score)) + int(leg_posture_score_adjust_description.get(leg_posture_adjust))
            # frce_scr = int(force_load_score[0]) + int(force_adjust[0])

            lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
            final_score = int(reba_tableA_dict.get(lookup_ky, "0"))# + frce_scr
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
def table_b_reba(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, wrist_score, wrist_adjust, coupling_score, n_clicks_show_res):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'

    if upper_arm_score in [None, ""]:
        return no_update

    if lower_arm_score in [None, ""]:
        return no_update
    
    if wrist_score in [None, ""]:
        return no_update
    
    str_one = "The score for section B, based on the REBA table, and steps 7-11, is: "
    str_two = "The total score for section B, after adding the coupling score, is: "

    assets_table_b = 'assets/data/reba_tableB.json' ###UpperArmScore_1|LowerArm_1|Wrist_1

    with open(assets_table_b) as f:
        reba_tableB_dict = json.load(f)

    if trigger_id == 'fade-button-b':
        ### Neck_1|TrunkPostureScore_1|Legs_1
        if upper_arm_score not in [None] and lower_arm_score not in [None] and wrist_score not in [None] and coupling_score not in [None]:

            upr_arm_scr = int(upper_arm_pos_ids_description.get(upper_arm_score)) + int(score_ids_adjust_description.get(shoulder_raised)) + int(score_ids_adjust_description.get(upper_arm_abducted)) - int(score_ids_adjust_neg_description.get(upper_arm_supported))
            lwr_arm_scr = int(lower_arm_pos_ids_description.get(lower_arm_score))
            wrst_scr = int(wrist_pos_ids_description.get(wrist_score)) + int(wrist_pos_adjust_description.get(wrist_adjust))
            coup_scr = int(coupling_score_ids_description.get(coupling_score))

            lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}'
            final_score = int(reba_tableB_dict.get(lookup_ky, "0")) + coup_scr
            return f'{str_one}{reba_tableB_dict.get(lookup_ky, "0")}', f'{str_two}{final_score}'
        else:
            return no_update
    else:
        return "", ""

# ************************  callback Table B *****************************
@callback(
    [Output("badge-a-reba", "children"),
     Output("badge-b-reba", "children"),
     Output("badge-c-reba", "children"),
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
    # Input("neck-bending", "value"),
     Input("trunk-posture-score", "value"),
     Input("trunk-twisted", "value"),
    # Input("trunk-bending", "value"),
     Input("leg-posture-score", "value"),
    Input("leg-posture-adjust", "value"),
     Input("force-load-score", "value"),
    Input("force-adjust", "value"),
    Input("activity-score-one", "value"),
     Input("activity-score-two", "value"),
    Input("activity-score-three", "value"),
    Input("date-change", "date"),
    Input("par-id", "value"),
    Input("procedure-id", "value"),
    ],
    # prevent_initial_call=True,
)
def table_c_reba(upper_arm_score, shoulder_raised, upper_arm_abducted, upper_arm_supported, lower_arm_score, wrist_score, wrist_adjust, coupling_score, neck_score, neck_twisted, trunk_posture_score, trunk_twisted, leg_posture_score, leg_posture_adjust, force_load_score, force_adjust, act_scr_one, act_scr_two, act_scr_three, date_value, par_id, procedure_id):

    trigger_id = dash.ctx.triggered_id if not None else 'No clicks yet'
    assessment = 'RE'
    file_path_stem = '/reba/'

    print("neck_score", neck_score)
    if neck_score in [None, ""]:
        return no_update

    if trunk_posture_score in [None, ""]:
        return no_update
    
    if leg_posture_score in [None, ""]:
        return no_update
    
    # if force_load_score in [None]:
    #     return no_update
    
    if upper_arm_score in [None, ""]:
        return no_update

    if lower_arm_score in [None, ""]:
        return no_update
    
    if wrist_score in [None, ""]:
        return no_update
    
    if date_value in [None, ""]:
        return no_update
    
    if par_id in [None, ""]:
        return no_update
    
    if procedure_id in [None, ""]:
        return no_update
    
    str_one = "The total REBA score, based on Table C and the Activity Score, is: "

    assets_table_a = 'assets/data/reba_tableA.json' ### Neck_1|TrunkPostureScore_1|Legs_1

    with open(assets_table_a) as f:
        reba_tableA_dict = json.load(f)

    assets_table_b = 'assets/data/reba_tableB.json' ### UpperArmScore_1|LowerArm_1|Wrist_1

    with open(assets_table_b) as f:
        reba_tableB_dict = json.load(f)
    
    assets_table_c = 'assets/data/reba_tableC.json' ### ScoreA_1|ScoreB_1

    with open(assets_table_c) as f:
        reba_tableC_dict = json.load(f)

    if upper_arm_score not in [None] and lower_arm_score not in [None] and wrist_score not in [None] and coupling_score not in [None] and neck_score not in [None] and trunk_posture_score not in [None] and leg_posture_score not in [None]:
        # nck_scr = int(neck_score[0]) + int(neck_twisted[0]) + int(neck_bending[0])
        # trnck_scr = int(trunk_posture_score[0]) + int(trunk_twisted[0]) + int(trunk_bending[0])
        # leg_scr = int(leg_posture_score[0]) + int(leg_posture_adjust[0])

        nck_scr = int(neck_score_ids_description.get(neck_score)) + int(neck_score_ids_adjust_description.get(neck_twisted))
        trnck_scr = int(trunk_posture_score_ids_description.get(trunk_posture_score)) + int(trunk_posture_ids_adjust_description.get(trunk_twisted))
        leg_scr = int(leg_posture_score_ids_description.get(leg_posture_score)) + int(leg_posture_score_adjust_description.get(leg_posture_adjust))
         
        # frce_scr = int(force_load_score[0]) + int(force_adjust[0])
        lookup_ky = f'{str(nck_scr)}{"_"}{str(trnck_scr)}{"_"}{str(leg_scr)}'
        score_a_interim = int(reba_tableA_dict.get(lookup_ky, "0"))
        final_score_a = score_a_interim# + frce_scr
        
        # upr_arm_scr = int(upper_arm_score[0]) + int(shoulder_raised[0]) + int(upper_arm_abducted[0]) - int(upper_arm_supported[0])
        # lwr_arm_scr = int(lower_arm_score[0])
        # wrst_scr = int(wrist_score[0]) + int(wrist_adjust[0])
        # coup_scr = int(coupling_score[0])
        upr_arm_scr = int(upper_arm_pos_ids_description.get(upper_arm_score)) + int(score_ids_adjust_description.get(shoulder_raised)) + int(score_ids_adjust_description.get(upper_arm_abducted)) - int(score_ids_adjust_neg_description.get(upper_arm_supported))
        lwr_arm_scr = int(lower_arm_pos_ids_description.get(lower_arm_score))
        wrst_scr = int(wrist_pos_ids_description.get(wrist_score)) + int(wrist_pos_adjust_description.get(wrist_adjust))
        coup_scr = int(coupling_score_ids_description.get(coupling_score))
        
        lookup_ky = f'{str(upr_arm_scr)}{"_"}{str(lwr_arm_scr)}{"_"}{str(wrst_scr)}'
        score_b_interim = int(reba_tableB_dict.get(lookup_ky, "0"))
        final_score_b = score_b_interim + coup_scr

        lookup_ky = f'{str(final_score_a)}{"_"}{str(final_score_b)}'
        final_score_c = int(reba_tableC_dict.get(lookup_ky, "0"))

        reba_score = final_score_c + int(score_ids_adjust_description.get(act_scr_one)) + int(score_ids_adjust_description.get(act_scr_two)) + int(score_ids_adjust_description.get(act_scr_three))
       
        reba_temp = output_template_reba.copy()

        reba_temp['Participant_ID'] = par_id
        reba_temp['Assessment'] = assessment
        reba_temp['Procedure_and_Mouth_Quadrant'] = procedure_id
        reba_temp['Variable_ID'] = f'{par_id}{assessment}{procedure_id}'
        reba_temp['Step_1:_Locate_the_neck_position'] = int(neck_score_ids_description.get(neck_score))
        reba_temp['If_neck_is_twisted'] = int(neck_score_ids_adjust_description.get(neck_twisted))
        reba_temp['If_neck_is_side_bending'] = None #int(neck_bending[0])
        reba_temp['Neck_score'] = nck_scr
        reba_temp['Step_2:_Locate_trunk_position'] = int(trunk_posture_score_ids_description.get(trunk_posture_score))
        reba_temp['If_trunk_is_twisted'] = int(trunk_posture_ids_adjust_description.get(trunk_twisted))
        reba_temp['If_trunk_is_side_bending'] = None #int(trunk_bending[0])
        reba_temp['Trunk_Posture_score'] = trnck_scr
        reba_temp['Step_3:_Legs'] = int(leg_posture_score_ids_description.get(leg_posture_score))
        reba_temp['step_3_Adjust'] = int(leg_posture_score_adjust_description.get(leg_posture_adjust))
        reba_temp['Leg_Score'] = leg_scr
        reba_temp['Step_4:_Look-up_Posture_Score_in_Table_A._Posture_Score_A'] = score_a_interim
        reba_temp['Step_5:_Add_fore_load_score'] = None #int(force_load_score[0])
        reba_temp['If_shock_or_rapid_build_up_of_force'] = None #int(force_adjust[0])
        reba_temp['Force_Load_score'] = None #frce_scr
        reba_temp['Step_6:_Score_A,_Find_Row_in_Table_C_(Steps_4+5_scores)._Score_A'] = final_score_a
        reba_temp['Step_7:_Locate_upper_arm_position'] = int(upper_arm_pos_ids_description.get(upper_arm_score))
        reba_temp['If_shoulder_is_raised'] =  int(score_ids_adjust_description.get(shoulder_raised))
        reba_temp['If_upper_arm_is_abducted'] = int(score_ids_adjust_description.get(upper_arm_abducted))
        reba_temp['If_arm_is_supported_or_person_is_leaning'] = int(score_ids_adjust_neg_description.get(upper_arm_supported))
        reba_temp['Upper_arm_score'] = upr_arm_scr
        reba_temp['Step_8:_Locate_lower_arm_position'] = lwr_arm_scr
        reba_temp['Step_9:_Locate_wrist_posture'] = int(wrist_pos_ids_description.get(wrist_score))
        reba_temp['If_wrist_is_bent_from_midline_or_twisted'] = int(wrist_pos_adjust_description.get(wrist_adjust))
        reba_temp['Wrist_posture_score'] = wrst_scr
        reba_temp['Step_10:_Look-up_posture_score_in_Table_B._Postue_Score_B'] = score_b_interim
        reba_temp['Step_11:Add_coupling_score_Coupling_Score'] = coup_scr
        reba_temp['Step_12:_Score_B,_Find_column_in_Table_C._Score_B'] = final_score_b
        reba_temp['Table_C_Score'] = final_score_c
        reba_temp['1_or_more_body_parts_are_held_for_longer_than_1_minute_(static)'] = int(score_ids_adjust_description.get(act_scr_one))
        reba_temp['Repeat_small_range_actions_more_than_4X_per_minute)'] = int(score_ids_adjust_description.get(act_scr_two))
        reba_temp['Action_causes_rapid_large_range_changes_in_postures_or_unstable_base'] = int(score_ids_adjust_description.get(act_scr_three))
        reba_temp['Activity_score'] = int(score_ids_adjust_description.get(act_scr_one)) + int(score_ids_adjust_description.get(act_scr_two)) + int(score_ids_adjust_description.get(act_scr_three))
        reba_temp['REBA_Score'] = reba_score

        if reba_score < 2:
            reba_conclusion = 'Negligible risk' ### 1-2: Negligible risk 
        elif reba_score >= 2 and reba_score <=3:
            reba_conclusion = 'Low risk. Change may be needed' ### 2-3: Low risk. Change may be needed 
        elif reba_score >= 4 and reba_score <=7:
            reba_conclusion = 'Medium risk. Further investigate. Change soon' ### 4-7: Medium risk. Further investigate. Change soon. 
        elif reba_score >= 8 and reba_score <=10:
            reba_conclusion = 'High risk. Investigate and implement change' ### 8-10: High risk. Investigate and implement change 
        elif reba_score >= 11:
            reba_conclusion = 'Very high risk. Implement change' ### 11+: Very high risk. Implement change
        
        reba_temp['REBA_Score_conclusion'] = reba_conclusion
        reba_temp['date_assessed'] = date_value

        # file_name = f'{file_path_stem}{par_id}{assessment}{procedure_id}{".json"}'
        # data = dbx_cls.dictionary_to_bytes(reba_temp, 'utf-8')
        # dbx_cls.add_to_dropbox(data, file_name)

        return [str(final_score_a)], [str(final_score_b)], [str(final_score_c)], f'{str_one}{str(reba_score)}'
    
    else:
        return no_update