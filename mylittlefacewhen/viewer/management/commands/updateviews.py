from django.core.management.base import BaseCommand
from datetime import timedelta
from datetime import datetime
from viewer.models import *


class Command(BaseCommand):
    args = "no args plz"
    help = "Update Face views count and TagPopularity counts from AccessLog data"
    mediadir = "/media/"
    td = timedelta(days=7)

    def handle(self, *args, **options):

        tags = {}
        AccessLog.objects.raw("""DELETE FROM viewer_accesslog WHERE accessed<'%s'""" % (datetime.utcnow()-self.td).strftime('%Y-%m-%d 00:00:00'))

        for face in Face.objects.all():
            path = self.mediadir + str(face.image)
            #views = AccessLog.objects.filter(resource=path).count()
            views = AccessLog.objects.filter(resource=str(face.id)).count()
            face.views = views
            face.save()
            
            for tag in face.tags:
                if not tags.get(tag.id):
                    tags[tag.id] = [tag,face.views]
                else:
                    tags[tag.id][1] += face.views

        for key, value in tags.items():
            tp = TagPopularity.objects.filter(tag=value[0])
            if tp:
                tp[0].popularity = value[1]
                tp[0].save()
            else:
                TagPopularity(tag=value[0], popularity=value[1]).save()
 
