import imgur
from viewer.models import Face, SourceLog

username = ""
password = ""

access = imgur.api(username=username, password=password, secure=True)

for face in Face.objects.all():
    name = face.image.name.lstrip("f/img/").rpartition(".")[0]
    if len(name) != 5:
        continue
    print name
    img = access.image(name)
    if img:
        face.source = img["links"]["imgur_page"]
        face.save()
        SourceLog.new(face)

