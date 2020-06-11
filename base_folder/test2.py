from base_folder.tasks import get_levelsystem, add, prefix_lookup

r = prefix_lookup.delay(715131657107144724)
print(r.status)
print(r.get())