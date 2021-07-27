from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)

@app.route("/")
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