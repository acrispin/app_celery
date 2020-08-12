### links
* https://docs.celeryproject.org/en/stable/getting-started/next-steps.html

### run celery
```
celery -A proj worker -l info
```

### run celery en windows
* https://stackoverflow.com/questions/27357732/celery-task-always-pending
* https://docs.celeryproject.org/en/stable/reference/celery.bin.worker.html#cmdoption-celery-worker-p
* https://www.distributedpython.com/2018/10/26/celery-execution-pool/
```
celery -A proj worker -l info --pool=solo
```

### Call task
``` python
>>> from proj.tasks import add
>>> add.delay(2, 2)
>>> add.apply_async((2, 2))
>>> add.apply_async((2, 2), countdown=10)
>>> add.apply_async((2, 2), queue='lopri', countdown=10)
>>> res = add.delay(2, 2)
>>> res.get(timeout=1)
>>> res.id
>>> res = add.delay(2, '2')
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
>>> from proj.celery import app
>>> res = app.AsyncResult('eae620f1-ecc8-47e9-8291-0f64f060f8a6')
>>> res.state
PENDING -> STARTED -> RETRY -> STARTED -> RETRY -> STARTED -> SUCCESS
```