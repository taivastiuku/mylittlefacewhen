# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ChangeLog.prev'
        db.delete_column(u'viewer_changelog', 'prev_id')


        # Changing field 'ChangeLog.flag'
        db.alter_column(u'viewer_changelog', 'flag_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Flag'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):
        # Adding field 'ChangeLog.prev'
        db.add_column(u'viewer_changelog', 'prev',
                      self.gf('django.db.models.fields.related.OneToOneField')(related_name='next', unique=True, null=True, to=orm['viewer.ChangeLog']),
                      keep_default=False)


        # Changing field 'ChangeLog.flag'
        db.alter_column(u'viewer_changelog', 'flag_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Flag'], null=True))

    models = {
        u'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        u'viewer.accesslog': {
            'Meta': {'object_name': 'AccessLog'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'useragent': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'viewer.advert': {
            'Meta': {'object_name': 'Advert'},
            'htmlad': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'viewer.changelog': {
            'Meta': {'object_name': 'ChangeLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viewer.Face']"}),
            'flag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viewer.Flag']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'viewer.face': {
            'Meta': {'object_name': 'Face'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'duplicate_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['viewer.Face']", 'null': 'True', 'blank': 'True'}),
            'gif': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hotness': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'huge': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '256'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'large': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'png': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'small': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'viewer.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'useragent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        u'viewer.flag': {
            'Meta': {'object_name': 'Flag'},
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viewer.Face']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        },
        u'viewer.tagpopularity': {
            'Meta': {'object_name': 'TagPopularity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tagging.Tag']"})
        }
    }

    complete_apps = ['viewer']