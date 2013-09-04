from abizeitung.models import Teacher, StudentSurvey, Student, TeacherSurvey
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.fields import ChoiceField
from django.forms.forms import Form
from django.shortcuts import render
from django.template.context import RequestContext

class StudentEditForm(Form):
    
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        
        self.student_choices = []
        for student in Student.objects.all():
            self.student_choices.append((student.id, student.fullname()))
        self.teacher_choices = []
        for teacher in Teacher.objects.all():
            self.teacher_choices.append((teacher.id, teacher.fullname()))
        
        self.student_surveys = []
        for survey in StudentSurvey.objects.all():
            field = ChoiceField(label=survey.title, choices=self.student_choices)
            name = "student_survey_%s" % survey.id
            self.fields[name] = field
            self.student_surveys.append(self.fields[name])
        
        self.teacher_surveys = []
        for survey in TeacherSurvey.objects.all():
            field = ChoiceField(label=survey.title, choices=self.teacher_choices)
            name = "teacher_survey_%s" % survey.id
            self.teacher_surveys.append(name)
            self.fields[name] = field

@login_required
def edit(request):
    context = {}
    context["form"] = StudentEditForm()
    context["students"] = User.objects.all()
    context["teachers"] = Teacher.objects.all()
    return render(request, "student/edit.html", context, context_instance=RequestContext(request))