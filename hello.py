import argparse
import os
from flask import Flask, render_template, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api
import json


app = Flask(__name__)

@app.route('/')
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

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask-RESTapi"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.register_blueprint(request_api.get_blueprint())

@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)

    
if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Python-Flask-RESTapi")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    if ARGS.debug:
        print("Running in debug mode")
        app.run(host='localhost', port=PORT, debug=True)
    else:
        app.run(host='localhost', port=PORT, debug=False)