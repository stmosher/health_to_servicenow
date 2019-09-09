import json
from threading import Thread

import requests
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


def post_to_snow(alert_dict):
    u = 'https://dev82732.service-now.com/api/now/table/x_397387_cw_alerts_alert_table'
    username = 'admin'
    password = 'XXX'

    headers = {'Accept': 'application/json',
               'Content-type': 'application/json'}

    r = requests.post(u, auth=(username, password), headers=headers, data=json.dumps(alert_dict))

    if r.status_code != 201:
        print('Web server communication error {}'.format(r.status_code))


def my_zip(list1, list2):
    md = dict()
    for i in list1:
        md[i] = list2[list1.index(i)]
    return md


def parse_alert_body(body):
    """
        This parses the body of the alert message, processes into simple dictionaries, and return a list
        of dictionaries composed of the seven key, value pairs as seen in the add_dicts dictionary
        below.
    """
    results = list()
    for a in body:
        for s in a['series']:
            columns_list = [c for c in s['columns']]
            for v1 in s['values']:
                values_list = [v for v in v1]
                z_dict = my_zip(columns_list, values_list)
                add_dict = {'producer': s['tags']['Producer'], 'kpi_id': s['tags']['kpi_id'],
                            'level': s['tags']['level'], 'state': s['tags']['state'], 'uuid': s['tags']['UUID'],
                            'time': z_dict['time'], 'id': z_dict['id'], 'msg': z_dict['msg']}
                results.append(add_dict)
    return results


def thread_waiter(alert):
    """
        This relieves Flask from waiting for action.
    """
    results = parse_alert_body(alert)  # results is list of dicts
    for i in results:
        post_to_snow(i)


@app.route('/health_to_snow', methods=['GET', 'POST'])
def health_to_snow():
    """
        Receive alert from crossworks, return status 200, and kick off thread for further processing
    """
    if request.method == 'GET':
        reply = 'Use the POST method'
        return reply
    elif request.method == 'POST':
        data = request.json
        Thread(target=thread_waiter, args=(data,)).start()
        return jsonify(data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
