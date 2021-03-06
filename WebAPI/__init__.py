from flask import Flask, redirect, url_for, request, render_template
from Queries import countryQuery, heatMapQuery
import json
app = Flask(__name__)

@app.route('/')
def main_page():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/country', methods=['GET', 'POST'])
def country_information():
    try:
        country = ''
        year_from = 0
        year_to = 0
        metric = ''
        human_index = ''
        
        if request.method == 'GET':
            country = request.args.get('country')
            year_from = request.args.get('year_from')
            year_to = request.args.get('year_to')
            metric = request.args.get('metric')
            human_index = request.args.get('human_index')
        else:
            country = request.form.get('country')
            year_from = request.form.get('year_from')
            year_to = request.form.get('year_to')
            metric = request.form.get('metric')
            human_index = request.form.get('human_index')
        
        result = countryQuery(country, year_from, year_to, metric, human_index)
        
        return json.dumps(result)
    except Exception as e:
        return str(e)
    
@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    try:
        op = ''
        year_from = 0
        year_to = 0
        metric = ''
        human_index = ''
        
        if request.method == 'GET':
            year_from = request.args.get('year_from')
            year_to = request.args.get('year_to')
            metric = request.args.get('metric')
            human_index = request.args.get('human_index')
            op = request.args.get('op')
        else:
            year_from = request.form.get('year_from')
            year_to = request.form.get('year_to')
            metric = request.form.get('metric')
            human_index = request.form.get('human_index')
            op = request.form.get('op')
            
        result = heatMapQuery( year_from, year_to, metric, human_index, op)
        
        return json.dumps(result)
    except Exception as e:
        return str(e)
    
@app.route('/how_to_use')
def how_to_use():
    return "Explanation"

if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)

