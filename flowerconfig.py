from decouple import config, Csv

FLOWER_BROKER_API = config('FLOWER_BROKER_API', default='', cast=str)
FLOWER_PORT = config('FLOWER_PORT', default=5555, cast=int)
FLOWER_BASIC_AUTH = config('FLOWER_BASIC_AUTH', default='', cast=Csv())
FLOWER_MAX_WORKERS = config('FLOWER_MAX_WORKERS', default=5000, cast=int)
FLOWER_MAX_TASKS = config('FLOWER_MAX_TASKS', default=10000, cast=int)
FLOWER_PERSISTENT = config('FLOWER_PERSISTENT', default=False, cast=bool)
FLOWER_DEBUG = config('FLOWER_DEBUG', default=False, cast=bool)

# https://flower.readthedocs.io/en/latest/config.html
# https://flower.readthedocs.io/en/latest/man.html
# https://www.cloudamqp.com/docs/celery.html

# RabbitMQ management api
broker_api = FLOWER_BROKER_API
port = FLOWER_PORT
basic_auth = FLOWER_BASIC_AUTH
max_workers = FLOWER_MAX_WORKERS
max_tasks = FLOWER_MAX_TASKS
persistent = FLOWER_PERSISTENT
debug = FLOWER_DEBUG
# logging = 'INFO'

'''
Ejecutar flower indicando las opciones en commando
$ flower --broker=amqp://guest:guest@localhost:5672/ --port=5555 --basic_auth=admin:12345678
--broker=amqp://guest:guest@localhost:5672/
--port=5555
--basic_auth=admin:12345678

No funciona poniendo flowerconfig en src
$ flower --conf=src/flowerconfig.py
$ flower --conf=src/flowerconfig

Si flowerconfig.py esta en la raiz, si funciona
$ flower --conf=flowerconfig

Forma correcta de invocar flower, el --broker lo toma de src
https://github.com/mher/flower/issues/341
$ flower -A src --conf=flowerconfig
'''
