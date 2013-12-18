# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TagPopularity'
        db.delete_table(u'viewer_tagpopularity')

        # Deleting model 'AccessLog'
        db.delete_table(u'viewer_accesslog')

        # Adding model 'UserComment'
        db.create_table(u'viewer_usercomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('username', self.gf('django.db.models.fields.CharField')(default='Poninymous', max_length=16)),
            ('text', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('client', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('visible', self.gf('django.db.models.fields.CharField')(default='visible', max_length=16)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'viewer', ['UserComment'])


    def backwards(self, orm):
        # Adding model 'TagPopularity'
        db.create_table(u'viewer_tagpopularity', (
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.Tag'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'viewer', ['TagPopularity'])

        # Adding model 'AccessLog'
        db.create_table(u'viewer_accesslog', (
            ('referrer', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('resource', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('accessed', self.gf('django.db.models.fields.DateTimeField')()),
            ('useragent', self.gf('django.db.models.fields.CharField')(max_length=512)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'viewer', ['AccessLog'])

        # Deleting model 'UserComment'
        db.delete_table(u'viewer_usercomment')


    models = {
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
        u'viewer.usercomment': {
            'Meta': {'object_name': 'UserComment'},
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viewer.Face']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'Poninymous'", 'max_length': '16'}),
            'visible': ('django.db.models.fields.CharField', [], {'default': "'visible'", 'max_length': '16'})
        }
    }

    complete_apps = ['viewer']