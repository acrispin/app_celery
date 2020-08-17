
# Ejecucion local
* python 3.7

### 1 copiar .env.local a .env y editar segun configuracion local
```
cp .env.local .env
```

### 2 instalar rabbitmq, si se tiene docker ejecutar lo siguiente
* https://www.rabbitmq.com/download.html
``` 
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e "TZ=America/Lima" rabbitmq:3-management
```

### 3 crear, activar entorno virtual e instalar dependencias, en winwods _(...>venv\Scripts\activate)_
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4 ejecutar api, worker, flower en diferente terminal (se usa _'-P threads'_ para evitar incompatibilidad en windows)
```
python -m src.api
celery -A src worker -l info -P threads
flower -A src --conf=flowerconfig
python -m src.job
```

### 5 probar las url
* http://localhost:5000/ (flask)
* http://localhost:5555/ (flower, autenticacion segun parametro _'FLOWER_BASIC_AUTH'_ de .env)

### 6 probar servicios, _'127.0.0.1'_ o _'localhost'_
```
GET /api?first=23&second=34 HTTP/1.1
Host: 127.0.0.1:5000

POST /api/ HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
{
    "first": 123,
    "second": 938
}

POST /api/obj/ HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
{
    "device": "TemperatureSensor",
    "value": "20",
    "timestamp": "2020-08-12 10:10:05"
}
```

# Ejecucion con docker
* Docker version 19.03.12, build 48a66213fe
* docker-compose version 1.25.4, build 8d51620a

### 1 copiar .env.docker a .env y editar segun configuracion de docker-compose
```
cp .env.docker .env
```

### 2 levantar los contenedores
```
docker-compose up -d --build rabbitmq
docker-compose up -d --build api
docker-compose up -d --build worker
docker-compose up -d --build flower
docker-compose up -d --build job
```

### 3 probar las url, segun los puertos que se hayan definido en el docker-compose
* http://localhost:5000/ (flask)
* http://localhost:5555/ (flower, autenticacion segun parametro _'FLOWER_BASIC_AUTH'_ de .env)

# RABBIT

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

# CELERY

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
>>> res.get()
>>> res.state
PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS
```

### celery, Delay and apply_async waiting forever when the broker is down, faq
* https://github.com/celery/celery/issues/4296#issuecomment-412526075
* https://github.com/celery/celery/issues/4627#issuecomment-396907957
* https://docs.celeryproject.org/en/stable/faq.html

### celery, utils
* https://medium.com/better-programming/python-celery-best-practices-ae182730bb81
* https://blog.daftcode.pl/working-with-asynchronous-celery-tasks-lessons-learned-32bb7495586b
* https://docs.celeryproject.org/en/stable/reference/celery.app.task.html
* https://docs.celeryproject.org/en/latest/userguide/tasks.html#bound-tasks
* https://www.vinta.com.br/blog/2018/celery-wild-tips-and-tricks-run-async-tasks-real-world/
* https://docs.celeryproject.org/en/stable/userguide/tasks.html#automatic-retry-for-known-exceptions
* https://testdriven.io/blog/retrying-failed-celery-tasks/
* https://www.agiliq.com/blog/2015/08/retrying-celery-failed-tasks/
* https://medium.com/@dwernychukjosh/retrying-asynchronous-tasks-with-celery-221acd385d34

# FLOWER

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

### flower run with rabbit and auth
```
flower --broker=amqp://guest:guest@localhost:5672/ --port=5555 --basic_auth=admin:12345678
```

### flower run with config, en el src se indica el broker
```
flower -A src --conf=flowerconfig
```

# FLASK

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

# DOCKER

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

### docker, logs and check con bash o sh, opcional indicando el .env file, si el contenedor _'app_celery_api'_ existe
```
docker run -it --rm app_celery:v1.1.0 bash
docker run -it --rm --env-file .env app_celery:v1.1.0 bash
docker exec -it app_celery_api bash
docker logs -f --tail 100 app_celery_api
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

### docker, stop and clean
* https://gist.github.com/ntarocco/4725e27f7a196d9fe405574152b0e744
```
#!/usr/bin/env bash

docker stop $(docker ps -aq)

# docker container prune   # Remove all stopped containers
# docker volume prune      # Remove all unused volumes
# docker image prune       # Remove unused images
# docker system prune      # All of the above, in this order: containers, volumes, images
echo y | docker system prune
```

### docker, detener y eliminar todos los contenedores
* https://blog.jongallant.com/2017/09/unknown-shorthand-flag/
```
docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
```

### docker, eliminar todas las imagenes
```
docker rmi $(docker images -a -q)
```

### docker, listar volumenes y networks
```
docker volume ls
docker network ls
```

### docker, links
* https://kelda.io/blog/common-docker-compose-mistakes/
* https://github.com/vishnubob/wait-for-it
* https://adilsoncarvalho.com/creating-multiple-images-from-a-single-dockerfile-3f69254b6137
* https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

# MARKDOWN, Syntax highlighting
* https://support.codebasehq.com/articles/tips-tricks/syntax-highlighting-in-markdown

# VIRTUALENV and PIP

### upgrade pip, install virtualenv, en linux con sudo, en windows cmd en modo administrador
```
python -m pip install --upgrade pip
pip install virtualenv
pip --version
virtualenv --version
```

### virtualenv, especificar otra version de python instalada en linux
```
virtualenv -p /usr/bin/python3 venv  
source venv/bin/activate
deactivate
```

### virtualenv, especificar otra version de python instalada en windows con gitbash
```
virtualenv -p /c/Program\ Files/Python37/python.exe venv  
source venv/Scripts/activate
deactivate
```

### virtualenv, especificar otra version de python instalada en windows con cmd
```
...>virtualenv -p "C:\Program Files\Python37\python.exe" venv 
...>venv\Scripts\activate
...>deactivate
```
 
### pip, actualizar una libreria
```
pip uninstall pyodbc
pip install pyodbc
pip freeze > requirements.txt  
```

# SENTRY

### sentry, instalacion, luego establecer la variable de entorno SENTRY_DSN en .env
* https://docs.sentry.io/platforms/python/logging/
```
pip install --upgrade sentry-sdk
pip freeze > requirements.txt
```

# DB

### db, instalacion odbc driver sql server y correccion conexion ssl
* https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#debian17
* https://github.com/microsoft/msphpsql/issues/1023

### db, prueba de concepto con pyodbc, script para testear insert masivo
* https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
* https://github.com/mkleehammer/pyodbc/issues/802

### db, prueba de conexion a la bd dentro del contenedor generado por Dockerfile, con sqlcmd y python
```
docker-compose exec api bash
sqlcmd -S $DB_SERVER,$DB_PORT -d $DB_NAME -U $DB_USER -P $DB_PASSWORD -i /app/info.sql
python -m src.db
```

# LINUX

### linux, verificar version de distribucion linux
```
cat /etc/os-release
cat /etc/*-release
```