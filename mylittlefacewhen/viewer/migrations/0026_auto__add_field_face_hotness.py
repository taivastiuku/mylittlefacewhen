# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Face.hotness'
        db.add_column('viewer_face', 'hotness',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Face.hotness'
        db.delete_column('viewer_face', 'hotness')


    models = {
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'viewer.accesslog': {
            'Meta': {'object_name': 'AccessLog'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'useragent': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'viewer.advert': {
            'Meta': {'object_name': 'Advert'},
            'htmlad': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'viewer.changelog': {
            'Meta': {'object_name': 'ChangeLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Face']"}),
            'flag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Flag']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': "orm['viewer.ChangeLog']"}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        'viewer.face': {
            'Meta': {'object_name': 'Face'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'duplicate_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['viewer.Face']", 'null': 'True'}),
            'gif': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hotness': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'huge': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '256'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'large': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'md5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'png': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'small': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'viewer.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'useragent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        'viewer.flag': {
            'Meta': {'object_name': 'Flag'},
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Face']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        },
        'viewer.salute': {
            'Meta': {'object_name': 'Salute'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'viewer.tagpopularity': {
            'Meta': {'object_name': 'TagPopularity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagging.Tag']"})
        }
    }

    complete_apps = ['viewer']