# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SourceLog'
        db.delete_table('viewer_sourcelog')

        # Deleting model 'TagLog'
        db.delete_table('viewer_taglog')

        # Adding model 'ChangeLog'
        db.create_table('viewer_changelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('prev', self.gf('django.db.models.fields.related.OneToOneField')(related_name='next', unique=True, null=True, to=orm['viewer.ChangeLog'])),
            ('source', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('flag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Flag'], null=True)),
        ))
        db.send_create_signal('viewer', ['ChangeLog'])


    def backwards(self, orm):
        # Adding model 'SourceLog'
        db.create_table('viewer_sourcelog', (
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('source', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('prev', self.gf('django.db.models.fields.related.OneToOneField')(related_name='next', unique=True, null=True, to=orm['viewer.SourceLog'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('viewer', ['SourceLog'])

        # Adding model 'TagLog'
        db.create_table('viewer_taglog', (
            ('prev', self.gf('django.db.models.fields.related.OneToOneField')(related_name='next', unique=True, null=True, to=orm['viewer.TagLog'])),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('viewer', ['TagLog'])

        # Deleting model 'ChangeLog'
        db.delete_table('viewer_changelog')


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
            'huge': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '256'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'large': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
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