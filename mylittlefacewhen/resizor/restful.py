#from piston.handler import BaseHandler
#from piston.resource import Resource
#from piston.utils import validate
#from django.db import models

#from resizor import models
#from resizor import forms

from cStringIO import StringIO
#import base64
import re
import json
try:
    import Image
    import ImageFile
except:
    from PIL import Image
    from PIL import ImageFile
ImageFile.MAXBLOCK = 1024*1024


#RESOURCES = {}
GIF = "/home/inopia/webapps/mlfw_static/gif.png"

#def register(key):
#
#    def deco(klass):
#        RESOURCES[key] = Resource(klass)
#        return klass
#
#    return deco

#@register("task")

def process_image(data):
    #string_image = StringIO(data.pop("image"))
    #image = Image.open(string_image)
    #image.load()
    #string_image.close()

    image = Image.open(data["image"])

    if image.format not in ("PNG", "JPEG", "GIF"):
        #return ["Unsupported format %s" % image.format]
        #return bad request
        return False

    elif image.mode not in ("L", "P", "LA", "RGB", "RGBA"):
        #return ["Unsupported mode %s" % image.mode]
        #return bad request
        return False


    output = {"png":{}, "jpg":{}}

    for size in data["sizes"]:
        if (size[0] >= image.size[0] or size[0] == 0) and size[1] >= image.size[1]:
            continue
        temp_handle = StringIO()


        rgba = False
        # Possibly alpha image
#            if image.format != "GIF":

        if image.mode in ("P", "LA"):
            rgba = True
            cpy = image.convert("RGBA")
            png = True
            jpg = False
        elif image.mode == "RGBA":
            rgba = True
            cpy = image.copy()
            png = True
            jpg = False
        elif image.mode == "L":
            cpy = image.convert("RGB")
            png = False
            jpg = True
        else: # image.mode == "RGB":
            cpy = image.copy()
            png = False
            jpg = True

#        if data.get("format"):
#            if data["format"] == "png":
#                png = True
#                jpg = False
#            elif data["format"] == "jpg":
#                if rgba:
#                    i = Image.new("RGB", cpy.size,(255,255,255))
#                    i.paste(cpy,(0,0,cpy.size[0],cpy.size[1],), cpy)
#                    cpy = i
#                png = False
#                jpg = True


        if size[0] == 0:
            resize = (cpy.size[0], size[1])
        elif size[1] == 0:
            resize = (size[0], cpy.size[1])
        else:
            resize = size

        cpy.thumbnail(resize, Image.ANTIALIAS)

        if data.get("write_gif") and image.format=="GIF":
            i_width, i_height = cpy.size
            gif = Image.open(GIF)
            gif.thumbnail((i_width-4, i_height*1/2), Image.ANTIALIAS)

            g_width, g_height = gif.size

            x0 = i_width/2-g_width/2
            y0 = i_height - g_height - 1
            x1 = x0 + g_width
            y1 = y0 + g_height

            cpy.paste(gif, (x0, y0, x1, y1), gif)


        if cpy.mode == "RGB" and not data.get("format", "").lower() == "png":
            if size[1] <= 100 :
                cpy.save(temp_handle, "JPEG", quality=70, optimize=True)
            else:
                cpy.save(temp_handle, "JPEG", quality=85, optimize=True)
            format = "jpg"
        else:
            cpy.save(temp_handle, "PNG")
            format = "png"

        temp_handle.seek(0)

        #output[format][str(size)] = base64.b64encode(temp_handle.read())
        output[format][json.dumps(size)] = temp_handle.read()
        temp_handle.close()

    return output

#class TaskHandler(BaseHandler):
#    allowed_methods = ("POST",)
#
#    @validate(forms.CreateTask)
#    def create(self, request):
#        return process_image(request.form.cleaned_data)

