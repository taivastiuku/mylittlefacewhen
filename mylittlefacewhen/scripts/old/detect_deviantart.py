from viewer.models import Face, SourceLog
import re

for face in Face.objects.all():
    if re.search("_by_[a-zA-Z0-9]+-[a-z0-9]{7}", face.image.name):
        print face.image.path
        artist = face.image.path.rpartition("_by_")[2].rpartition("-")[0]
        imghash = face.image.path.rpartition("-")[2].rpartition(".")[0]
        face.source = "http://%s.deviantart.com/#/%s" % (artist, imghash)
        face.save()
        SourceLog.new(face)
