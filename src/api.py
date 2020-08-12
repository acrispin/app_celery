from flask import Flask, request, jsonify, abort, make_response

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/', methods=['POST', 'PUT'])
def post_json():
    logger.info(request.is_json)
    logger.info(request.json)
    content = request.get_json()
    # abort(404)
    # abort(make_response(jsonify({'message': 'msg', 'code': 400, 'status': 'FAIL'}), 500))
    logger.info(content)
    return jsonify(content)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000', debug=True)
