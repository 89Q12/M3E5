# Broker/Backend settings.
broker_url = 'amqp://zofi:brdfat65mc@localhost:5672/m3e5'
result_backend = 'amqp://zofi:brdfat65mc@localhost:5672/m3e5'
# List of modules to import when the Celery worker starts.
BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = 0
imports = ('base_folder.queuing.db',)
include = ['base_folder.queuing']
task_cls = 'base_folder.queuing.db:DatabaseTask'
timezone = 'Europe/Berlin'

