### links
* https://docs.celeryproject.org/en/stable/getting-started/next-steps.html

### run celery
```
celery -A src worker -l info
```

### run celery en windows
* https://stackoverflow.com/questions/27357732/celery-task-always-pending
* https://docs.celeryproject.org/en/stable/reference/celery.bin.worker.html#cmdoption-celery-worker-p
* https://www.distributedpython.com/2018/10/26/celery-execution-pool/
```
celery -A src worker -l info --pool=solo
```

### Call task
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

### get response celery by id
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
