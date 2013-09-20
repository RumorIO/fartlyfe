# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Podcast'
        db.create_table(u'podcasts_podcast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('itunes_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'podcasts', ['Podcast'])

        # Adding model 'Episode'
        db.create_table(u'podcasts_episode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('podcast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['podcasts.Podcast'])),
            ('location', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'podcasts', ['Episode'])


    def backwards(self, orm):
        # Deleting model 'Podcast'
        db.delete_table(u'podcasts_podcast')

        # Deleting model 'Episode'
        db.delete_table(u'podcasts_episode')


    models = {
        u'podcasts.episode': {
            'Meta': {'ordering': "['title']", 'object_name': 'Episode'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'podcast': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['podcasts.Podcast']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'podcasts.podcast': {
            'Meta': {'ordering': "['title']", 'object_name': 'Podcast'},
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itunes_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['podcasts']