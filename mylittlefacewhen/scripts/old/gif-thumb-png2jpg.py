from viewer.models import Face
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from cStringIO import StringIO

try:
    from PIL import Image
except:
    import Image

for face in Face.objects.all():
    if not face.gif or not face.png:
        continue
    print "id: " + str(face.id)

    thumb = Image.open(face.png.path)

    thumb = thumb.convert("RGB")
    
    #JPEG
    temp_handle = StringIO()
    thumb.save(temp_handle, "JPEG", quality=70, optimize=True)
    temp_handle.seek(0)
    name = "mlfw" + str(face.id) + ".jpg"
    suf = SimpleUploadedFile(name,
                             temp_handle.read(),
                             content_type="image/jpeg")
    face.jpg.save(name, suf, save=False)
    temp_handle.close()

    #WEBP
    temp_handle = StringIO()
    thumb.save(temp_handle, "WEBP", quality=30)
    temp_handle.seek(0)
    name = "mlfw" + str(face.id) + ".webp"
    suf = SimpleUploadedFile(name,
                             temp_handle.read(),
                             content_type="image/webp")
    face.webp.save(name, suf, save=False)
    temp_handle.close()

    #remove old PNG
    try:
        os.remove(face.png.path)
    except:
        pass
    face.png = ""
    face.save()
