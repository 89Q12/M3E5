from celery import Celery, Task

app = Celery('queuing', include=['queuing.db'])
app.config_from_object('queuing.celeryconfig')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()