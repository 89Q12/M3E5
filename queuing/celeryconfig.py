# Broker/Backend settings.
broker_url = 'amqp://zofi:brdfat65mc@localhost:5672/m3e5'
result_backend = 'amqp://zofi:brdfat65mc@localhost:5672/m3e5'
# List of modules to import when the Celery worker starts.
imports = ('queuing.db',)
include = ['queuing']
task_cls = 'queuing.db:DatabaseTask'
timezone = 'Europe/Berlin'

