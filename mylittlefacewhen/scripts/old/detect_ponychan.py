from viewer.models import Face, SourceLog
import re
import requests
import time

ponychan = "http://pinkie.ponychan.net/chan/files/src/"

for face in Face.objects.all():
    name = face.image.name[6:]
    if re.match("[0-9]{12}\.", name):
        try:
            r = requests.head(ponychan + name)
        except:
            print "ERROR"
            time.sleep(5)
            try:
                r = requests.head(ponychan + name)
            except:
                continue
        
        if r.status_code == 200:
            print "FOUND"
        else:
            print "no"



