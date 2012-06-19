# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Face'
        db.create_table('viewer_face', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('thumbname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('webp', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added', self.gf('django.db.models.fields.DateTimeField')()),
            ('retired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('viewer', ['Face'])

        # Adding model 'Salute'
        db.create_table('viewer_salute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('thumbnail', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('viewer', ['Salute'])

        # Adding model 'Comment'
        db.create_table('viewer_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('viewer', ['Comment'])

        # Adding model 'Introduction'
        db.create_table('viewer_introduction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('imagenames', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('viewer', ['Introduction'])

        # Adding model 'TagLog'
        db.create_table('viewer_taglog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('face', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viewer.Face'])),
            ('prev', self.gf('django.db.models.fields.related.OneToOneField')(related_name='next', unique=True, null=True, to=orm['viewer.TagLog'])),
        ))
        db.send_create_signal('viewer', ['TagLog'])

        # Adding model 'Feedback'
        db.create_table('viewer_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('viewer', ['Feedback'])

        # Adding model 'APILog'
        db.create_table('viewer_apilog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('useragent', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('get', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('post', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('viewer', ['APILog'])

        # Adding model 'TagPopularity'
        db.create_table('viewer_tagpopularity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagging.Tag'])),
            ('popularity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('viewer', ['TagPopularity'])


    def backwards(self, orm):
        
        # Deleting model 'Face'
        db.delete_table('viewer_face')

        # Deleting model 'Salute'
        db.delete_table('viewer_salute')

        # Deleting model 'Comment'
        db.delete_table('viewer_comment')

        # Deleting model 'Introduction'
        db.delete_table('viewer_introduction')

        # Deleting model 'TagLog'
        db.delete_table('viewer_taglog')

        # Deleting model 'Feedback'
        db.delete_table('viewer_feedback')

        # Deleting model 'APILog'
        db.delete_table('viewer_apilog')

        # Deleting model 'TagPopularity'
        db.delete_table('viewer_tagpopularity')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumbname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'webp': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
