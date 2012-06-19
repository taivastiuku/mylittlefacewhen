"""
Imports count of views from Google Analytics dump.
"""
import json
from viewer.models import *
j = json.loads(open("views.json","r").read())

for key, value in j.iteritems():
    try:
        f = Face.objects.get(id=int(key))
        f.views = value
        f.save()
    except:
        pass
