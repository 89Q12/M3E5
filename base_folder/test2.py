from tasks import add

r = add.delay(1, 1)

print(r.get())