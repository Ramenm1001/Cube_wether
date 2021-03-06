from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')


data = []
data1 = []


@app.route('/')
def main():
    resp = {"RoomsReadings":
                {"Комната 1":
                     [
                         {"Единица измерения": "мг/м³", "Знаечние измерения": 6.54, "Название величины": "Монооксид углерода"},
                         {"Единица измерения": "Проценты", "Знаечние измерения": 8.46, "Название величины": "Влажность"},
                         {"Единица измерения": "Люкс", "Знаечние измерения": 5.46, "Название величины": "Освещённость"},
                         {"Единица измерения": "мг/м³", "Знаечние измерения": 12, "Название величины": "Метан"},
                         {"Единица измерения": "мг/м³", "Знаечние измерения": 14, "Название величины": "Дым"},
                         {"Единица измерения": "Градусы Цельсия", "Знаечние измерения": 29.7, "Название величины": "Температура"}
                     ],
                "Комната 2":
                    [
                        {"Единица измерения": "мг/м³", "Знаечние измерения": 0, "Название величины": "Монооксид углерода"},
                        {"Единица измерения": "Проценты", "Знаечние измерения": 0, "Название величины": "Влажность"},
                        {"Единица измерения": "Люкс", "Знаечние измерения": 0, "Название величины": "Освещённость"},
                        {"Единица измерения": "мг/м³", "Знаечние измерения": 0, "Название величины": "Метан"},
                        {"Единица измерения": "мг/м³", "Знаечние измерения": 0, "Название величины": "Дым"},
                        {"Единица измерения": "Градусы Цельсия", "Знаечние измерения": 0, "Название величины": "Температура"}
                    ]
                },
            "Название организации": "Дом Ивана"}
    return resp


@app.route('/data')
def get_data():
    global data
    return data


@app.route('/data1')
def get_data1():
    global data1
    return data1


@app.route('/organization_list')
def get_organization_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM public."Organization"')
    return jsonify([x[0] for x in cur.fetchall()])


@app.route('/postjson', methods=['POST'])
def postjson():
    json_as_dict = request.json
    # open connect for insert new data in DB
    conn = get_db_connection()
    cur = conn.cursor()

    # getting organization name from JSON
    org_name = json_as_dict["Organization_name"]
    # old code for correct return data at /data
    global data
    data = jsonify(json_as_dict)

    # all commented prints just for better code understanding
    # print("0", json_as_dict)
    # key is a name of room OR name of organization
    for key in json_as_dict:
        sub_dict = json_as_dict[key]
        # print("1", sub_dict)
        # if key is room name its key of dict with readings values
        if type(sub_dict) is dict:
            # finding id of sensor from room name and organization name
            cur.execute('SELECT id_sensor '
                        'FROM public."Sensor" INNER JOIN public."Organization" '
                        'on public."Sensor".organization_id = public."Organization".id_organization '
                        'WHERE public."Sensor".name = ' + '\''+key+'\'' +
                        ' and public."Organization".name = ' + '\''+org_name+'\'')
            id_sensor = cur.fetchall()
            # print("2", *id_sensor[0])
            # inserting data in DB (Sensor_Readings table; id is autoincrement)
            cur.execute('INSERT INTO public."Sensor_Readings" '
                        '(Carbon_Monoxide, Humidity, Light_Lux, Methane, Smoke, Temperature_C, Sensor_id) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (sub_dict['CarbonMonoxide'], sub_dict['Humidity'], sub_dict['LightLux'], sub_dict['Methane'],
                         sub_dict['Smoke'], sub_dict['TemperatureC'], *id_sensor[0]))
    # all changes approve
    conn.commit()
    # and close connection
    cur.close()
    conn.close()
    # old code for correct return data at /data
    return data


@app.route('/postjson1', methods=['POST'])
def postjson1():
    file_json = jsonify(request.json)
    global data1
    data1 = jsonify(request.json)
    return jsonify(request.json)


@app.route('/savetxt')
def savetxt():
    with open('123.txt', 'w') as file:
        file.write("123321")
    file.close()
    return "OK"


@app.route('/opentxt')
def opentxt():
    txt = ""
    for i in open('123.txt', 'r'):
        txt += i
    return txt


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=port)
