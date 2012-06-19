from viewer.models import *

for face in Face.objects.all():
    if face.huge:
        face.huge = face.huge.path[32:]
    if face.large:
        face.large = face.large.path[32:]
    if face.medium:
        face.medium = face.medium.path[32:]
    if face.small:
        face.small = face.small.path[32:]
    face.save()
