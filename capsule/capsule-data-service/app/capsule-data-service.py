#!/usr/bin/env python
import os, sys
import datetime, yaml, json
from flask import Flask, render_template, request
import requests
from requests.auth import HTTPBasicAuth

STACKLEAD_TOKEN = 'ce16e873ff'

auth = HTTPBasicAuth(STACKLEAD_TOKEN, '')
stacklead_data = {}

# Read in and process the configuration
def open_yaml(f):
    return open(os.path.join(os.path.dirname(os.path.realpath(__file__)), f))
try:
    config = yaml.load(open_yaml('config.yaml'))
except IOError:
    print 'config.yaml missing -- no configuration file found (see config.example.yaml for a sample configuration.)'
    sys.exit()

app = Flask(__name__)

@app.route('/')
def capsule_toolkit():
    return json.dumps(stacklead_data)

@app.route('/stacklead/request')
def stacklead():
    email = request.args.get('email', '')
    if len(email) == 0:
        return 'HTTP 400: No email was provided.', 400
    # The token is a generated randomly client-side and used to track and retrieve the user data
    token = request.args.get('token', '')
    if len(token) == 0:
        return 'HTTP 400: No token was provided.', 400
    data = {
        'email': email,
        'delivery_method': 'webhook',
        'token': token,
    }

    req = requests.post('https://stacklead.com/api/leads', data=data, auth=auth)
    return ''

@app.route('/stacklead', methods=['POST'])
def stacklead_hook():
    d = request.json
    stacklead_data[d['token']] = d
    return ''

@app.route('/stacklead', methods=['GET'])
def get_lead():
    token = request.args.get('token', '')
    if len(token) == 0:
        return 'HTTP 400: No token was provided.', 400
    if token in stacklead_data:
        return json.dumps(stacklead_data[token])
    else:
        return "HTTP 404: User data with token %s not found." % token, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
