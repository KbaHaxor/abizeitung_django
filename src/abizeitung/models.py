# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.conf import settings
import hashlib
import os

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
        return self.fullname()

def image_filename(path):
    def inner(instance, filename):
        filename = "%s_%s_Sonne2013" % (instance.user.first_name.lower(), instance.user.last_name.lower())
        filename = path + "/" + hashlib.md5(filename).hexdigest()[:6] + ".jpg"
        fullname = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(fullname):
            os.remove(fullname)
        return filename
    return inner

class Student(models.Model):
    class Meta:
        verbose_name = u"Schüler"
        verbose_name_plural = u"Schüler"
        
        ordering = ["user__first_name", "user__last_name"]
    
    user = models.OneToOneField(User, verbose_name="Benutzer")
    tutor = models.ForeignKey(Teacher, null=True, verbose_name="Tutorengruppe")
    test = models.CharField(default="", blank=True, max_length=255, verbose_name="Test")
    picture = models.ImageField(upload_to=image_filename("student_pictures"), 
                                default="", blank=True, verbose_name="Normales Foto")
    baby_picture = models.ImageField(upload_to=image_filename("baby_pictures"), 
                                default="", blank=True, verbose_name="Babyfoto")
    
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name
    fullname.short_description = "Name"
    
    def __unicode__(self):
        return self.fullname()

class StudentSurvey(models.Model):
    class Meta:
        verbose_name = u"Schülerumfrage"
        verbose_name_plural = u"Schülerumfragen"
        
        ordering = ["title"]
    
    question = models.CharField(max_length=255, verbose_name="Frage")
    title = models.CharField(max_length=255, verbose_name="Titel")
    
    def __unicode__(self):
        return self.title

class StudentSurveyEntry(models.Model):
    class Meta:
        verbose_name = u"Schülerumfrage Eintrag"
        verbose_name_plural = u"Schülerumfragen Einträge"
        
    survey = models.ForeignKey(StudentSurvey, null=True, verbose_name="Schülerumfrage")
    student = models.ForeignKey(Student, related_name="student", verbose_name="Schüler")
    choice = models.ForeignKey(Student, related_name="choice", verbose_name="Auswahl")

class TeacherSurvey(models.Model):
    class Meta:
        verbose_name = u"Lehrerumfrage"
        verbose_name_plural = u"Lehrerumfragen"
        
        ordering = ["title"]
    
    question = models.CharField(max_length=255, verbose_name="Frage")
    title = models.CharField(max_length=255, verbose_name="Titel")
    
    def __unicode__(self):
        return self.title

class TeacherSurveyEntry(models.Model):
    class Meta:
        verbose_name = u"Lehrerumfrage Eintrag"
        verbose_name_plural = u"Lehrerumfragen Einträge"
    
    survey = models.ForeignKey(TeacherSurvey, null=True, verbose_name="Lehrerumfrage")
    student = models.ForeignKey(Student, verbose_name="Schüler")
    choice = models.ForeignKey(Teacher, verbose_name="Auswahl")

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.get_or_create(user=instance)
signals.post_save.connect(create_user_profile, sender=User)
