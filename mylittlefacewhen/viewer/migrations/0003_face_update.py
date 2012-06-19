# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for face in orm.Face.objects.all():
            face.image = "f/img/" + face.original
            if face.webp:
                face.webp2 = "f/thumb/" + str(face.id) + ".webp"
                face.jpg = "f/thumb/" + str(face.id) + ".jpg"
            else:
                face.gif = "f/thumb/" + str(face.id) + ".gif"
            face.save()

    def backwards(self, orm):
        raise RuntimeError("Irreversable migration!")


    models = {
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'viewer.apilog': {
            'Meta': {'object_name': 'APILog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'get': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'useragent': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'viewer.comment': {
            'Meta': {'object_name': 'Comment'},
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Face']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        'viewer.face': {
            'Meta': {'object_name': 'Face'},
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'gif': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'png': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumbname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'webp2': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'})
        },
        'viewer.face2': {
            'Meta': {'object_name': 'Face2'},
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'gif': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagefile': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'png': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'viewer.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'viewer.introduction': {
            'Meta': {'object_name': 'Introduction'},
            'data': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagenames': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'viewer.salute': {
            'Meta': {'object_name': 'Salute'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'viewer.taglog': {
            'Meta': {'object_name': 'TagLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Face']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': "orm['viewer.TagLog']"})
        },
        'viewer.tagpopularity': {
            'Meta': {'object_name': 'TagPopularity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagging.Tag']"})
        }
    }

    complete_apps = ['viewer']
