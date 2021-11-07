"""
==========
Javascript
==========
Example of writing JSON format graph data and using the D3 Javascript library
to produce an HTML/Javascript drawing.
You will need to download the following directory:
- https://github.com/networkx/networkx/tree/main/examples/external/force
"""
import json

import flask
import networkx as nx
from graph import build_json

build_json()

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")


@app.route("/")
def static_proxy():
    return app.send_static_file("force.html")


print("\nGo to http://localhost:8000 to see the example\n")
app.run(port=8000)