from viewer.models import Face, SourceLog
import re

for face in Face.objects.all():
    if re.search("tumblr_", face.image.path):
        print face.image.path
        face.source = "http://www.tumblr.com/"
        face.save()
        SourceLog.new(face)

