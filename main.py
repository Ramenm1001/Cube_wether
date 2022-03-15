from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn_data = "155"
except Exception as e:
    conn_data = "55"

data = []
conn_data = "1"

@app.route('/')
def main(methods=['GET']):
    resp = {"temperature": 15,
            "light": 150,
            "smth": 200}
    return json.dumps(resp)


@app.route('/test')
def test():
    global conn_data
    return conn_data


@app.route('/data')
def test():
    global some_data
    global data
    return " ".join(data)


@app.route('/postjson', methods=['POST'])
def postjson():
    global some_data
    file_json = jsonify(request.json)
    global data
    data.append(jsonify(request.json))
    return some_data


@app.route('/savetxt')
def savetxt():
    with open('123.txt', 'w') as file:
        file.write("123321")
    file.close()
    return "OK"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
