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

import json
import requests


def test_server(u, d):
    headers = {'Accept': 'application/json',
               'Content-type': 'application/json'}

    r = requests.post(u, headers=headers, data=json.dumps(d))

    if r.status_code != 200:
        print('Web server communication error {}'.format(r.status_code))
        exit()

    try:
        assert r.json() == d
    except AssertionError:
        print("Web server failed to POST body")
    except BaseException as e:
        print(e)


if __name__ == '__main__':

    web_server = 'http://127.0.0.1:5001'
    view_route = '/health_to_snow'

    data = [{
        "series": [{
            "columns": [
                "time",
                "activation_threshold",
                "alert_src",
                "clear_threshold",
                "crit_threshold",
                "id",
                "kpi_stream",
                "msg",
                "sigma",
                "warn_threshold"
            ],
            "name": "alerts",
            "tags": {
                "CollectorId": "mdt-robot-collector-13a3958e-63d5-47e5-9e0f-31e846b89f2e",
                "EncodingPath": "Cisco-IOS-XR-wdsysmon-fd-oper:system-monitoring/cpu-utilization",
                "Producer": "spnac-a9k-s079",
                "UUID": "5108e98e-aea0-49a5-ba32-88db39b777c3",
                "kpi_id": "pulse_cpu_utilization",
                "level": "INFO",
                "node-name": "0/RP0/CPU0",
                "state": "clear"
            },
            "values": [
                [
                    "2019-09-05T22:02:57.412Z",
                    -1,
                    "TICK",
                    2,
                    2,
                    "pulse_cpu_utilization",
                    2,
                    "INFO : 0/RP0/CPU0  5min CPU Utilization: 2.00 % has returned to Usual range, Threshold: 2.00 SD. It is 0.45 std. dev away from Average.",
                    0.45390323755854023,
                    2
                ]
            ]
        }]
    },
        {
            "series": [{
                "columns": [
                    "time",
                    "activation_threshold",
                    "alert_src",
                    "clear_threshold",
                    "crit_threshold",
                    "id",
                    "kpi_stream",
                    "msg",
                    "sigma",
                    "warn_threshold"
                ],
                "name": "alerts",
                "tags": {
                    "CollectorId": "mdt-robot-collector-13a3958e-63d5-47e5-9e0f-31e846b89f2e",
                    "EncodingPath": "Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/data-rate",
                    "Producer": "spnac-a9k-s078",
                    "UUID": "16df73dc-0614-44bd-885a-1cad09a68689",
                    "interface-name": "GigabitEthernet0/0/0/0",
                    "kpi_id": "pulse_interface_rate_counters",
                    "level": "INFO",
                    "state": "down"
                },
                "values": [
                    [
                        "2019-09-05T22:03:03.496Z",
                        -1,
                        "TICK",
                        2,
                        2,
                        "pulse_interface_rate_counters_rxrate",
                        0,
                        "INFO : GigabitEthernet0/0/0/0 Rx Rate: 0.00 pkts/sec has returned to Usual range, Threshold: 2.00 SD. It is 0.00 std.dev away from Average.",
                        0,
                        2
                    ]
                ]
            }]
        }
    ]

    url = web_server + view_route
    test_server(url, data)
