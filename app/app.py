from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Read version from version.txt
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    # Get environment from environment variable
    env = os.getenv('APP_ENV', 'unknown')
    return render_template('index.html', version=version, env=env)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)