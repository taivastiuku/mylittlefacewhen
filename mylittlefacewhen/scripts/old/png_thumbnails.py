"""
Creates png thumbnail of all the RGBA images in the database.
"""

from viewer.models import Face
from PIL import Image

THUMB_SIZE = (100,100)
PATH = "/home/inopia/webapps/mlfw_media/f/thumb/"

for face in Face.objects.all():
    format = face.image.path.rsplit(".")[1].lower()
    if format != "png":
        continue
   
    i = Image.open(face.image)
    
    if i.mode == "RGBA":
        i.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        namepath = PATH + str(face.id) + ".png"
        i.save(namepath, "PNG", optimize=True)
        face.png = namepath
        face.save()
