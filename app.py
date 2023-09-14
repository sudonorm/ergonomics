import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
import os
from sys import platform as pltfrm_type
import sys
home_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(home_dir)
from Pages import index, rula

PROD = True
DEBUG_MODE = False ### this should only be set to true when developing and not in production

if pltfrm_type in ['win32', 'cygwin', 'darwin']:
    PROD = False
    DEBUG_MODE = True

app = Dash(__name__, use_pages=True, pages_folder="", external_stylesheets=[dbc.themes.FLATLY],
            meta_tags=[{'name': 'viewport',
                                        'content': 'width=device-width, initial-scale=1.0'}], url_base_pathname="/ergo_questionaire/")

dash.register_page("index", path='/', layout=index.layout, name='Reba-Rula')
dash.register_page("rula", layout=rula.layout, name='Rula')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("REBA", href="/ergo_questionaire")),
        dbc.NavItem(dbc.NavLink("RULA", href="/ergo_questionaire/rula")),
        
    ],
    #brand="NavbarSimple",
    #brand_href="#",
    links_left=True,
    color="primary",
    dark=True,
)

# elements = []
# for pg in dash.page_registry:
#     data = dash.page_registry[pg]['layout']
#     try:
#         for i in data:
#             elements.append(i)
#     except:
#         pass


# data = dash.get_app().layout

# try:
#     for i in data:
#         elements.append(i)
# except:
#     pass

# print(elements)

app.layout = html.Div([

    dbc.Row([
       dbc.Col([
           navbar
       ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Container(dash.page_container, fluid=True),
        ])
    ])
])

if not PROD:
    if __name__ == "__main__":
        app.run(debug=DEBUG_MODE, port= 8999)
