# -*- coding: utf-8 -*-

from abizeitung.models import Teacher, StudentSurvey, Student, TeacherSurvey,\
    StudentSurveyEntry, TeacherSurveyEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import Select, ValidationError
from django.forms.fields import ChoiceField, CharField
from django.forms.models import ModelForm
from django.shortcuts import render
from django.template.context import RequestContext, Context
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.forms import Form
from django.utils.safestring import mark_safe
from django.db.models.fields import TextField
from django.forms.widgets import Textarea
from django.template.base import Template

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
            "widget" : Select(attrs={"class" : "selectpicker",})
                                     #"data-live-search" : "true",
                                     #"data-size" : "10"}),
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

@login_required
@staff_member_required
def evaluation(request):
    progress = {}
    
    all_profiles, value_profiles, percentage_profiles = 0, 0, 0
    students = Student.objects.all()
    for student in students:
        for field, value in student.get_profile_fields():
            all_profiles += 1
            if value:
                value_profiles += 1
    percentage_profiles = round(float(value_profiles) / all_profiles * 100, 2)
    
    progress["all_profiles"] = all_profiles
    progress["value_profiles"] = value_profiles
    progress["percentage_profiles"] = percentage_profiles
    
    progress["all_student_surveys"] = StudentSurvey.objects.count() * students.count()
    progress["value_student_surveys"] = StudentSurveyEntry.objects.count()
    progress["percentage_student_surveys"] = round(float(progress["value_student_surveys"]) / progress["all_student_surveys"] * 100, 2)
    
    progress["all_teacher_surveys"] = TeacherSurvey.objects.count() * students.count()
    progress["value_teacher_surveys"] = TeacherSurveyEntry.objects.count()
    progress["percentage_teacher_surveys"] = round(float(progress["value_teacher_surveys"]) / progress["all_teacher_surveys"] * 100, 2)
    
    student_surveys = []
    for survey in StudentSurvey.objects.all():
        survey_obj = {"question" : survey.question}
        students_obj = []
        
        for student in students:
            students_obj.append({
                "name" : student.fullname(),
                "votes" : StudentSurveyEntry.objects.all().filter(survey=survey, choice=student).count(),
            })
        
        students_obj.sort(key=lambda student: student["votes"], reverse=True)
        students_obj = filter(lambda student: student["votes"] != 0, students_obj)
        survey_obj["students"] = students_obj[:5]
        student_surveys.append(survey_obj)
    
    teacher_surveys = []
    teachers = Teacher.objects.all()
    for survey in TeacherSurvey.objects.all():
        survey_obj = {"question" : survey.question}
        teachers_obj = []
        
        for teacher in teachers:
            teachers_obj.append({
                "name" : teacher.fullname(),
                "votes" : TeacherSurveyEntry.objects.all().filter(survey=survey, choice=teacher).count(),
            })
        
        teachers_obj.sort(key=lambda teacher: teacher["votes"], reverse=True)
        teachers_obj = filter(lambda teacher: teacher["votes"] != 0, teachers_obj)
        survey_obj["teachers"] = teachers_obj[:5]
        teacher_surveys.append(survey_obj)
    
    context = {}
    context["progress"] = progress
    context["student_surveys"] = student_surveys
    context["teacher_surveys"] = teacher_surveys
    return render(request, "student/evaluation.html", context, context_instance=RequestContext(request))

class ExportTemplateForm(Form):
    template = CharField(required=False, widget=Textarea(attrs={"class" : "form-control",}))

DEFAULT_TEMPLATE = """
<ul>
{% for student in students %}

<li>
  <b>Name:</b> {{ student.name }}
  <ul>
  {% for key, value in student.profile %}
    <li><b>{{ key }}:</b> {{ value }}</li>
  {% endfor %}
  </ul>
</li>

{% endfor %}
</ul>

<!--<pre>{{ students }}</pre>-->
"""

@login_required
@staff_member_required
def export(request):
    context = {}
    
    template = DEFAULT_TEMPLATE
    
    form = ExportTemplateForm(initial=dict(template=DEFAULT_TEMPLATE))
    if request.POST:
        form = ExportTemplateForm(request.POST)
        if form.is_valid():
            template = form.cleaned_data["template"]
    
    students = []
    for student in Student.objects.all().order_by("user__username"):
        current = dict(name=student.fullname())
        current["profile"] = student.get_profile_fields()
        
        students.append(current)
    
    export = mark_safe(Template(template).render(Context(dict(students=students))))
    
    context["form"] = form
    context["export"] = export
    return render(request, "student/export.html", context, context_instance=RequestContext(request))
