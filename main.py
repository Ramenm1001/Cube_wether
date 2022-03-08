from flask import Flask, request, jsonify
import os
import json
app = Flask(__name__)


@app.route('/')
def main():
    resp = {"температура": 15,
            "освещенность": 150,
            "ну и еще немного": 200}
    return json.dumps(resp)


@app.route('/test'):
def test():
    return "OK"


@app.route('/postjson', methods=['POST'])
def postjson():
    return jsonify(request.json) 

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
