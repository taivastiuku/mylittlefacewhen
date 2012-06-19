from viewer.models import Face
from PIL import Image
import os
import requests
import base64
from cStringIO import StringIO
import sys
import shutil
import json

# "Suspension not allowed here" workaround
from PIL import ImageFile
ImageFile.MAXBLOCK = 1024*1024 # default is 64k

sizes = ((1000, "huge"), (640, "large"), (320, "medium"), (160, "small"))
square_sizes = (160, 90)
mediadir = "/home/inopia/webapps/mlfw_media/f/rsz/"
tmp = "/tmp/resizor/"
PNGOUT_PATH = "/home/inopia/pngout-static"

#if os.path.exists(tmp):
#    shutil.rmtree(tmp)

#os.mkdir(tmp)
#os.mkdir(tmp + "pngout/")

if not os.path.exists(PNGOUT_PATH):
    sys.exit("no pngout")


out = []
for face in Face.objects.filter(id__gt=1040):
    with open(face.image.path) as filu:
        i = Image.open(filu)
        i.load()
        
    width, height = i.size
    
    if i.format == "GIF":
        continue

    faceout = {"id" : face.id}

    
    for value in sizes:
        size = value[0]
        sizename = value[1]

        if size > max(width,height):
            continue
        
        if i.format == "JPEG" or (i.format == "PNG" and not face.tags.filter(name="transparent")):
            cpy = i.copy()
            cpy.thumbnail((size, size), Image.ANTIALIAS)
            if cpy.mode != "RGB":
                cpy = cpy.convert("RGB")
            
            path = tmp + str(face.id) + "_" + sizename + ".jpg"
            cpy.save(path, "JPEG", quality=85, optimize=True)
            faceout[sizename] = path


        elif i.format == "PNG":
            cpy = i.copy()
            cpy.thumbnail((size, size), Image.ANTIALIAS)
            name = str(face.id) + "_" + sizename + ".png"
            cpy.save(tmp + name, "PNG")
            # PNGOUT
            os.system("""%s '%s' '%s' -y""" % (PNGOUT_PATH, tmp+name, tmp + "pngout/" + name))
    
            # PNGOUT fails for some pngs so use PNGCRUSH instead
            if not os.path.exists(tmp+"pngout/"+name):
                os.system("""pngcrush -rem alla -rem text '%s' '%s'""" % (tmp+name, tmp+"pngout/"+name))

            faceout[sizename] = tmp + "pngout/" + name

    out.append(faceout)

with open("./out.json", "w") as dump:
    dump.write(json.dumps(out, indent=4))

