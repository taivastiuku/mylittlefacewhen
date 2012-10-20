from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from viewer import models


class Face(ForeignKeyAutocompleteAdmin):
    related_search_fields = {"duplicate_of": ["id"]}

admin.site.register(models.Face, Face)


class Flag(ForeignKeyAutocompleteAdmin):
    related_search_fields = {"face": ["id"]}

admin.site.register(models.Flag, Flag)


class ChangeLog(ForeignKeyAutocompleteAdmin):
    related_search_fields = {"face": ["id"]}

admin.site.register(models.ChangeLog, ChangeLog)


class Feedback(admin.ModelAdmin):
    pass

admin.site.register(models.Feedback, Feedback)
