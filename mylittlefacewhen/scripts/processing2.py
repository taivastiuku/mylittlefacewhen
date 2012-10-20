import base64
import json
import os
import requests
import shutil
import sys
from urllib import urlretrieve

import secrets

try:
    from PIL import Image
except:
    import Image

logininfo = {
    "username": secrets.API_ACCESS["username"],
    "password": secrets.API_ACCESS["password"]}

server = "https://mylittlefacewhen.com/api"

DEBUG = False
if DEBUG:
    server = server = "http://0.0.0.0:8000/api"

THUMB_SIZE = (0, 100,)
PNGOUT_PATH = "/home/inopia/pngout-static"

session = requests.session()
login_request = session.post(server + "/login/", data=logininfo, verify=False)

print login_request
if login_request.status_code != 200:
    sys.exit("login failed: %s" % login_request.read()[0:100])

temp_dir = "/tmp/processing/"
nq_dir = temp_dir + "pngnq/"
out_dir = temp_dir + "out/"

for d in (temp_dir, nq_dir, out_dir):
    if os.path.exists(d):
        shutil.rmtree(d)
    os.mkdir(d)


def get_thumb_size(thumb_size, image_size):
    if thumb_size[0] == 0 and thumb_size[1] == 0:
        out = None
    elif thumb_size[0] == 0:
        out = (image_size[0], thumb_size[1])
    elif thumb_size[1] == 0:
        out = (thumb_size[0], image_size[1])
    else:
        out = thumb_size
    return out


def process_jpeg(url):
    if DEBUG:
        url = url.replace("mlfw.info", "0.0.0.0:8000")
    urlretrieve(url, temp_dir + "process.jpg")
    os.system("jpegoptim --strip-all " + temp_dir + "process.jpg")

    with open(temp_dir + "process.jpg") as out_jpeg:
        out = base64.b64encode(out_jpeg.read())
    return out


def process_webp(url):
    if DEBUG:
        url = url.replace("mlfw.info", "0.0.0.0:8000")
    ext = url.rpartition(".")[2]
    urlretrieve(url, temp_dir + "process." + ext)

    i = Image.open(temp_dir + "process." + ext)
    if i.mode != "RGB":
        i = i.convert("RGB")

    i.thumbnail(get_thumb_size(THUMB_SIZE, i.size), Image.ANTIALIAS)
    i.save(temp_dir + "process.webp", "WEBP", quality=40)
    with open(temp_dir + "process.webp", "r") as webp:
        out = base64.b64encode(webp.read())
    return out


def process_png(url, nq=False):
    if DEBUG:
        url = url.replace("mlfw.info", "0.0.0.0:8000")
    urlretrieve(url, temp_dir + "process.png")

    if nq:
        nq_command = """pngnq -e .png -d %s %s""" % (nq_dir, temp_dir + "process.png")
        print nq_command
        os.system(nq_command)
        os.remove(temp_dir + "process.png")
        shutil.move(nq_dir + "process.png", temp_dir)

    if os.path.exists(out_dir + "out.png"):
        os.remove(out_dir + "out.png")
    pngout_command = """%s %s %s -y""" % (PNGOUT_PATH, temp_dir + "process.png", out_dir + "out.png")
    print pngout_command
    os.system(pngout_command)

    if not os.path.exists(out_dir + "out.png"):
        pngcrush_command = """pngcrush -rem alla -rem text %s %s""" % (temp_dir + "process.png", out_dir + "out.png")
        print pngcrush_command
        os.system(pngcrush_command)

    with open(out_dir + "out.png", "r") as out_png:
        out = base64.b64encode(out_png.read())

    return out


def process_gif(url):
    if DEBUG:
        url = url.replace("mlfw.info", "0.0.0.0:8000")
    urlretrieve(url, temp_dir + "process.gif")

    i = Image.open(temp_dir + "process.gif")

    resize = get_thumb_size(THUMB_SIZE, i.size)

    os.system("""convert %s -coalesce %s""" % ((temp_dir + "process.gif"), (temp_dir + "coalesce.gif")))
    os.system("convert %s -resize %dx%d %s" % ((temp_dir + "coalesce.gif"), resize[0], resize[1], (temp_dir + "thumb.gif")))
    with open(temp_dir + "thumb.gif", "r") as thumb_gif:
        out = base64.b64encode(thumb_gif.read())
    return out

json_request = session.get(server + "/faces/?unprocessed=1", verify=False)
#json_request = session.get(server+ "/faces/2465")

unprocesseds = json.loads(json_request.content)
#unprocesseds = [unprocesseds]

for face in unprocesseds:
    out = {"processed": True}
    print face.get("id")

    to_process = {}
    if face["thumbnails"].get("jpg") and not face["image"].lower().endswith("gif"):
        to_process["webp"] = face["image"]
    if face["thumbnails"].get("png"):
        to_process["png"] = face["thumbnails"].get("png")
    if face["image"].lower().endswith("gif"):
        to_process["gif"] = face["image"]
    if face["image"].lower().endswith("jpg") or face["image"].lower().endswith("jpeg"):
        to_process["jpeg"] = face["image"]

    if face["image"].lower().endswith("png"):
        to_process["image"] = face["image"]
        for item in ("small", "medium", "large", "huge"):
            if face["resizes"].get(item):
                if face["resizes"][item].endswith("png"):
                    out["rszformat"] = "png"
                    to_process[item] = face["resizes"][item]
    if not to_process:
        continue

    try:
        for key, value in to_process.items():
            print key
            if key == "gif":
                out[key] = process_gif(value)
            elif key == "webp":
                out[key] = process_webp(value)
            elif key == "png":
                out[key] = process_png(value, nq=True)
            elif key == "jpeg":
                out["image"] = process_jpeg(value)
            elif key in ("image", "small", "medium", "large", "huge"):
                out[key] = process_png(value, nq=False)
    except:
        print "ERROR"
        continue

    if out.get("image"):
        out["name"] = face["image"].rpartition("/")[2]
    put_request = session.put(server + "/faces/" + str(face["id"]) + "/", data=out, verify=False)
    print put_request.status_code
    if put_request.status_code != 200:
        print put_request.read()
