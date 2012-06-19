# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Feedback.contact'
        db.add_column('viewer_feedback', 'contact', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Feedback.contact'
        db.delete_column('viewer_feedback', 'contact')


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
        'viewer.face': {
            'Meta': {'object_name': 'Face'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'gif': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'huge': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '256'}),
            'jpg': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'large': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'png': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'small': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'})
        },
        'viewer.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '256'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'viewer.salute': {
            'Meta': {'object_name': 'Salute'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'viewer.sourcelog': {
            'Meta': {'object_name': 'SourceLog'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'face': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viewer.Face']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': "orm['viewer.SourceLog']"}),
            'source': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
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
