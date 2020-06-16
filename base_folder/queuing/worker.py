from celery import Celery, Task

app = Celery('queuing', include=['base_folder.queuing.db', ])
app.config_from_object('base_folder.bot.config.config')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
