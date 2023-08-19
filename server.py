from waitress import serve
import subprocess
import os
from sys import platform as pltfrm_type
from app import app

print("Dash should be running on http://127.0.0.1:8999/ergo_questionaire")
print("* Serving Flask app 'app'")
print("Press CTRL+C to quit")

server = app.server

# if pltfrm_type in ['win32', 'cygwin']:
#         subprocess.Popen("waitress-serve --listen=127.0.0.1:8999 app:app.server", shell=True, stdout=subprocess.PIPE, cwd=os.getcwd()).stdout.read()
# else:
#         subprocess.Popen("waitress-serve --port=8999 --url-scheme=https app:app.server", shell=True, stdout=subprocess.PIPE, cwd=os.getcwd()).stdout.read()