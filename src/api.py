from flask import Flask, request, jsonify, abort, make_response
from decouple import config

from .tasks import longtime_add, check_obj
from .log import logging, setup_custom_logger

logger = setup_custom_logger(__name__)

DEBUG = config('DEBUG', default=False, cast=bool)
FLASK_HOST = config('FLASK_HOST', default='0.0.0.0', cast=str)
FLASK_PORT = config('FLASK_PORT', default='5000', cast=str)

app = Flask(__name__)


@app.route('/')
def hello_world():
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"{request.method} {request.path}")
    return jsonify({'message': 'Hello, World!'})


@app.route('/test/', methods=['POST', 'PUT'])
def post_json():
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"{request.method} {request.path}")
    logger.info(request.is_json)
    logger.info(request.json)
    content = request.get_json()
    logger.info(content)
    # abort(404)
    abort(make_response(jsonify({'message': 'msg', 'code': 400, 'status': 'FAIL'}), 500))
    return jsonify(content)


# Por defecto es metodo GET
@app.route('/api/')
def process_task():
    try:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{request.method} {request.path}")
        first_num = request.args.get('first')
        second_num = request.args.get('second')
        result = longtime_add.delay(first_num, second_num)
        return jsonify({'message': 'OK', 'id': result.id})
    except Exception as ex:
        logger.exception(ex)
        return make_response(jsonify({'message': str(ex), 'code': 500, 'status': 'FAIL'}), 500)


@app.route('/api/', methods=['POST', 'PUT'])
def process_task2():
    try:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{request.method} {request.path}")
        content = request.get_json()
        data = content['first'], content['second']
        result = longtime_add.delay(*data)
        result = longtime_add.apply_async(data, countdown=10)
        result = longtime_add.apply_async(args=data, countdown=10)
        result = longtime_add.apply_async(kwargs=content, countdown=10)
        return jsonify({'message': 'OK', 'id': result.id})
    except Exception as ex:
        logger.exception(ex)
        return make_response(jsonify({'message': str(ex), 'code': 500, 'status': 'FAIL'}), 500)


@app.route('/api/obj/', methods=['POST', 'PUT'])
def process_obj():
    try:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{request.method} {request.path}")
        content = request.get_json()
        result = check_obj.delay(content)
        result = check_obj.apply_async((content,))
        result = check_obj.apply_async(args=(content,))
        result = check_obj.apply_async(kwargs={"obj": content})
        return jsonify({'message': 'OK', 'id': result.id})
    except Exception as ex:
        logger.exception(ex)
        return make_response(jsonify({'message': str(ex), 'code': 500, 'status': 'FAIL'}), 500)


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
