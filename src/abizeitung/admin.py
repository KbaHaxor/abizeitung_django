from django.contrib import admin
from abizeitung.models import Student, Teacher, StudentSurvey, TeacherSurvey,\
    StudentSurveyEntry, TeacherSurveyEntry

class StudentAdmin(admin.ModelAdmin):
    list_display = ("fullname", "tutor", "test", "picture", "school_picture")

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("fullname",)

class StudentSurveyAdmin(admin.ModelAdmin):
    list_display = ("question", "title",)

class StudentSurveyEntryAdmin(admin.ModelAdmin):
    list_display = ("survey", "student", "choice", )

class TeacherSurveyAdmin(admin.ModelAdmin):
    list_display = ("question", "title",)

class TeacherSurveyEntryAdmin(admin.ModelAdmin):
    list_display = ("survey", "student", "choice", )

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StudentSurvey, StudentSurveyAdmin)
admin.site.register(StudentSurveyEntry, StudentSurveyEntryAdmin)
admin.site.register(TeacherSurvey, TeacherSurveyAdmin)
admin.site.register(TeacherSurveyEntry, TeacherSurveyEntryAdmin)