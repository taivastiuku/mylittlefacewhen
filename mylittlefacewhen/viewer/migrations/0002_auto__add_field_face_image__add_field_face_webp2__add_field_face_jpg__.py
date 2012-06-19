# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Face.image'
        db.add_column('viewer_face', 'image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Face.webp2'
        db.add_column('viewer_face', 'webp2', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Face.jpg'
        db.add_column('viewer_face', 'jpg', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Face.gif'
        db.add_column('viewer_face', 'gif', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Face.png'
        db.add_column('viewer_face', 'png', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Face.image'
        db.delete_column('viewer_face', 'image')

        # Deleting field 'Face.webp2'
        db.delete_column('viewer_face', 'webp2')

        # Deleting field 'Face.jpg'
        db.delete_column('viewer_face', 'jpg')

        # Deleting field 'Face.gif'
        db.delete_column('viewer_face', 'gif')

        # Deleting field 'Face.png'
        db.delete_column('viewer_face', 'png')


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
