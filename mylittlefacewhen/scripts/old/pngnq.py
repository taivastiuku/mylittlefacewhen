import os

thumbsdir = "/home/inopia/webapps/mlfw_media/f/rsz/"
nqdir = thumbsdir + "png/"

l = os.listdir(thumbsdir)

#for imagefile in l:
#    if imagefile.endswith(".png"):
#        os.system("pngnq -s1 -e .png -d %s %s%s" % ( nqdir, thumbsdir, imagefile))

#l = os.listdir(nqdir)

for imagefile in l:
    if imagefile.endswith(".png"):
        os.system("~/pngout-static " + thumbsdir + imagefile)
