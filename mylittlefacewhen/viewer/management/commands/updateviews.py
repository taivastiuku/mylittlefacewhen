from datetime import datetime, timedelta
import os
from math import log

from django.core.management.base import BaseCommand
from django.utils import simplejson as json

from viewer import models


def hotness(score, date):
    td = datetime.now() - date
    factor = (600.0 - td.days)/500.0
    order = log(max(abs(score*factor), 1), 10)
    return round(order, 7)


class Command(BaseCommand):
    args = "no args plz"
    help = "Update Face views from log data"
    accesslogdir = "/home/inopia/access/"
    td = timedelta(days=7)

    def handle(self, *args, **options):
        time = datetime.now() - self.td
        timestring = str("%d%d%d" % (time.year, time.month, time.day))

        all_views = {}
        logs = os.listdir(self.accesslogdir)
        for log in logs:
            if log.split("-")[1] >= timestring:
                print log
                with open(self.accesslogdir + log) as logfile:
                    data = json.loads(logfile.read())
                    for id, views in data.iteritems():
                        all_views[id] = all_views.get(id, 0) + views

        l = len(all_views)
        i = 1

        for id, views in all_views.iteritems():
            print "%d/%d" % (i, l)
            i += 1
            try:
                f = models.Face.objects.get(id=id)
            except:
                # Image may have been deleted -> get fails
                continue
            f.views = views
            f.hotness = hotness(views, f.added)
            print f.hotness
            f.save()
