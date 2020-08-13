### rabbitmq, install
* https://www.rabbitmq.com/download.html
``` 
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### rabbitmq, install 2, with Detached (-d)
``` 
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e "TZ=America/Lima" rabbitmq:3-management
docker logs -f --tail 100 rabbitmq
```

### celery, links
* https://docs.celeryproject.org/en/stable/getting-started/next-steps.html

### celery, run celery opcional usar --concurrency o -c
* https://docs.celeryproject.org/en/stable/reference/celery.bin.worker.html#cmdoption-celery-worker-c
```
celery -A src worker -l info
celery -A src worker -l info --concurrency=20
```

### celery, run celery en windows
* https://stackoverflow.com/questions/27357732/celery-task-always-pending
* https://docs.celeryproject.org/en/stable/reference/celery.bin.worker.html#cmdoption-celery-worker-p
* https://www.distributedpython.com/2018/10/26/celery-execution-pool/
```
celery -A src worker -l info --pool=solo
celery -A src worker -l info --pool=threads
celery -A src worker -l info -P threads
```

### celery, Call task
* https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/
``` python
>>> from src.tasks import longtime_add
>>> longtime_add.delay(12, 17)
>>> longtime_add.apply_async((12, 17))
>>> longtime_add.apply_async((12, 17), countdown=10)
>>> longtime_add.apply_async((12, 17), queue='lopri', countdown=10)
>>> res = longtime_add.delay(12, 17)
>>> res.get(timeout=1)
>>> res.id
>>> res = longtime_add.delay(2, '2')
>>> res.get(timeout=1)
>>> res.get(propagate=False)
>>> res.failed()
>>> res.successful()
>>> res.state
PENDING -> STARTED -> SUCCESS
```

### celery, get response celery by id
* https://stackoverflow.com/questions/9034091/how-to-check-task-status-in-celery
``` python
>>> from src.celery import app
>>> res = app.AsyncResult('eae620f1-ecc8-47e9-8291-0f64f060f8a6')
>>> res.state
PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS
```

### flower install
```
pip install flower
```

### flower run with redis
```
flower --broker=redis://localhost:6379/0 --port=5555
```

### flower run with rabbit
```
flower --broker=amqp://guest:guest@localhost:5672/ --port=5555
```

### flower run with rabbit
```
flower --broker=amqp://guest:guest@localhost:5672/ --port=5555 --basic_auth=admin:12345678
```

### flower run with config, en el src se indica el broker
```
flower -A src --conf=flowerconfig
```

### flask
* https://flask.palletsprojects.com/en/1.1.x/quickstart/
* https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
* https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
* https://riptutorial.com/flask/example/5832/receiving-json-from-an-http-request
* https://gist.github.com/hirobert/394981a661cbf78d442e
```
python src/api.py
```

### flask, otra forma de ejecutarlo con -m para evitar error: "_ImportError: attempted relative import with no known parent package_"
* https://napuzba.com/a/import-error-relative-no-parent/p4
```
python -m src.api
```

### flask restful 
* https://unipython.com/como-hacer-paso-a-paso-una-api-restful-en-flask-con-python/
* https://dev.to/aligoren/building-basic-restful-api-with-flask-restful-57oh
* https://blog.j-labs.pl/flask-restful

### pycharm, pycharm run python module
* https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003879119-how-to-run-python-m-command-in-pycharm-

### docker version, Docker version 19.03.12, build 48a66213fe
```
docker --version
```

### docker-compose version, docker-compose version 1.25.4, build 8d51620a
```
docker-compose --version
```

### docker, build image
```
docker build -t app_celery:v1.1.0 .
```

### docker, check container con bash o sh, opcional indicando el .env file
```
docker run -it --rm app_celery:v1.1.0 bash
docker run -it --rm --env-file .env app_celery:v1.1.0 bash
docker run -it --rm -p 5000:5000 --env-file .env app_celery:v1.1.0
```

### docker, si la imagen tiene ENTRYPOINT y CMD para ejecutar flask, se indica el puerto 5000
```
docker run -it --rm -p 5000:5000 --env-file .env app_celery:v1.1.0
```

### docker-compose, verificar configuracion de archivo docker-compose
```
docker-compose config
```

### docker-compose, ejecutar servicio rabbitmq, opcional con --remove-orphans para eliminar contenedores eliminados del docker-compose
```
docker-compose up -d rabbitmq
docker-compose up -d --remove-orphans rabbitmq
docker-compose logs -f --tail 100
docker-compose logs -f --tail 100 rabbitmq
```

### docker-compose, ejecutar y forzar build a los servicios rabbitmq, api, worker, flower
```
docker-compose up -d --build rabbitmq
docker-compose up -d --build api
docker-compose up -d --build worker
docker-compose up -d --build flower
```

### docker-compose, otros commandos
```
docker-compose restart rabbitmq
docker-compose stop rabbitmq
docker-compose start rabbitmq
docker-compose down
docker-compose build rabbitmq
docker-compose rm -fs rabbitmq
docker-compose exec rabbitmq bash  
```
