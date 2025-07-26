from flask import Flask, redirect, request
import requests

app = Flask(__name__)

def get_active_env():
    try:
        with open('active_env.txt', 'r') as f:
            env = f.read().strip()
            return env if env in ['blue', 'green'] else 'blue'
    except:
        return 'blue'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def route_traffic(path):
    active_env = get_active_env()
    port = 5000 if active_env == 'blue' else 5001
    url = f'http://localhost:{port}/{path}'  # <-- Corrected f-string

    try:
        response = requests.get(url, params=request.args, timeout=5)
        return response.text, response.status_code
    except Exception as e:
        return f"Error routing to {active_env} environment: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)