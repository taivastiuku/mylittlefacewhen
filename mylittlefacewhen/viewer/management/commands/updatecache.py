from datetime import datetime

from django.core.management.base import BaseCommand

from viewer.helpers import UPDATED


class Command(BaseCommand):
    args = "no args plz"
    help = "Updates appcache"
    cachefile = "/home/inopia/webapps/mlfw_static/dictionary.appcache"

    def handle(self, *args, **options):
        files = [
            "/static/favicon.ico",
            "/static/empty.gif",
            "/static/dash.gif",
            "/static/errors/derpy-404.png",
            "/static/errors/derpy-500.png",
            "/static/icons/red_flag_24.png",
            "/static/icons/white_flag_24.png",
            "/static/offline.html",
            "/static/css/responsive.css",
            "/static/css/normalize.css",
            "/static/css/rainbow_dash_always_dresses_in.css",
            "/static/css/rarity.css",
            "/static/css/jquery-ui-1.10.3.custom.css",
            "/static/app.js"]

        for index in xrange(0, len(files)):
            if files[index].endswith("js") or files[index].endswith("css"):
                files[index] = files[index] + "?" + str(UPDATED)

#        pages = [
#            "/submit/",
#            "/f/",
#            "/develop/",
#            "/feedback/",
#            "/tags/",
#            "/toplist/",
#            "/search/",
#            "/randoms/"]

#        for item in os.listdir("/home/inopia/webapps/mlfw_static/lib/"):
#            files.append("/static/lib/" + item)

#        for item in os.listdir("/home/inopia/webapps/mlfw_static/js/"):
#            if item.endswith(".js"):
#                files.append("/static/js/" + item)

#        for item in os.listdir("/home/inopia/webapps/mlfw_static/js/views/"):
#            if item.endswith(".js"):
#                files.append("/static/js/views/" + item)

        s = "CACHE MANIFEST\n#%s\nCACHE:\n"
        for filu in files:
            s += filu + "\n"
        s = s % datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#        for face in Face.objects.filter(accepted=1).order_by("-id")[0:30]:
#            for thumb in ("webp", "png", "jpg"):
#                if getattr(face, thumb):
#                    s += getattr(face, thumb).url + "\n"
        s += "NETWORK:\n"
        s += "*\nhttp://*\nhttps://*\n"
        s += "/api/\n"
#        s += "FALLBACK:\n"
#        for page in pages:
#            s += page + " /static/offline.html\n"

        with open(self.cachefile, "w") as cache:
            cache.write(s)
