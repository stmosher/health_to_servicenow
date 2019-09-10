#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""


import logging
from threading import Thread

from flask import Flask
from flask import jsonify
from flask import request

from h_s_classes.health_insights import HealthInsights
from h_s_classes.snow import Snow

app = Flask(__name__)



def thread_worker(alert):
    """Processes alerts and creates Service Now ticket

    Parameters
    ----------
    alert : list
        body from incoming HTTP POST request

    Logic
    -------
    Process alert into list of dictionaries
    Iterate through dictionies list
        POST ticket to Service Now per alert dictionary

    Returns
    -------
    None
    """
    logger = logging.getLogger(__name__)
    my_health_insights = HealthInsights()
    results = my_health_insights.parse_alert_body(alert)


    if results:
        my_snow = Snow(username='admin',
                       password='GKt12iZBsYhr',
                       url='https://dev82732.service-now.com',
                       post_ticket='/api/now/table/x_397387_cw_alerts_alert_table')
        for i in results:
            if i['state'] != 'clear':
                my_snow.p_create_ticket(body_data=i)
    else:
        logger.warning('Unable to parse message body in POST from {ip}.'.format(ip=request.remote_addr))
        return
    return


@app.route('/health_to_snow', methods=['GET', 'POST'])
def health_to_snow():
    """Flask web server receives http requests and executes worker thread if needed

    Parameters
    ----------
    HTTP POST request

    Logic
    -------
    if POST body match
        Start worker thread for further action

    Returns
    -------
    HTTP Response 200
        Proper HTTP status code and echos payload from POST request body
    """
    logger = logging.getLogger(__name__)
    if request.method == 'GET':
        logger.info('received a GET request from {}'.format(request.remote_addr))
        reply = 'Use the POST method'
        return reply
    elif request.method == 'POST':
        data = request.json
        try:
            if data[0]['series'][0]['name'] == 'alerts' and data[0]['series'][0]['tags']:
                Thread(target=thread_worker, args=(data,)).start()
        except ValueError:
            logger.warning('Malformed body format in POST from {ip}. / Received body was {body}'
                           .format(ip=request.remote_addr, body=data))
        return jsonify(data)


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(handlers=[
        logging.StreamHandler()], format=FORMAT, level=logging.INFO)

    app.run(host='127.0.0.1', port=5001, debug=True)
