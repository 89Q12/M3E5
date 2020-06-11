from celery import Celery, Task

app = Celery('base_folder', include=['base_folder.tasks'])
app.config_from_object('base_folder.celeryconfig')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()