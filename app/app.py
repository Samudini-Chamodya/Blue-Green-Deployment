from flask import Flask, render_template
import os
import argparse

app = Flask(__name__)

@app.route('/')
def home():
    try:
        with open('version.txt', 'r') as f:
            version = f.read().strip()
    except FileNotFoundError:
        version = 'unknown'
    env = os.getenv('APP_ENV', 'unknown')
    return render_template('index.html', version=version, env=env)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=os.getenv('PORT', '5000'), type=int)
    parser.add_argument('--env', default=os.getenv('APP_ENV', 'unknown'))
    args = parser.parse_args()
    os.environ['APP_ENV'] = args.env
    app.run(host='0.0.0.0', port=args.port)