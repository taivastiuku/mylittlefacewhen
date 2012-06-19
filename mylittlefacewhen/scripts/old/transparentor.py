"""
Find all pngs that have RGBA mode and add "transparent" tag to them.
"""

from viewer import models
from PIL import Image
from tagging.models import Tag

for face in models.Face.objects.all():
    if not face.image.name.lower().endswith(".png"):
        continue
    if face.tags.filter(name="transparent"):
        continue

    print face.image
    image = Image.open(face.image.path)
    if image.format == "PNG" and image.mode == "RGBA":
        Tag.objects.add_tag(face, "transparent")
        models.TagLog.new(face)
