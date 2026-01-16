#!/usr/bin/env python3
import os
import json
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/data')
def get_data():
    with open('database.json', 'r', encoding='utf-8') as f:
        return send_file('database.json', mimetype='application/json')

@app.route('/<path:path>')
def serve_files(path):
    try:
        return send_file(path)
    except:
        return send_file('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
