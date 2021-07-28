from flask import Flask, render_template, request, jsonify
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restplus import Api, Resource, fields

import json


app = Flask(__name__)
api = Api(app)



@app.route("/survey")
def hello_world():
    return render_template('survey.html')
@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        fileName = request.form["name"]
        fileName = fileName.replace(" ", "_")
        with open("./survey-results/"+fileName+".json", 'w') as f:
            json.dump(request.form, f, indent=6)
        return render_template('success.html')