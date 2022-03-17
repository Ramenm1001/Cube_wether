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
test_data = "Ничего"

@app.route('/')
def main(methods=['GET']):
    resp = {"temperature": 15,
            "light": 150,
            "smth": 200}
    return json.dumps(resp)

@app.route('/data')
def data():
    global data
    return data


@app.route('/postjson', methods=['POST'])
def postjson():
    file_json = jsonify(request.json)
    global data
    data = jsonify(request.json)
    return jsonify(request.json)


@app.route('/savetxt')
def savetxt():
    with open('123.txt', 'w') as file:
        file.write("123321")
    file.close()
    return "OK"

@app.route('/postdata', methods=['POST']))
def postdata():
    global test_data
    test_data = request.json
    return test_data


@app.route('/testdata')
def testdata():
    global test_data
    return test_data

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
