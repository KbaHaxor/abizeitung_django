from django.contrib import admin
from abizeitung.models import Student, Teacher, StudentSurvey, TeacherSurvey

class StudentAdmin(admin.ModelAdmin):
    list_display = ("fullname", "tutor",)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("fullname",)

class StudentSurveyAdmin(admin.ModelAdmin):
    list_display = ("question", "title",)

class TeacherSurveyAdmin(admin.ModelAdmin):
    list_display = ("question", "title",)

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StudentSurvey, StudentSurveyAdmin)
admin.site.register(TeacherSurvey, TeacherSurveyAdmin)