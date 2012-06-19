#!/usr/bin/env python
# -- coding: utf-8 --

import cairo
from cStringIO import StringIO

try:
    import Image
except:
    from PIL import Image

def _getExtents(text, font_size, font_family, slant, weight):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    ctx = cairo.Context(surface)
    ctx.select_font_face(font_family, slant, weight)
    ctx.set_font_size(font_size)
    ext1 = ctx.text_extents("qÖ")
    ext2 = ctx.text_extents(text)
    return (ext2[0], ext1[1], ext2[2], ext1[3])

def generateText(text, fill=(1,1,1), stroke=(0,0,0), line_width=2, weight=cairo.FONT_WEIGHT_NORMAL, slant=cairo.FONT_SLANT_NORMAL, font_family="sans-serif", font_size=50.0, image=None):

    extent = _getExtents(text, font_size, font_family, slant, weight)
    width, height = int(extent[2] + 1), int(extent[3] + 2)

    if image:
        i_width, i_height = image.size
        w_scale = (i_width)/(width*0.95)
        h_scale = (i_height/2)/height
        font_size=font_size * min(w_scale, h_scale)
        extent = _getExtents(text, font_size, font_family, slant, weight)
        width, height = int(extent[2] + 1), int(extent[3] + 2)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    ctx.move_to(-extent[0], abs(extent[1]))
    ctx.select_font_face(font_family, slant, weight)
    ctx.set_font_size(font_size)
    ctx.text_path(text)
    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(line_width)
    ctx.stroke()

    temp_handle = StringIO()
    surface.write_to_png(temp_handle)
    temp_handle.seek(0)
    return Image.open(temp_handle)

def paste(image, text, location):
    i_width, i_height = image.size

    text.thumbnail((i_width-4, i_height*1/2) , Image.ANTIALIAS)
    t_width, t_height = text.size


    if location == "N":
        x0 = i_width/2-t_width/2
        y0 = 1
    elif location == "S":
        x0 = i_width/2-t_width/2
        y0 = i_height - t_height - 1

    x1 = t_width + x0
    y1 = t_height + y0
    image.paste(text, (x0,y0,x1,y1), text)
    return image



