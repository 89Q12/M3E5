# Broker/Backend settings.
broker_url = 'amqp://zofi:60814630@localhost:5672/m3e5'
result_backend = 'amqp://zofi:60814630@localhost:5672/m3e5'
# List of modules to import when the Celery worker starts.
imports = ('base_folder.queuing.db',)
include = ['base_folder.queuing']
task_cls = 'base_folder.queuing.tasks:DatabaseTask'

