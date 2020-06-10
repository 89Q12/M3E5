from celery import Celery

app = Celery('tasks', broker='redis://172.17.0.1//')


@app.task
def add(x, y):
    return x + y

