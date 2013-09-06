# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
import hashlib

class Teacher(models.Model):
    class Meta:
        verbose_name = "Lehrer"
        verbose_name_plural = "Lehrer"
        
        ordering = ["name"]
    
    title = models.CharField(max_length=100, verbose_name="Anrede")
    name = models.CharField(max_length=100, verbose_name="Name")
    
    def fullname(self):
        return self.title + " " + self.name
    fullname.short_description = "Name"
    
    def __unicode__(self):
        return u"%s %s" % (self.title, self.name)

class Student(models.Model):
    class Meta:
        verbose_name = u"Schüler"
        verbose_name_plural = u"Schüler"
        
        ordering = ["user__first_name", "user__last_name"]
    
    user = models.OneToOneField(User, verbose_name="Benutzer")
    tutor = models.ForeignKey(Teacher, null=True, verbose_name="Tutorengruppe")
    test = models.CharField(default="", blank=True, max_length=255, verbose_name="Test")
    
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name
    fullname.short_description = "Name"
    
    def get_password(self):
        plain  = "%s.%s" % (self.user.first_name.lower(), self.user.last_name.lower())
        plain += getattr(settings, "USER_PASSWORD_SECRET")
        return hashlib.md5(plain).hexdigest()[:8]
    
    def __unicode__(self):
        return u"%s - %s" % (self.user, self.get_password())

class StudentSurvey(models.Model):
    class Meta:
        verbose_name = u"Schülerumfrage"
        verbose_name_plural = u"Schülerumfragen"
        
        ordering = ["title"]
    
    title = models.CharField(max_length=255, verbose_name="Titel")

class TeacherSurvey(models.Model):
    class Meta:
        verbose_name = u"Lehrerumfrage"
        verbose_name_plural = u"Lehrerumfragen"
        
        ordering = ["title"]
    
    title = models.CharField(max_length=255, verbose_name="Titel")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.get_or_create(user=instance)
signals.post_save.connect(create_user_profile, sender=User)