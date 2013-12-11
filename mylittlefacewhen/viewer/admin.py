from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from viewer import models


def accept_face(modeladmin, request, queryset):
    queryset.update(accepted=True)


def remove_face(modeladmin, request, queryset):
    queryset.update(removed=True)


class Face(ForeignKeyAutocompleteAdmin):
    list_display = ["id", "title", "thumb", "changes", "taglist", "accepted", "removed", "processed",
                    "views", "hotness", "width", "height"]
    list_filter = ["accepted", "processed", "removed"]
    readonly_fields = [
        "image", "webp", "jpg", "gif", "png", "small", "medium", "large", "huge", "width", "height", "md5",
        "added", "views", "hotness"]
    search_fields = ["id"]
    related_search_fields = {"duplicate_of": ["id"]}

    actions = [accept_face, remove_face]

    def thumb(self, obj):
        try:
            return "<a href='/f/%d/'><img src='%s'></a>" % (obj.id, obj.thumbnail.url)
        except:
            return
    thumb.allow_tags = True

    def changes(self, obj):
        return "<a href='/admin/viewer/changelog/?face__id=%d'>changes</a>" % obj.id
    changes.allow_tags = True

    def title(self, obj):
        return obj.title[:100]

admin.site.register(models.Face, Face)


class Flag(ForeignKeyAutocompleteAdmin):
    list_display = ["id", "thumb", "admin_link", "reason"]

    related_search_fields = {"face": ["id"]}

    def thumb(self, obj):
        try:
            return "<a href='/f/%d/'><img src='%s'></a>" % (obj.face.id, obj.face.thumbnail.url)
        except:
            return
    thumb.allow_tags = True

    def admin_link(self, obj):
        return "<a href='/admin/viewer/face/?id=%d'>admin link</a>" % obj.face.id
    admin_link.allow_tags = True


admin.site.register(models.Flag, Flag)


def undo_change(modeladmin, request, queryset):
    for item in queryset:
        item.undo()


class ChangeLog(ForeignKeyAutocompleteAdmin):
    list_display = ["id", "thumb", "admin_link", "age", "added_tags", "removed_tags", "same_tags", "source_change"]

    related_search_fields = {"face": ["id"]}
    actions = [undo_change]

    def thumb(self, obj):
        try:
            return "<a href='/f/%d/'><img src='%s'></a>" % (obj.face.id, obj.face.thumbnail.url)
        except:
            return
    thumb.allow_tags = True

    def admin_link(self, obj):
        return "<a href='/admin/viewer/face/?id=%d'>admin link</a>" % obj.face.id
    admin_link.allow_tags = True

admin.site.register(models.ChangeLog, ChangeLog)


class Feedback(admin.ModelAdmin):
    pass

admin.site.register(models.Feedback, Feedback)
