from viewer.models import Face
import os
import shutil
SIZES = (120, 160, 320, 640, 1000)
SIZENAMES = ("thumb", "small", "medium", "large", "huge")



for face in Face.objects.filter(id__gte=1536):
#    if not face.image.name.startswith("f/img/mlfw"):
    print str(face.id) + ": " + face.image.name
    #namepart = face.image.name.rpartition("/")
    #relpath = namepart[0]
    #new_name = "/mlfw" + str(face.id) + "_" + namepart[2]
    #part = face.image.path.rpartition("/")
    #path = part[0]

    #there shouldnt be stuff with same name
    #shutil.copy(face.image.path, path + new_name)
    #face.image = relpath + new_name
    #face.save()

    if face.tags.filter(name="transparent"):
        face.generateImages("png")
    else:
        face.generateImages("jpg")

    face.processed = False
    for ext in ("gif", "webp",):
        if getattr(face, ext):
            try:
                os.remove(getattr(face, ext).path)
            except:
                pass
            setattr(face, ext, "")
    face.save()
