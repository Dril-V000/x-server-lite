import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

SERVER_URL = os.environ.get("SERVER_URL")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY")

@app.route('/config', methods=['GET'])
def get_config():
    if request.headers.get("X-Internal-Key") != INTERNAL_KEY:
        abort(403)
    return jsonify({
        "SERVER_URL": SERVER_URL,
        "AUTH_TOKEN": AUTH_TOKEN
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
