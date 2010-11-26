from django import forms
from django.forms.models import ModelForm
from notes.models import Interview

class InterviewForm(ModelForm):
    company = forms.CharField(max_length=50)
    position = forms.CharField(max_length=50)
    date = forms.DateField()
    description = forms.CharField(max_length=2000, label='', \
        widget=forms.Textarea(attrs={'rows':20,'cols':80}))

    class Meta:
        model = Interview
        exclude = ('profile',)
        fields = ('company', 'position', 'date', 'description')
