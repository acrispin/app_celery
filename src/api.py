from flask import Flask, request, jsonify, abort, make_response

from .tasks import longtime_add
from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})


@app.route('/test/', methods=['POST', 'PUT'])
def post_json():
    logger.info(request.is_json)
    logger.info(request.json)
    content = request.get_json()
    logger.info(content)
    # abort(404)
    abort(make_response(jsonify({'message': 'msg', 'code': 400, 'status': 'FAIL'}), 500))
    return jsonify(content)


@app.route('/api/')
def process_task():
    first_num = request.args.get('first')
    second_num = request.args.get('second')
    result = longtime_add.delay(first_num, second_num)
    return jsonify({'message': 'OK', 'id': result.id})


@app.route('/api/', methods=['POST', 'PUT'])
def process_task2():
    content = request.get_json()
    # result = longtime_add.delay(content['first'], content['second'])
    data = content['first'], content['second']
    result = longtime_add.apply_async(data, countdown=10)
    result = longtime_add.apply_async(args=data, countdown=10)
    result = longtime_add.apply_async(kwargs=content, countdown=10)
    return jsonify({'message': 'OK', 'id': result.id})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='5000', debug=True)
