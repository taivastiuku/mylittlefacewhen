import re
from viewer.models import Face, TagLog, SourceLog
import requests
from tagging.models import Tag

ponibooru = "http://ponibooru.413chan.net/post/view/"

for face in Face.objects.all():
    name = face.image.name.lstrip("f/img/")
    if re.match("[0-9]+[+_ ]-[+_ ]", name):
        if face.source:
            continue
        print name
        pid = name.replace("+", " ").replace("_", " ").partition(" ")[0]
        r = requests.get(ponibooru + pid)
        if r.status_code == 200:
            source = r.content.partition("Source:")[2].partition("'")[2].partition("'")[0]
            if not source:
                source = ponibooru + pid
            print "source: " + source
            tags = r.content.partition("Tags (separate with spaces)")[2].partition("value='")[2].partition("'")[0]
            print "tags: " + tags
            print " "
            face.source = source
            tags = tags.split(" ")
            for tag in tags:
                try:
                    Tag.objects.add_tag(face, tag.replace("_", " ") + ",")
                except:
                    continue
            TagLog.new(face)
            SourceLog.new(face)
            face.save()

