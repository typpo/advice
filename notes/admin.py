from django.contrib import admin
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview
from notes.models import Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class InterviewAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ['name']

admin.site.register(Interview, InterviewAdmin)
admin.site.register(Company)
admin.site.register(Position)
admin.site.register(Profile)
