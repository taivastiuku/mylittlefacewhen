import os
import sys

rszdir = "/home/inopia/webapps/mlfw_media/f/rsz/"
#nqdir = thumbsdir + "png/"

l = os.listdir(rszdir)
l.sort()

for imagefile in l:
    part = imagefile.lstrip("mlfw").partition(".")
    ext = part[2].lower()
    if part[0] in ("save", "png"):
        continue
    try:
        iid = int(part[0].partition("_")[0])
    except:
        print imagefile
        sys.exit()

    if ext == "png" and iid > 1535:
        os.system("~/pngout-static " + rszdir + imagefile)
#        os.system("pngnq -s1 -e .png -d %s %s%s" % ( nqdir, thumbsdir, imagefile))

#l = os.listdir(nqdir)

#for imagefile in l:
#    if imagefile.endswith(".png"):
        #os.system("~/pngout-static " + thumbsdir + imagefile)
