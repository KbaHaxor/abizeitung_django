# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals

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
    survey = models.ForeignKey(StudentSurvey, null=True)
    student = models.ForeignKey(Student, related_name="student")
    choice = models.ForeignKey(Student, related_name="choice")

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
    survey = models.ForeignKey(TeacherSurvey, null=True)
    student = models.ForeignKey(Student)
    choice = models.ForeignKey(Teacher)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.get_or_create(user=instance)
signals.post_save.connect(create_user_profile, sender=User)
