import os
import json

l = os.listdir("/tmp/resizor")
l.sort()

out = {}
for item in l:
    part = item.partition("_")
    if not out.get(part[0]):
        out[part[0]] = {}

    out[part[0]][part[2].partition(".")[0]] = "/tmp/resizor/" + item


lista = []

for key, value in out.items():
    value["id"] = int(key)
    lista.append(value)

with open("output.json", "w") as dump:
    dump.write(json.dumps(lista, indent=4))
