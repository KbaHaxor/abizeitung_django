# -*- coding: utf-8 -*-

from abizeitung.models import Teacher, StudentSurvey, Student, TeacherSurvey,\
    StudentSurveyEntry, TeacherSurveyEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import Select, ValidationError
from django.forms.fields import ChoiceField
from django.forms.models import ModelForm
from django.shortcuts import render
from django.template.context import RequestContext

def validate_student(value):
    if value == "-1":
        return
    if not Student.objects.filter(id=value).exists():
        raise ValidationError(u"Ungültige Auswahl!")

def validate_teacher(value):
    if value == "-1":
        return
    if not Teacher.objects.filter(id=value).exists():
        raise ValidationError(u"Ungültige Auswahl")

class StudentEditForm(ModelForm):
    class Meta:
        model = Student
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
            "picture", "school_picture"
        ]
    
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        
        self.instance = kwargs["instance"]
        
        for field in StudentEditForm.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        
        self.student_choices = [(-1, u"Bitte jemanden auswählen.")]
        for student in Student.objects.all():
            self.student_choices.append((student.pk, student.fullname()))
        self.teacher_choices = [(-1, u"Bitte jemanden auswählen.")]
        for teacher in Teacher.objects.all():
            self.teacher_choices.append((teacher.pk, teacher.fullname()))
       
        kwargs = lambda survey: {
            "label" : survey.question,
            "widget" : Select(attrs={"class" : "selectpicker",
                                     "data-live-search" : "true",
                                     "data-size" : "10"}),
        }

        self.student_surveys = {}
        for survey in StudentSurvey.objects.all():
            initial = -1
            entries = StudentSurveyEntry.objects.filter(student=self.instance, survey=survey)
            if entries.exists():
                initial = entries[0].choice.pk
            
            field = ChoiceField(choices=self.student_choices, initial=initial, validators=[validate_student], **kwargs(survey))
            name = "student_survey_%s" % survey.id
            self.fields[name] = field
            self.student_surveys[survey] = name
        
        self.teacher_surveys = {}
        for survey in TeacherSurvey.objects.all():
            initial = -1
            entries = TeacherSurveyEntry.objects.filter(student=self.instance, survey=survey)
            if entries.exists():
                initial = entries[0].choice.pk
            
            field = ChoiceField(choices=self.teacher_choices, initial=initial, validators=[validate_teacher], **kwargs(survey))
            name = "teacher_survey_%s" % survey.id
            self.fields[name] = field
            self.teacher_surveys[survey] = name

    def clean(self):
        super(StudentEditForm, self).clean()

        self.survey2student = {}
        for survey, name in self.student_surveys.items():
            pk = self.cleaned_data.get(name, "-1")
            if pk != "-1":
                self.survey2student[survey] = Student.objects.get(pk=self.cleaned_data[name])
        
        self.survey2teacher = {}
        for survey, name in self.teacher_surveys.items():
            pk = self.cleaned_data.get(name, "-1")
            if pk != "-1":
                self.survey2teacher[survey] = Teacher.objects.get(pk=self.cleaned_data[name])

        return self.cleaned_data

    def save_surveys(self):
        used = set()
        for entry in StudentSurveyEntry.objects.filter(student=self.instance):
            if entry.survey in self.survey2student:
                entry.choice = self.survey2student[entry.survey]
                entry.save()
            else:
                entry.delete()
            used.add(entry.survey)
        for survey, choice in self.survey2student.items():
            if not survey in used:
                entry = StudentSurveyEntry()
                entry.survey = survey
                entry.student = self.instance
                entry.choice = choice
                entry.save()
        
        used = set()
        for entry in TeacherSurveyEntry.objects.filter(student=self.instance):
            if entry.survey in self.survey2teacher:
                entry.choice = self.survey2teacher[entry.survey]
                entry.save()
            else:
                entry.delete()
            used.add(entry.survey)
        for survey, choice in self.survey2teacher.items():
            if not survey in used:
                entry = TeacherSurveyEntry()
                entry.survey = survey
                entry.student = self.instance
                entry.choice = choice
                entry.save()
                
@login_required
def edit(request):
    messages.info(request, "Bitte unten speichern nicht vergessen! Bei Fragen oder Problemen bitte per E-Mail an abiumfrage-support@mapcrafter.org wenden.")
    
    context = {}
    form = StudentEditForm(request.POST or None, files=request.FILES or None,
                           instance=Student.objects.get(user=request.user))
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form.save_surveys()
        else:
            messages.error(request, "Konnte Daten nicht speichern!")
    context["form"] = form
    context["student"] = Student.objects.get(user=request.user)
    return render(request, "student/edit.html", context, context_instance=RequestContext(request))
