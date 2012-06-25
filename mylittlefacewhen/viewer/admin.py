from django.contrib import admin
from viewer import models

class Face(admin.ModelAdmin):
    pass

admin.site.register(models.Face, Face)

class Flag(admin.ModelAdmin):
    pass

admin.site.register(models.Flag, Flag)

class SourceLog(admin.ModelAdmin):
    pass

admin.site.register(models.SourceLog, SourceLog)

class TagLog(admin.ModelAdmin):
    pass

admin.site.register(models.TagLog, TagLog)

class Feedback(admin.ModelAdmin):
    pass

admin.site.register(models.Feedback, Feedback)

