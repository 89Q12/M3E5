
# Broker settings.
broker_url = 'pyamqp://guest@localhost//'

# List of modules to import when the Celery worker starts.
imports = ('base_folder.tasks',)

# Using the database to store task state and results.
result_backend = 'db+sqlite:///results.db'

task_annotations = {'tasks.add': {'rate_limit': '10/s'}}