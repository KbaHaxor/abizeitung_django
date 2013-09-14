# -*- coding: utf-8 -*-

from abizeitung.models import Teacher, StudentSurvey, Student, TeacherSurvey
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
        fields = ["test"]
    
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        
        self.fields["test"].widget.attrs["class"] = "form-control"
        
        self.student_choices = [(-1, u"Bitte jemanden auswählen."), ("42", "Test")]
        for student in Student.objects.all():
            self.student_choices.append((student.id, student.fullname()))
        self.teacher_choices = [(-1, u"Bitte jemanden auswählen.")]
        for teacher in Teacher.objects.all():
            self.teacher_choices.append((teacher.id, teacher.fullname()))
       
        kwargs = lambda survey: {
            "label" : survey.question,
            "widget" : Select(attrs={"class" : "form-control"}),
        }

        self.student_surveys = []
        for survey in StudentSurvey.objects.all():
            field = ChoiceField(choices=self.student_choices, validators=[validate_student], **kwargs(survey))
            name = "student_survey_%s" % survey.id
            self.fields[name] = field
            self.student_surveys.append(self.fields[name])
        
        self.teacher_surveys = []
        for survey in TeacherSurvey.objects.all():
            field = ChoiceField(choices=self.teacher_choices, validators=[validate_teacher], **kwargs)
            name = "teacher_survey_%s" % survey.id
            self.fields[name] = field
            self.teacher_surveys.append(name)

    def clean(self):
        super(StudentEditForm, self).clean()

        print self.cleaned_data

        return self.cleaned_data

@login_required
def edit(request):
    context = {}
    form = StudentEditForm(request.POST or None, instance=Student.objects.get(user=request.user))
    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Konnte Daten nicht speichern!")
    context["form"] = form
    context["student"] = Student.objects.get(user=request.user)
    return render(request, "student/edit.html", context, context_instance=RequestContext(request))
