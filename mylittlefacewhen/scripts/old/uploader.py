import os
import sys
import requests
import shutil
import base64

DEBUG = False

logininfo = {
    "username":"",
    "password":"",
    }
server = "https://mylittlefacewhen.com/api"

if DEBUG:
    server = "http://0.0.0.0:8000/api"

source_dir="/home/inopia/upload/"
error_dir="/home/inopia/failed/"

faces = os.listdir(source_dir)
faces.sort()
if not faces:
    sys.exit(0)

session = requests.session()
login_request = session.post(server + "/login/", data=logininfo)

if login_request.status_code != 200:
    sys.exit("login failed: %s" % login_request.read()[0:100])


for face in faces:
    print face
    out = {}
    with open(source_dir + face, "r") as image_file:
        out["image"] = base64.b64encode(image_file.read())
    out["name"] = face
    out["accepted"] = True
    upload_request = session.post(server + "/faces/", data = out)
    print upload_request.status_code
    if upload_request.status_code != 200:
        shutil.move(source_dir+face, error_dir)
        print upload_request.read()
        break
    elif not DEBUG:
        os.remove(source_dir+face)


