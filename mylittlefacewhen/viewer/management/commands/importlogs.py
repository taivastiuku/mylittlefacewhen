from django.core.management.base import BaseCommand
import os
import sys
from datetime import datetime
from datetime import timedelta
import time

from viewer.models import AccessLog


class Command(BaseCommand):
    args = "no args plz"
    help = "Import image access data from apache access logs."

    def handle(self, *args, **options):
        timeformat = "%d/%b/%Y:%H:%M:%S"
        indexes = range(1,5)
        indexes.reverse()

        for i in indexes:
            logname = "/home/inopia/logs/frontend/access_mylittlefacewhen.log.%d" % i

            with open(logname) as log:
                print logname
                first = True

                for l in log:
                    """ 
                    Parsing fails sometimes for some reason. This happens so 
                    infrequently that the erring row is just discarded.
                    """
                    try:
                        out = {}
                        part = l.partition(" - - ")
                        out["ip"] = part[0]
                        l = part[2].strip().strip("[")
                        part = l.partition("]")
                        timepart = part[0].partition(" ")
                        out["accessed"] = datetime.fromtimestamp(time.mktime(time.strptime(part[0].partition(" ")[0],timeformat))) + timedelta(hours=6)
                        l = part[2].strip().strip('"')
                        part = l.partition(' ')
                        out["method"] = part[0]
                        l = part[2].strip()
                        part = l.partition(' ')
                        out["resource"] = part[0][:512]
                        if out["resource"].startswith("/media/f/rsz/") or out["resource"].startswith("/media/f/img/"):
                            out["resource"] = out["resource"].rpartition(".")[0].rpartition("_")[0].rpartition("/")[2].strip("mlfw")
                        else:
                            continue


                        l = part[2].partition('"')[2].partition('"')[2]
                        part = l.partition('"')
                        out["referrer"] = part[0][:1024]
                        out["useragent"] = part[2].strip().strip('"')[:512]
                        if first:
                            if AccessLog.objects.filter(**out):
                                print "already processed"
                                break
                            else:
                                first = False
                        # oh god i love **
                        AccessLog(**out).save()
                        
                    except:
                        try:
                            print "Error: " + l
                        except:
                            print "Error."
