#!/usr/bin/env python
# -- coding: utf-8 --

"""
Generates thumbnails from files in a given folder and posts them to dev and 
production servers. Doesn't do anything if access to both servers is not 
available.

PNG -> jpg, wepb thumbnails, do a lossless optimization to original image
PNG.RGBA -> png, jpg, webp thumbnails, do a lossless optimization to original image
JPG -> jpg, webp thumbnails
GIF -> gif thumbnail, jpg and webp thumbnails with text 'GIF' superimposed

"""

from datetime import datetime
import cairo
import os
import sys
import shutil
import json
from PIL import Image
import requests
import base64
from cStringIO import StringIO
import imgur
import re
# "Suspension not allowed here" workaround
from PIL import ImageFile
ImageFile.MAXBLOCK = 1024*1024 # default is 64k

username = ""
password = ""
imgur_login = {"username":"", "password":"", "secure":False}
imgur_access = imgur.api(**imgur_login)

s = {"mlfw":{"session":requests.session(), "server":"https://mylittlefacewhen.com/api"},
     "dev":{"session":requests.session(), "server":"http://0.0.0.0:8000/api"}}

source_dir="/home/inopia/upload/"
failed_dir="/home/inopia/failed/"

imagedir = "/tmp/media/img/"
thumbdir = "/tmp/media/thumb/"
nqdir = "/tmp/media/pngnq/"
outdir = "/tmp/media/pngout/"
rszdir = "/tmp/media/rsz/"

ponibooru = "http://ponibooru.413chan.net/post/view/"

sizes = ((1000, "huge"), (640, "large"), (320, "medium"), (160, "small"))
THUMB_SIZE = 100, 100
PNGOUT_PATH = "/home/inopia/pngout-static"

current_id = 1

complete = []

faces = os.listdir(source_dir)
faces.sort()

if not faces:
    sys.exit(0)

for key, value in s.items():
    r = value["session"].post(value["server"] + "/login/", data={"username":username, "password":password})
    if r.status_code != 200:
        sys.exit("%s login failed: %s" % (key, r))

for d in ("/tmp/media/", imagedir, thumbdir, nqdir, outdir, rszdir, rszdir+"pngout/"):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)

os.chdir("/tmp/media/")

def _getExtents(text, font_size, font_family, slant, weight):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    ctx = cairo.Context(surface)
    ctx.select_font_face(font_family, slant, weight)
    ctx.set_font_size(font_size)
    ext1 = ctx.text_extents("qÖ")
    ext2 = ctx.text_extents(text)
    return (ext2[0], ext1[1], ext2[2], ext1[3])

def generateText(text, fill=(1,1,1), stroke=(0,0,0), line_width=2, weight=cairo.FONT_WEIGHT_NORMAL, slant=cairo.FONT_SLANT_NORMAL, font_family="sans-serif", font_size=50.0, image=None):

    extent = _getExtents(text, font_size, font_family, slant, weight)
    width, height = int(extent[2] + 1), int(extent[3] + 2)

    if image:
        i_width, i_height = image.size
        w_scale = (i_width)/(width*0.95)
        h_scale = (i_height/2)/height
        font_size=font_size * min(w_scale, h_scale)
        extent = _getExtents(text, font_size, font_family, slant, weight)
        width, height = int(extent[2] + 1), int(extent[3] + 2)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    ctx.move_to(-extent[0], abs(extent[1]))
    ctx.select_font_face(font_family, slant, weight)
    ctx.set_font_size(font_size)
    ctx.text_path(text)
    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(line_width)
    ctx.stroke()

    temp_handle = StringIO()
    surface.write_to_png(temp_handle)
    temp_handle.seek(0)
    return Image.open(temp_handle)

def paste(image, text, location):
    i_width, i_height = image.size

    text.thumbnail((i_width-4, i_height*1/2) , Image.ANTIALIAS)
    t_width, t_height = text.size


    if location == "N":
        x0 = i_width/2-t_width/2
        y0 = 1
    elif location == "S":
        x0 = i_width/2-t_width/2
        y0 = i_height - t_height - 1

    x1 = t_width + x0
    y1 = t_height + y0
    image.paste(text, (x0,y0,x1,y1), text)
    return image



def getName(target, name):
    i = 1
    while os.path.exists(target + name):
        part = name.rpartition(".")
        name = part[0] + "." + str(i) + "." + part[2]
        i += 1

    return name



for face in faces:
    thumbname = str(current_id)
    out = {"id":current_id}
    part = face.rpartition(".")
    ext = part[2].lower()
    image_path = source_dir

    if re.match("[0-9]+[ +_]-[ +_]", part[0]):
        #ponibooru
        print "ponibooru: " + face
        pid = part[0].replace("+", " ").replace("_", " ").partition(" ")[0]
        r = requests.get(ponibooru + pid)
        if r.status_code == 200:
            source = r.content.partition("Source:")[2].partition("'")[2].partition("'")[0]
            if not source:
                source = ponibooru + pid
            boorutags = r.content.partition("Tags (separate with spaces)")[2].partition("value='")[2].partition("'")[0]
            boorutags = boorutags.split(" ")
            tags = ""
            for tag in boorutags:
                tags += tag.replace("_", " ") + ", "
            out["source"] = source
            out["tags"] = tags
    elif len(part[0]) == 5:
        #imgur
        print "imgur: " + face
        img = imgur_access.image(part[0])
        if img:
            out["source"] = img["links"]["imgur_page"]
    elif re.match("Screenshot-S[0-9]{2}E[0-9]{2}", part[0]):
        #screenshot
        out["source"] = part[0].rpartition("-")[0]

    elif re.search("_by_[a-zA-Z0-9]+-[a-z0-9]{7}", part[0]):
        #DeviantART
        artist = part[0].rpartition("_by_")[2].rpartition("-")[0]
        imghash = part[0].rpartition("-")[2]
        out["source"] = "http://%s.deviantart.com/#/%s" % (artist, imghash)
    elif re.match("tumblr_", part[0]):
        out["source"] = "http://www.tumblr.com/"
    elif re.match("^[0-9]{12}$", part[0]):
        #ponychan
        if requests.head("http://pinkie.ponychan.net/chan/files/src/" + face).status_code == 200:
            out["source"] = "http://www.ponychan.net/"
        else:
            for board in ("k", "poni", "art", "int", "meta"):
                if requests.head("http://ponilauta.fi/%s/src/%s" % (board, face)).status_code == 200:
                    out["source"] = "http://ponilauta.fi/"
                    break
            



    # WEBP not supported as input before I encounter one
    if ext not in ("png", "jpg", "gif", "jpeg"):
        print "invalid image format: " + face
        continue

    # PNGOUT
    if ext == "png":
        os.system("""%s '%s%s' '%s%s' -y""" % (PNGOUT_PATH, source_dir, face, "./", face))
        image_path = "./"
    
    # PNGOUT fails for some pngs so use PNGCRUSH instead
    if not os.path.exists(image_path + face):
        os.system("""pngcrush -rem alla -rem text '%s%s' '%s%s'""" % (source_dir, face, "./", face))
        image_path = "./"

   
    image = Image.open(image_path + face)
 
    for value in sizes:
        size = value[0]
        sizename = value[1]
        width, height = image.size

        if size > max(width,height) or image.format == "GIF":
            continue

            
        cpy = image.copy()
        cpy.thumbnail((size, size), Image.ANTIALIAS)
        
        if image.format == "JPEG" or (image.format == "PNG" and image.mode == "RGB"):
            if cpy.mode != "RGB":
                cpy = cpy.convert("RGB")
            
            path = rszdir + thumbname + "_" + sizename + ".jpg"
            cpy.save(path, "JPEG", quality=85, optimize=True)
            out[sizename] = path
            out["rszformat"] = "jpg"


        elif image.format == "PNG":
            name = thumbname + "_" + sizename + ".png"
            cpy.save(rszdir + name, "PNG")
            # PNGOUT
            os.system("""%s '%s' '%s' -y""" % (PNGOUT_PATH, rszdir+name, rszdir + "pngout/" + name))
    
            # PNGOUT fails for some pngs so use PNGCRUSH instead
            if not os.path.exists(rszdir+"pngout/"+name):
                os.system("""pngcrush -rem alla -rem text '%s' '%s'""" % (rszdir+name, rszdir+"pngout/"+name))

            out[sizename] = rszdir + "pngout/" + name
            out["rszformat"] = "png"


   
    # Copy to images
    # ololol.1.png if ololol.png exists
    image_name = face
    i = 1
    while os.path.exists(imagedir + image_name):
        image_name = image_name.rpartition(".")[0] + "." + str(i) + "." + ext
        i += 1
    shutil.copy(image_path + face, imagedir + image_name)
    
    out["image"] = imagedir + image_name 

    # Create thumbnails

    # GIF or not, if GIF then it should be an animation
    if image.format=="GIF":
        gifname = thumbname + ".gif"
        print "GIF"
        os.system("""convert "%s" -coalesce coalesce.gif""" % (image_path + face))
        os.system("convert coalesce.gif -resize %dx%d %s" % (THUMB_SIZE[0], THUMB_SIZE[1], gifname))
        shutil.move(gifname, thumbdir)
        out["gif"] = thumbdir + gifname

        thumb = Image.open(thumbdir + gifname)
        t = thumb.convert("RGB")


        paste(t, generateText("GIF"), "S")

        print t
    
        jpgname = thumbname + ".jpg"
        t.save(thumbdir + jpgname, "JPEG", quality=70, optimize=True)
        out["jpg"] = thumbdir + jpgname

        webpname = thumbname + ".webp"
        t.save(thumbdir + webpname, "WEBP", quality=30)
        out["webp"] = thumbdir + webpname

    # PNG, JPG
    else:

        # PNG thumbnail is needed for RGBA PNGs
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        if image.format == "PNG" and (image.mode == "RGBA" or image.mode == "P"):
            pngname = str(thumbname) + ".png"
            image.save(pngname, "PNG", optimize=True)
            os.system("""pngnq -e .png -d '%s' '%s'""" % (nqdir, pngname))
            if image.mode == "RGBA":
                os.system("""%s '%s%s' '%s%s' -y""" % (PNGOUT_PATH, nqdir, pngname, outdir, pngname))
            else:
                os.system("""pngcrush -rem alla -rem text '%s%s' '%s%s'""" % (nqdir, pngname, outdir, pngname))
            shutil.move(outdir + pngname, thumbdir)
            out["png"] = thumbdir + pngname

            #insert white background for non-transparent thumbs
            try:
                i = Image.new("RGB", image.size, (255,255,255))
                i.paste(image, (0,0,image.size[0], image.size[1],), image)
                image = i
            except:
                pass
            
        jpgname = thumbname + ".jpg"

        if image.mode == "P":
            image = image.convert("RGB")

        image.save(thumbdir + jpgname, "JPEG", quality=70, optimize=True)

        out["jpg"] = thumbdir + jpgname

        if image.mode == "L":
            image = image.convert("RGB")

        webpname = thumbname + ".webp"
        image.save(thumbdir + webpname, "WEBP", quality=30)
        out["webp"] = thumbdir + webpname
                

    print out
    for key,value in s.items():
        print key

        data = {"name":out["image"].rpartition("/")[2]}


        for itm in ("rszformat","tags","source"):
            if out.get(itm):
                data[itm] = out[itm]



        for img in ("image", "gif", "png", "jpg", "webp", "huge", "large", "medium", "small"):
            if out.get(img):
                with open(out[img], "rb") as i:
                    data[img] = base64.b64encode(i.read())
        r = value["session"].post(value["server"] + "/faces/", data=data)
        if r.status_code != 200 and key == "mlfw":
            shutil.copy(source_dir + face, failed_dir + getName(failed_dir, face)) 
        print r.status_code
        if r.status_code != 200:
            with open("error.log", "w") as dump:
                dump.write(r.content)

    os.remove(source_dir + face)
    
    current_id += 1

