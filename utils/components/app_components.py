
import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc

class AppComponents:

    def create_text_area(self, component_id:str, placeholder:str) -> html.Div:

        text_area = html.Div(className='textareacontainer',
            children=[
                dbc.Textarea(id=component_id, className="mb-3", placeholder=placeholder, style={'width': '100%', 'height': '300px', 'overflowY': 'scroll'}),
               
            ]
        )

        return text_area
    
    def create_strain_index_ui(self, accordion_title:str, dpn_borg_intensity_id:str, dpn_items_borg_intensity:dict,
                               total_observations_id:str, total_number_of_exertion_id:str, duration_of_exertion_id:str,  
                               dpn_hand_wrist_id:str, dpn_items_hand_wrist:dict, dpn_speed_work_id:str, dpn_items_speed_work:dict, 
                               dpn_dur_task_per_day_id:str, dpn_items_dur_task_per_day:dict, strain_index_result_id:str):

        si_component = html.Div(
            children=[dbc.Accordion([ 
            
            dbc.AccordionItem([


                ## Intensity of Exertion (Borg Scale - BS)
                dbc.Accordion([ 
            
                    dbc.AccordionItem([

                        html.Label("Describe the intensity of exertion of performing the task based on the Borg scale", style={"marginBottom": 10}),

                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem("0-2: Light - Barely noticeable or relaxed effort"),
                                dbc.ListGroupItem("3: Somewhat hard - Noticeable or definite effort"),
                                dbc.ListGroupItem("4-5: Hard - Obvious effort, unchanged expression"),
                                dbc.ListGroupItem("6-7: Very hard - Substantial effort, changed expressions"),
                                dbc.ListGroupItem("8-10: Near maximal - Uses shoulder or trunk for force"),
                            ], style={"marginBottom": 10}
                        ),

                        dcc.Dropdown(
                                        id=dpn_borg_intensity_id,
                                        options=[{'label':k, 'value': v} for k,v in dpn_items_borg_intensity.items()],
                                        multi=False,
                                        value='',
                                        searchable=True,
                                        disabled=False
                                    ),
                        
                    ], title="Intensity of Exertion (Borg Scale - BS)",), 

                ],start_collapsed=True , style={"margin": 30}),

                ## Duration of Exertion (% of Cycle)
                dbc.Accordion([ 
            
                    dbc.AccordionItem([
                        
                        dbc.Accordion([ 
            
                            dbc.AccordionItem([
                                html.Label("What is the total observation or cycle time for the task (in seconds)?", style={"marginBottom": 10}),

                                dbc.Input(id=total_observations_id, placeholder="Type a number...", type="number"),
                            ], title="Total observation time (in seconds)",), 
                        ],start_collapsed=True , style={"margin": 30}),
                        # # 

                        dbc.Accordion([ 
                            dbc.AccordionItem([
                                    html.Label("What is the total number of exertions performed by the upper extremity in question?"),
                                    html.Br(),
                                    html.Label("Tip: Count the number of exertions that occur during an observation period", style={"marginBottom": 10}, className="fw-bold"),
                                    #
                                    dbc.Input(id=total_number_of_exertion_id, placeholder="Type a number...", type="number"),
                                ], title="Effort required for task",), 
                        ],start_collapsed=True , style={"margin": 30}),

                        #total-observations
                        #total-number-of-exertion
                        #duration-of-exertion
                        dbc.Accordion([  
                            dbc.AccordionItem([
                                html.Label("What is the duration of all the exertions performed by the upper extremity in question (in seconds)?"),
                                html.Br(),
                                html.Label("Tip: Measure the duration of all exertions performed by the left upper extremity during an observation period", style={"marginBottom": 10}, className="fw-bold"),
                                dbc.Input(id=duration_of_exertion_id, placeholder="Type a number...", type="number"),
                            ], title="Duration of Exertion (in seconds)",), 

                        ],start_collapsed=True , style={"margin": 30}),
                        
                    ], title="Duration of Exertion (% of Cycle)",), 

                ],start_collapsed=True , style={"margin": 30}),

                ## Hand or Wrist Posture
                dbc.Accordion([ 
            
                    dbc.AccordionItem([

                        html.Label("Describe the hand or wrist posture while performing the task in relation to neutral position"),
                        dcc.Dropdown(
                                        id=dpn_hand_wrist_id,
                                        options=[{'label':k, 'value': v} for k,v in dpn_items_hand_wrist.items()],
                                        multi=False,
                                        value='',
                                        searchable=True,
                                        disabled=False
                                    ),
                        
                    ], title="Hand or Wrist Posture",), 

                ],start_collapsed=True , style={"margin": 30}),

                ## Speed of Work
                dbc.Accordion([ 
            
                    dbc.AccordionItem([

                        html.Label("Describe the speed of performing the task or how fast the participant is working"),
                        dcc.Dropdown(
                                        id=dpn_speed_work_id,
                                        options=[{'label':k, 'value': v} for k,v in dpn_items_speed_work.items()],
                                        multi=False,
                                        value='',
                                        searchable=True,
                                        disabled=False
                                    ),
                        
                    ], title="Speed of Work",), 

                ],start_collapsed=True , style={"margin": 30}),

                ## Duration of Task Per Day (hours)
                dbc.Accordion([ 
            
                    dbc.AccordionItem([
                        
                        html.Label("Number of hours performing the task"),
                        dcc.Dropdown(
                                        id=dpn_dur_task_per_day_id,
                                        options=[{'label':k, 'value': v} for k,v in dpn_items_dur_task_per_day.items()],
                                        multi=False,
                                        value='',
                                        searchable=True,
                                        disabled=False
                                    ),
                        
                    ], title="Duration of Task Per Day (hours)",), 

                ],start_collapsed=True , style={"margin": 30}),


            dbc.Card(
                dbc.CardBody(children=[
                    html.P(
                        "The total Strain Index is: ", id = strain_index_result_id, className="card-text-sec-a"
                    ),
                    ]
                )
                , style={"margin": 30}),

            ], title=accordion_title,), 

        ],start_collapsed=True , style={"margin": 30}),

        ]
        )

        return si_component