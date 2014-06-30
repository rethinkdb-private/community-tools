#!/usr/bin/env python
import os, sys
import datetime, yaml, json
from flask import Flask, render_template, request
from flask.ext import assets
import requests

# Read in and process the configuration
def open_yaml(f):
    return open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f))
try:
    config = yaml.load(open_yaml('config.yaml'))
except IOError:
    print 'config.yaml missing -- no configuration file found (see config.example.yaml for a sample configuration.)'
    sys.exit()

# Make sure main directories we're logging to exist, error and exit if not
app_dir = os.path.dirname(os.path.abspath(__file__))
for log_dir in config['log_dirs']:
    if not os.path.exists(os.path.join(app_dir, log_dir)):
        print 'Log directory not found: ' + os.path.join(app_dir, log_dir)
        sys.exit()

# Initialize the Flask app and Flask-Assets

app = Flask(__name__)
assets_env = assets.Environment(app)

# Flask-Assets needs to know where our Sass and CoffeeScript files are
assets_env.load_path = [
    os.path.join(app_dir, 'static')
]

# Register JavaScript / CoffeeScript assets
assets_env.register(
    'js_all',
    assets.Bundle(
        'js/jquery-2.1.1.min.js',
        'js/DYMO.Label.Framework.1.2.6.js',
        assets.Bundle(
            'js/hestia.coffee',
            filters=['coffeescript']
        ),
        output='gen/app.js'
    )
)

assets_env.register(
    'css_all',
    assets.Bundle(
        'css/styles.scss',
        filters=['scss'],
        output='styles.css'
    )
)

@app.route('/')
def hestia():
    return render_template('hestia.html', event_name = config['event']['name'])

@app.route('/dymo-template', methods=['GET'])
def get_dymo_template():
    path = os.path.join(app_dir, config['dymo-template'])
    if os.path.isfile(path):
        with open(path) as f:
            return f.read().replace('\n', '')
    else:
        return 'No DYMO template found.'

@app.route('/logs', methods=['POST'])
def log_user():
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = config['event']['log_to']
    
    user = {
        'meetup': config['event']['name'],
        'date': date,
        'name': request.form.get('name', ''),
        'about': request.form.get('about', ''),
        'github': request.form.get('github', ''),
    }
    # Make sure we have a directory we can log to
    for log_dir in config['log_dirs']:
        log_dir = os.path.join(app_dir, log_dir)
        with open(os.path.join(log_dir, filename), 'a+') as f:
            out = json.dumps(user)
            f.write(out+'\n')

    r = requests.post('https://zapier.com/hooks/catch/w07io/', data=user)
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
