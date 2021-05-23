#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify
app = Flask(__name__)

from moon_phases import moon
moon = moon(mock=False)

@app.route('/')
def index():
    moon.setPhase()
    moon_b, moon_r = moon.getImg_br()
    return jsonify({'moon_b': moon_b,
                    'moon_r': moon_r})

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80, debug=False)
    app.run()
