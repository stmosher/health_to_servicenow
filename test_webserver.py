import requests
import json


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
    data = {'one': '1', 'two': '2', 'three': '3'}
    url = web_server + view_route

    test_server(url, data)
