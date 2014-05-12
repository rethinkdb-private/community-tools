#!/usr/bin/env python
import os
from flask import Flask, render_template
#from flask.ext.assets import Environment, Bundle
from flask.ext import assets

app = Flask(__name__)
assets_env = assets.Environment(app)

# Flask-Assets needs to know where our Sass and CoffeeScript files are
app_dir = os.path.dirname(__file__)
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

@app.route("/")
def hestia():
    return render_template('hestia.html')

if __name__ == "__main__":
    app.run(debug=True)
