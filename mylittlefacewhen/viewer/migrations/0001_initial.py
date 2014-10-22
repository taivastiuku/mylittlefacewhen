# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('htmlad', models.CharField(help_text=b'Advertisement text, may contain html.', max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(help_text=b'Datetime of change', verbose_name=b'datetime when added', auto_now=True)),
                ('source', models.URLField(default=b'', help_text=b'New source for face', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'', help_text=b'Image uploaded in base64 format. The core of this service.', max_length=256, upload_to=b'f/img/')),
                ('webp', models.ImageField(default=b'', help_text=b'WEBP formatted thumbnail, max height: 100px', upload_to=b'f/thumb/', blank=True)),
                ('jpg', models.ImageField(default=b'', help_text=b'JPG formatted thumbnail, max height: 100px', upload_to=b'f/thumb/', blank=True)),
                ('gif', models.ImageField(default=b'', help_text=b'animated GIF thumbnail, max height: 100px', upload_to=b'f/thumb/', blank=True)),
                ('png', models.ImageField(default=b'', help_text=b'transparent PNG thumbnail, max height: 100px', upload_to=b'f/thumb/', blank=True)),
                ('small', models.ImageField(default=b'', help_text=b'Resize of image fitted into 320x320 box', upload_to=b'f/rsz/', blank=True)),
                ('medium', models.ImageField(default=b'', help_text=b'Resize of image fitted into 640x640 box', upload_to=b'f/rsz/', blank=True)),
                ('large', models.ImageField(default=b'', help_text=b'Resize of image fitted into 1000x1000 box', upload_to=b'f/rsz/', blank=True)),
                ('huge', models.ImageField(default=b'', help_text=b'Resize of image fitted into 1920x1920 box', upload_to=b'f/rsz/', blank=True)),
                ('width', models.IntegerField(default=0, help_text=b'Width of image')),
                ('height', models.IntegerField(default=0, help_text=b'Height of image')),
                ('source', models.URLField(default=b'', help_text=b'Source for image', blank=True)),
                ('md5', models.CharField(default=b'', help_text=b'md5 hash of image for detecting duplicates.', max_length=32)),
                ('removed', models.BooleanField(default=False, help_text=b"Image is 'removed' and should not be shown")),
                ('comment', models.CharField(default=b'', help_text=b'Reason for deletion etc.', max_length=512, blank=True)),
                ('added', models.DateTimeField(help_text=b'Date added', verbose_name=b'date added')),
                ('accepted', models.BooleanField(default=False, help_text=b'Face has been accepted by moderator.')),
                ('processed', models.BooleanField(default=False, help_text=b'Thumbnails and resizes have been generated and compressed')),
                ('views', models.IntegerField(default=0, help_text=b'Views during last 7 days.')),
                ('hotness', models.FloatField(default=0, help_text=b'Represents newness and popularity of face.')),
                ('duplicate_of', models.ForeignKey(default=None, blank=True, to='viewer.Face', help_text=b'Current image is duplicate, redirect to duplicate_of Face', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.CharField(default=b'', help_text=b'Contact info of feedback giver', max_length=256)),
                ('image', models.ImageField(help_text=b'DEPRECATED', max_length=256, upload_to=b'upload/')),
                ('text', models.TextField(help_text=b'The feedback goes here. What is on your mind?')),
                ('datetime', models.DateTimeField(help_text=b'When the feedback was received.', verbose_name=b'datetime when added', auto_now_add=True)),
                ('useragent', models.CharField(default=b'', help_text=b'Useragent of feedback giver. Useful for bug reports.', max_length=512)),
                ('processed', models.BooleanField(default=False, help_text=b'DEPRECATED')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent', models.CharField(help_text=b'User agent of reporter.', max_length=512, null=True)),
                ('reason', models.TextField(help_text=b'Reason for report.')),
                ('face', models.ForeignKey(help_text=b'Face related to this report.', to='viewer.Face')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=b'Poninymous', help_text=b'Username of anon user', max_length=16)),
                ('text', models.CharField(default=b'', help_text=b'Comment itself', max_length=255)),
                ('client', models.IPAddressField(help_text=b'IP of the commenter')),
                ('visible', models.CharField(default=b'visible', help_text=b'If comment is visible, moderated or hidden', max_length=16, choices=[(b'moderated', b'Moderated'), (b'hidden', b'Hidden'), (b'visible', b'Visible')])),
                ('color', models.CharField(help_text=b'IP/Face specific color', max_length=6)),
                ('time', models.DateTimeField(help_text=b'Time of writing', auto_now_add=True)),
                ('face', models.ForeignKey(help_text=b'Face that is being commented', to='viewer.Face')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='changelog',
            name='face',
            field=models.ForeignKey(help_text=b'Face related to change', to='viewer.Face'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='changelog',
            name='flag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='viewer.Flag', help_text=b'Face was flagged', null=True),
            preserve_default=True,
        ),
    ]
