# -*- coding: utf-8 -*-

from abizeitung.models import Teacher, StudentSurvey, Student, TeacherSurvey
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.fields import ChoiceField
from django.forms.models import ModelForm
from django.forms.widgets import Select
from django.shortcuts import render
from django.template.context import RequestContext

class StudentEditForm(ModelForm):
    class Meta:
        model = Student
        fields = ["test", ]
    
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        
        self.fields["test"].widget.attrs["class"] = "form-control"
        
        self.student_choices = [(-1, u"Bitte jemanden auswählen.")]
        for student in Student.objects.all():
            self.student_choices.append((student.id, student.fullname()))
        self.teacher_choices = [(-1, u"Bitte jemanden auswählen.")]
        for teacher in Teacher.objects.all():
            self.teacher_choices.append((teacher.id, teacher.fullname()))
        
        self.student_surveys = []
        for survey in StudentSurvey.objects.all():
            field = ChoiceField(label=survey.title, choices=self.student_choices, widget=Select(attrs={"class" : "form-control"}))
            name = "student_survey_%s" % survey.id
            self.fields[name] = field
            self.student_surveys.append(self.fields[name])
        
        self.teacher_surveys = []
        for survey in TeacherSurvey.objects.all():
            field = ChoiceField(label=survey.title, choices=self.teacher_choices, widget=Select(attrs={"class" : "form-control"}))
            name = "teacher_survey_%s" % survey.id
            self.fields[name] = field
            self.teacher_surveys.append(name)

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
    return render(request, "student/edit.html", context, context_instance=RequestContext(request))