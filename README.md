# Create a Flask web server to receive alerts from Crossworks Healt Insights and create a Service Now ticket
## Installation
1. Clone the repository from GitHub
2. Install application requirements:
    - ````````pip install -r requirements.txt````````
3. Run webserver
    - ````````python3 webserver.py````````
4. Configure test_webserver.py vars
    - web_server
    - view_route
    - data
5. Run test_webserver.py
    - ````````python3 test_webserver.py````````
## Pytest
    - ````````python -m pytest -v````````