from base_folder.tasks import add

r = add.delay(4, 4)

print(r.backend)