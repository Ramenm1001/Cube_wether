from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def main(methods=['GET']):
    resp = {"temperature": 15,
            "light": 150,
            "smth": 200}
    return json.dumps(resp)


@app.route('/test')
def test():
    global some_data
    return some_data


@app.route('/postjson', methods=['POST'])
def postjson():
    global some_data
    file_json = jsonify(request.json)
    some_data = jsonify(request.json) 
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
