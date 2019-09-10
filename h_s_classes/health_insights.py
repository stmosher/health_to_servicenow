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


class HealthInsights:
    """
    A class used handle POST requests from crossworks Health Insights

    ...

    Attributes
    ----------
    None

    Methods
    -------
    parse_alert_body(body)
        Parses Health Insights Alert messages
    """

    def parse_alert_body(self, body):
        """Parses Health Insights Alert messages.

        Parameters
        ----------
        body : dict
            Converted body from Health Insights alert

        Returns
        -------
        list
            a list of dictionaries containing key/value pairs as
            parsed from Health Insights alert message

        """
        logger = logging.getLogger(__name__)
        try:
            results = list()
            for a in body:
                for s in a['series']:
                    columns_list = [c for c in s['columns']]
                    for v1 in s['values']:
                        values_list = [v for v in v1]
                        z_dict = self.my_zip(columns_list, values_list)
                        add_dict = {
                                    'id': z_dict.get('id', 'Unknown'),
                                    'kpi_id': s['tags'].get('kpi_id', 'Unknown'),
                                    'level': s['tags'].get('level', 'Unknown'),
                                    'msg': z_dict.get('msg', 'Unknown'),
                                    'producer': s['tags'].get('Producer', 'Unknown'),
                                    'state': s['tags'].get('state', 'Unknown'),
                                    'time': z_dict.get('time', 'Unknown'),
                                    'uuid': s['tags'].get('UUID', 'Unknown')
                                    }
                        results.append(add_dict)
            return results
        except ValueError as e:
            logger.warning(e)
            return False
        except BaseException as e:
            logger.warning(e)
            return False

    @staticmethod
    def my_zip(list1, list2):
        """Combines indexes from two lists into key/value pairs in a dict.

        Parameters
        ----------
        list1 : list
            List of future keys for dict

        list2 : list
            List of future values for dict

        Returns
        -------
        dict
            key/values resulting from combining list1 and list2

        """
        md = dict()
        for i in list1:
            md[i] = list2[list1.index(i)]
        return md
