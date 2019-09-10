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
import logging

import requests


class Snow:
    """
    A class used to interact with Service Now

    ...

    Attributes
    ----------
    username : str
    password : str
    url: str
        The URL for Service Now

    Methods
    -------
    post(api_path, body_data)
        Makes HTTP POST request to Service Now
    """
    def __init__(self, username=None, password=None, url=None, api_path=None):
        """
        Parameters
        ----------
        username : str
        password : str
        url: str
            The URL for Service Now
         """
        self.username = username
        self.password = password
        self.url = url
        self.api_path = api_path

    def post(self, body_data):
        """HTTP POSTs body_data to Service Now at api_path

        Parameters
        ----------
        body_data : dict
            Dictionary of key/values for body of POST to Service Now

        Returns
        ------
        boolean:
            True: if POST worked
            False: id POST failed
        """
        logger = logging.getLogger(__name__)
        u = self.url + self.api_path

        headers = {'Accept': 'application/json',
                   'Content-type': 'application/json'}

        r = requests.post(u, auth=(self.username, self.password), headers=headers, data=json.dumps(body_data))

        if r.status_code != 201:
            logger.warning('Web server communication error {}'.format(r.status_code))
            logger.warning('Unable to update snow for alert {body}.'.format(body=str(body_data)))
            return False
        else:
            logger.info('POST successful {}'.format(r.status_code))
        return True
