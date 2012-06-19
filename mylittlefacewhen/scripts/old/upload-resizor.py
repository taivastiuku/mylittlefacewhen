from viewer.models import Face
import json


with open("/home/inopia/webapps/mylittlefacewhen/mylittlefacewhen/output.json") as data:
    faces = json.loads(data.read())

for face in faces:
    f = Face.objects.filter(id=face["id"])[0]
    
    if face.get("huge"):
        f.huge = face["huge"]
    if face.get("large"):
        f.large = face["large"]
    if face.get("medium"):
        f.medium = face["medium"]
    if face.get("small"):
        f.small = face["small"]
    f.save()
