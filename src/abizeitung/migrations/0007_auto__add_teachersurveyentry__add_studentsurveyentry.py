# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeacherSurveyEntry'
        db.create_table(u'abizeitung_teachersurveyentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abizeitung.Student'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abizeitung.Teacher'])),
        ))
        db.send_create_signal(u'abizeitung', ['TeacherSurveyEntry'])

        # Adding model 'StudentSurveyEntry'
        db.create_table(u'abizeitung_studentsurveyentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student', to=orm['abizeitung.Student'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choice', to=orm['abizeitung.Student'])),
        ))
        db.send_create_signal(u'abizeitung', ['StudentSurveyEntry'])

        # Adding M2M table for field entries on 'TeacherSurvey'
        m2m_table_name = db.shorten_name(u'abizeitung_teachersurvey_entries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teachersurvey', models.ForeignKey(orm[u'abizeitung.teachersurvey'], null=False)),
            ('teachersurveyentry', models.ForeignKey(orm[u'abizeitung.teachersurveyentry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['teachersurvey_id', 'teachersurveyentry_id'])

        # Adding M2M table for field entries on 'StudentSurvey'
        m2m_table_name = db.shorten_name(u'abizeitung_studentsurvey_entries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentsurvey', models.ForeignKey(orm[u'abizeitung.studentsurvey'], null=False)),
            ('studentsurveyentry', models.ForeignKey(orm[u'abizeitung.studentsurveyentry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['studentsurvey_id', 'studentsurveyentry_id'])


    def backwards(self, orm):
        # Deleting model 'TeacherSurveyEntry'
        db.delete_table(u'abizeitung_teachersurveyentry')

        # Deleting model 'StudentSurveyEntry'
        db.delete_table(u'abizeitung_studentsurveyentry')

        # Removing M2M table for field entries on 'TeacherSurvey'
        db.delete_table(db.shorten_name(u'abizeitung_teachersurvey_entries'))

        # Removing M2M table for field entries on 'StudentSurvey'
        db.delete_table(db.shorten_name(u'abizeitung_studentsurvey_entries'))


    models = {
        u'abizeitung.student': {
            'Meta': {'ordering': "['user__first_name', 'user__last_name']", 'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['abizeitung.Teacher']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'abizeitung.studentsurvey': {
            'Meta': {'ordering': "['title']", 'object_name': 'StudentSurvey'},
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['abizeitung.StudentSurveyEntry']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'abizeitung.studentsurveyentry': {
            'Meta': {'object_name': 'StudentSurveyEntry'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choice'", 'to': u"orm['abizeitung.Student']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': u"orm['abizeitung.Student']"})
        },
        u'abizeitung.teacher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Teacher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'abizeitung.teachersurvey': {
            'Meta': {'ordering': "['title']", 'object_name': 'TeacherSurvey'},
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['abizeitung.TeacherSurveyEntry']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'abizeitung.teachersurveyentry': {
            'Meta': {'object_name': 'TeacherSurveyEntry'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['abizeitung.Teacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['abizeitung.Student']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['abizeitung']