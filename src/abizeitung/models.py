# -*- coding: iso-8859-15 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

import hashlib

class Student(models.Model):
    class Meta:
        verbose_name = u"Sch�ler"
        verbose_name_plural = u"Sch�ler"
    
    user = models.OneToOneField(User, verbose_name="Benutzer")
    test = models.CharField(default="", blank=True, max_length=255, verbose_name="Test")
    
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name
    fullname.short_description = "Name"
    
    def get_password(self):
        plain  = "%s.%s" % (self.user.first_name.lower(), self.user.last_name.lower())
        plain += "Sonne2013" 
        return hashlib.md5(plain).hexdigest()[:8]
    
    def __unicode__(self):
        return u"Sch�ler %s - %s" % (self.user, self.get_password())

class Teacher(models.Model):
    class Meta:
        verbose_name = "Lehrer"
        verbose_name_plural = "Lehrer"
    
    title = models.CharField(max_length=100, verbose_name="Anrede")
    name = models.CharField(max_length=100, verbose_name="Name")
    
    def fullname(self):
        return self.title + " " + self.name
    fullname.short_description = "Name"
    
    def __unicode__(self):
        return u"Lehrer %s %s" % (self.title, self.name)

class StudentSurvey(models.Model):
    class Meta:
        verbose_name = u"Sch�lerumfrage"
        verbose_name_plural = u"Sch�lerumfragen"
    
    title = models.CharField(max_length=255, verbose_name="Titel")

class TeacherSurvey(models.Model):
    class Meta:
        verbose_name = u"Lehrerumfrage"
        verbose_name_plural = u"Lehrerumfragen"
    
    title = models.CharField(max_length=255, verbose_name="Titel")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.get_or_create(user=instance)
signals.post_save.connect(create_user_profile, sender=User)