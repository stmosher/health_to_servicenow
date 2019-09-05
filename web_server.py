from flask import Flask
from flask import request
from flask import jsonify


app = Flask(__name__)


@app.route('/health_to_snow', methods=['GET', 'POST'])
def health_to_snow():
    if request.method == 'GET':
        reply = 'Use the POST method'
        return reply
    elif request.method == 'POST':
        data = request.json
        return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
