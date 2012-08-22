from django.contrib import admin
from viewer import models

class Face(admin.ModelAdmin):
    pass

admin.site.register(models.Face, Face)

class Flag(admin.ModelAdmin):
    pass

admin.site.register(models.Flag, Flag)

class ChangeLog(admin.ModelAdmin):
    pass

admin.site.register(models.ChangeLog, ChangeLog)

class Feedback(admin.ModelAdmin):
    pass

admin.site.register(models.Feedback, Feedback)
