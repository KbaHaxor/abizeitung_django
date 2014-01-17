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
        filename = path + "/" + hashlib.md5(filename).hexdigest()[:12] + ".jpg"
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
    
    user = models.ForeignKey(User, verbose_name="Benutzer")
    tutor = models.ForeignKey(Teacher, null=True, verbose_name="Tutorengruppe")
    
    lebensmotto = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist dein Lebensmotto?")
    woerter_phrasen = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Welche Wörter/Phrasen benutzt du oft?")
    lieblingszitat = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist dein Lieblingszitat?")
    biographie = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Wie wäre der Titel deiner Biographie?")
    hobbies = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was sind deine Hobbies?")
    lieblingsserie = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist deine Lieblingsserie?")
    lieblingsmusik = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist deine Lieblingsmusik?")
    beschaeftigung_unterricht = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist deine Lieblingsbeschäftigung im Unterricht?")
    wen_vermissen = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was wirst du am meisten vermissen?")
    ohne_wen_abi_nicht = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Ohne ... hätte ich mein Abi nicht geschafft.")
    unvergessliche_momente = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was waren unvergessliche Momente in deiner Schulzeit?")
    lieblingsprodukt_sky = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ist dein Lieblingsprodukt im Sky?")
    schlusswort = models.CharField(default="", blank=True, max_length=255,
        verbose_name="Was ich noch sagen wollte...")
    
    picture = models.ImageField(upload_to=image_filename("student_pictures"), 
                                default="", blank=True, verbose_name="Normales Foto")
    school_picture = models.ImageField(upload_to=image_filename("school_pictures"), 
                                default="", blank=True, verbose_name="Einschulungsfoto")
    
    def fullname(self):
        return self.user.first_name + " " + self.user.last_name
    fullname.short_description = "Name"
    
    def get_profile_fields(self):
        fields = [
            "lebensmotto",
            "woerter_phrasen",
            "lieblingszitat",
            "biographie",
            "hobbies",
            "lieblingsserie",
            "lieblingsmusik",
            "beschaeftigung_unterricht",
            "wen_vermissen",
            "ohne_wen_abi_nicht",
            "unvergessliche_momente",
            "lieblingsprodukt_sky",
            "schlusswort",
        ]
        
        values = {}
        for field in fields:
            values[field] = getattr(self, field)
        return values
    
    def __unicode__(self):
        return self.fullname()

class StudentSurvey(models.Model):
    class Meta:
        verbose_name = u"Schülerumfrage"
        verbose_name_plural = u"Schülerumfragen"
        
        ordering = ["question"]
    
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
        
        ordering = ["question"]
    
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
