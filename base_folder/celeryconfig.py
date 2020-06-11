# Broker settings.
broker_url = 'amqp://zofi:60814630@localhost:5672/m3e5'
result_backend = 'amqp://zofi:60814630@localhost:5672/m3e5'
# List of modules to import when the Celery worker starts.
imports = ('base_folder.tasks',)
include = ['base_folder.tasks']
# Using the database to store task state and results.

task_cls = 'base_folder.tasks:DatabaseTask'
task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
