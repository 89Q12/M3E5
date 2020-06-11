from base_folder.tasks import get_levelsystem, add

r = add.delay(715131657107144724)
print(r.status)

r.forget()
