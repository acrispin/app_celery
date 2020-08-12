
# from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='amqp://guest:guest@localhost:5672',
             backend='rpc://',
             include=['proj.tasks'])

app.conf.timezone = 'America/Lima'
# # Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

if __name__ == '__main__':
    app.start()
