from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Flask on port {port}...")
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
