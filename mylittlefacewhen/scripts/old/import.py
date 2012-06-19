"""
Old import script. Works only with local db.
Process all images in a given folder into Face objects.
This process has multiple steps.
"""

from datetime import datetime
import os
import sys
import shutil
from PIL import Image
from viewer.models import *

#directories = ["/home/inopia/mlfw2/"]#,
#	       "/home/inopia/mlfw2/"]i
image_dir="/home/inopia/mlfw/"
#directories=os.listdir(image_dir)
directories=["mlfwe"]
directories.sort()
statics = "/home/inopia/webapps/mlfw_static/"

lista = []
size = 100, 100

if not os.path.exists(statics + "original/"):
    os.mkdir(statics + "original/")
if not os.path.exists(statics + "faces/"):
    os.mkdir(statics + "faces/")
if not os.path.exists(statics + "facethumbs/"):
    os.mkdir(statics + "facethumbs/")

faces = Face.objects.order_by("id").reverse()

os.chdir("/tmp/")

if not faces:
    current_id = 1
else:
    current_id = faces[0].id + 1
for directory in directories:
    directory = image_dir + directory + "/"
    reacts = os.listdir(directory)
    reacts.sort()

    for react in reacts:
	current_ext = react.rpartition(".")[2].lower()
	filename = str(current_id)
	try:
	    im = Image.open(directory + react)

	    # Create resized version if the image is really large
	    if im.size[0] > 950 and current_ext != "gif":
		im.thumbnail((950, im.size[1]), Image.ANTIALIAS)
		if current_ext == "jpg" or current_ext == "jpeg":
		    im.save(statics + "faces/" + filename + ".jpg", "JPEG", quality=85)
		    #im.save(statics + "faces/" + filename + ".webp", "WEBP", quality=85)
		    facename = filename+".jpg"
		else:
		    im.save(statics + "faces/" + filename + ".png", "PNG", optimize=True)
		    facename = filename + ".png"
		im = Image.open(directory + react)
	    else:
		shutil.copy(directory + react, statics + "faces/" + filename + "." + current_ext)
		facename = filename + "." + current_ext
	    
	    # Trickery for PNG to make transparecy white on jpeg thumbnails
	    if im.format=="PNG":
		try:
		    i = Image.new("RGB",im.size,(255,255,255))
		    i.paste(im,(0,0,im.size[0],im.size[1],), im)
		    im = i
		except:
		    pass

	    # GIF or not
	    if im.format=="GIF":
		#ANIMATION
		print "GIF"
		ext = ".gif"
		os.system("""convert "%s" -coalesce coalesce.gif""" % (directory + react))
		os.system("convert coalesce.gif -resize 100x100 %s" % (filename + ext))
		shutil.move("./%s.gif" % filename, statics + "facethumbs/")
		webp = False
	    else:
		ext = ".jpg"
		im.thumbnail(size, Image.ANTIALIAS)
		full = statics + "facethumbs/" + filename
		im.save(full + ext, "JPEG", quality=70, optimize=True)
		if im.mode == "L":
		    i = im.convert("RGB")
		    i.save(full + ".webp", "WEBP", quality=30)
		else:
		    im.save(full + ".webp", "WEBP", quality=30)
		webp = True

	    shutil.copy(directory + react, statics + "original/")
	    f = Face(original = react,
		     filename = facename, 
		     thumbname = filename + ext,
		     webp = webp,
		     added = datetime.utcnow())
	    f.save()
	    f.tags = "untagged"
	    TagLog.new(f)
	    print str((f.id, f.filename, f.webp, f.original, f.thumbname))
	    current_id += 1
	except IOError:
	    print "cannot create thumbnail for %s" % react
