"""
Custom template loader, template and templatetag to handle mustache templates.

PystacheTemplate and Loader are pretty much copies of their parent classes
with one line modifications or so.

do_mustache allows template tags like
{% mustache "main.mustache" %}
and
{% mustache "main.mustache" main_vars %}

where main_vars is a dict containing variables needed by the mustache.

"""

from django import template
from django.conf import settings
from django.template import Template
from django.template.base import TemplateEncodingError, TemplateDoesNotExist
from django.template.loader import make_origin
from django.template.loaders import filesystem
from django.utils.encoding import smart_unicode
from pystache import render as pystache_render

register = template.Library()


class PystacheTemplate(Template):

    def __init__(self, template_string, origin=None, name='<Unknown Template>'):
        try:
            template_string = smart_unicode(template_string)
        except:
            raise TemplateEncodingError("Templates can only be constructed from unicode or UTF-8 strings.")
        if settings.TEMPLATE_DEBUG and origin is None:
            origin = template.StringOrigin(template_string)
        self.nodelist = template_string
        self.name = name

    def __iter__(self):
        pass

    def render(self, context):
        return pystache_render(self.nodelist, context)


class Loader(filesystem.Loader):

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_name.endswith(".mustache"):
            return []
        else:
            return super(Loader, self).get_template_sources(template_name, template_dirs)

    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(template_name, template_dirs)
        origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
        try:
            template = PystacheTemplate(source, origin, template_name)
            return template, None
        except TemplateDoesNotExist:
            # If compiling the template we found raises TemplateDoesNotExist,
            # back off to returning the source and display name for the
            # template we were asked to load.
            # This allows for correct identification (later) of the actual
            # template that does not exist.
            return source, display_name


class MustacheNode(template.Node):

    def __init__(self, raw_template, data):
        self.tpl = template.Variable(raw_template)
        if data:
            self.data = template.Variable(data)
        else:
            self.data = None

    def render(self, context):
        if self.data:
            data = self.data.resolve(context)
        else:
            data = {}
        tpl = self.tpl.resolve(context)
        return template.loader.get_template(tpl).render(data)


@register.tag(name="mustache")
def do_mustache(parser, token):
    contents = token.split_contents()
    if len(contents) == 2:
        tag_name, tpl = contents
        data = None
    else:
        tag_name, tpl, data = contents

    return MustacheNode(tpl, data)
