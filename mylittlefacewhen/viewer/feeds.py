from django.contrib.syndication.views import Feed

from viewer import models

class LatestAcceptedImages(Feed):
    """
    RSS feed of new accepted images
    """
    title = "MyLittleFaceWhen.com image feed"
    link = "/"
    description = "Newest pony reactions accepted at MyLittleFaceWhen.com"

    def items(self):
        return models.Face.objects.filter(accepted=True, removed=False).order_by('-added')[:20]

    def item_title(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return """<img src="http://mylittlefacewhen.com%s" alt="" /><br /><small><a href="http://mylittlefacewhen.com/submit/">Send more ponies</a></small>""" % item.get_image("medium")

class LatestUnreviewedImages(Feed):
    """
    RSS feed of new unreviewed images
    """
    title = "MyLittleFaceWhen.com unreviewed image feed"
    link = "/"
    description = "Newest unreviewed image submissions at MyLittleFaceWhen.com"

    def items(self):
        return models.Face.objects.filter(accepted=False).order_by('-added')[:20]

    def item_title(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return """<img src="http://mylittlefacewhen.com%s" alt="" /><br /><small>"""
