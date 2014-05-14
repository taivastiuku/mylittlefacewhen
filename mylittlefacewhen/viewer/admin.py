from django.contrib import admin
#from django_extensions.admin import ForeignKeyAutocompleteAdmin

from viewer import models


def accept_face(modeladmin, request, queryset):
    queryset.update(accepted=True)


def remove_face(modeladmin, request, queryset):
    queryset.update(removed=True)


class Face(admin.ModelAdmin):
    list_display = ["id", "title", "thumb", "changes", "taglist", "accepted", "removed",
                    "views", "hotness", "width", "height"]
    list_filter = ["accepted", "removed"]
    readonly_fields = [
        "image", "webp", "jpg", "gif", "png", "small", "medium", "large", "huge", "width", "height", "md5",
        "added", "views", "hotness"]
    search_fields = ["id"]
#    related_search_fields = {"duplicate_of": ["id"]}

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


class Flag(admin.ModelAdmin):
    list_display = ["id", "thumb", "admin_link", "reason"]

#    related_search_fields = {"face": ["id"]}

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


class ChangeLog(admin.ModelAdmin):
    objects = models.ChangeLog.objects.filter(face__removed=False, face__accepted=True)
    list_display = ["id", "thumb", "admin_link", "age", "added_tags", "removed_tags", "same_tags", "source_change"]

#    related_search_fields = {"face": ["id"]}
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


def moderate_comment(modeladmin, request, queryset):
    queryset.update(visible="moderated")
    face_ids = set()
    for item in queryset:
        if item.face_id not in face_ids:
            item.face.update_comments()
            face_ids.add(item.face_id)


def unmoderate_comment(modeladmin, request, queryset):
    queryset.update(visible="visible")
    face_ids = set()
    for item in queryset:
        if item.face_id not in face_ids:
            item.face.update_comments()
            face_ids.add(item.face_id)


class UserComment(admin.ModelAdmin):
    list_display = ["id", "thread", "thumb", "comment", "ip", "visible"]
    list_filter = ["visible"]
    search_fields = ["username", "client"]
    actions = [moderate_comment, unmoderate_comment]

    def comment(self, obj):
        return "<span style='color: #%s'>%s: </span>%s" % (obj.color, obj.username, obj.text)
    comment.allow_tags = True

    def thread(self, obj):
        return "<a href='/admin/viewer/usercomment/?face=%d'>thread</a>" % obj.face_id
    thread.allow_tags = True

    def thumb(self, obj):
        try:
            return "<a href='/f/%d/'><img src='%s'></a>" % (obj.face.id, obj.face.thumbnail.url)
        except:
            return
    thumb.allow_tags = True

    def ip(self, obj):
        return "<a href='/admin/viewer/usercomment/?client=%s'>%s</a>" % (obj.client, obj.client)
    ip.allow_tags = True

admin.site.register(models.UserComment, UserComment)
