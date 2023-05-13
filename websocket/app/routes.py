from flask import render_template
from flask import current_app as app
from flask import request
import json

@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Graph MSXV Telemetry Data',
        description='Fetches telemetry data and graphs it',
        template='home-template',
        body="This is a homepage served with Flask."
    )


@app.route('/test', methods=['POST'])
def test():
    """Landing page."""
    text = request.form['text']
    return text


@app.route('/input-data', methods=['POST'])
def append_data():
    data = request.data.decode("utf-8")
    json_data = json.loads(data)
    print(json_data)
    f = open('data.json')
    print("Microservice Data Received")
    json_file = json.load(f)
    json_file.update(json_data)
    json_file_str = json.dumps(json_file)
    with open('data.json', 'w') as output:
        output.write(json_file_str)

    return "success"