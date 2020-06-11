# Broker/Backend settings.
broker_url = 'amqp://zofi:60814630@localhost:5672/m3e5'
result_backend = 'amqp://zofi:60814630@localhost:5672/m3e5'
# List of modules to import when the Celery worker starts.
imports = ('queuing.db',)
include = ['queuing']
task_cls = 'queuing.db:DatabaseTask'

