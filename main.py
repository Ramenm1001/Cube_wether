from flask import Flask
import os
import json
app = Flask(__name__)


@app.route('/')
def main():
    resp = {"температура": 15,
            "освещенность": 150,
            "ну и еще немного": 200}
    return json.dumps(resp)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
