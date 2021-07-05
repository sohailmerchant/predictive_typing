"""API for IslamAtlas edge ngrams, for predictive typing.

The API returns a sorted list of ngrams (+ their counts: [[ngram, count], ])
that start with the characters provided to the API.

Run the API with command `python api.py` from the command line
to make it run on local server http://127.0.0.1:5000/

Example request:

http://127.0.0.1:5000/API/IslamAtlasNgrams?edge="الطول وال"


The API currently uses json dictionary,
but this should be replaced by a backend database. 

Based on https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
"""

import flask
from flask import request, jsonify
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

fp = "ngram_count_normalized_keys.json"
with open(fp, mode="r", encoding="utf-8") as file:
    edge_ngrams = json.load(file)

@app.route('/API/IslamAtlasNgrams', methods=['GET'])
def get_ngrams_for_edge():
    if "edge" in request.args:
        edge = request.args['edge'].strip()
        d = edge_ngrams[edge]
        res_array = [[k, v] for k,v in d.items()]
        # sort results first on count, then  on length, then alphabetically:
        sorted_res_array = sorted(res_array,
                                  key=lambda x: (x[1], len(x), x), 
                                  reverse=True)
        return jsonify(sorted_res_array)
    else:
        return "Error: no edge provided"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



app.run()
