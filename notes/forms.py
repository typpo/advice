from django import forms
from django.contrib.flatpages.models import FlatPage
from django.forms.models import ModelForm
from tinymce.widgets import TinyMCE
from notes.models import Interview

class InterviewForm(ModelForm):
    company = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'size':50}))
    position = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'size':50}))
    date = forms.DateField(label='Date of interview')
    description = forms.CharField(max_length=2000, \
        widget=forms.widgets.Textarea(attrs={'rows':10,'cols':80}))

    question = forms.CharField(max_length=2000, \
        widget=forms.widgets.Textarea(attrs={'rows':10,'cols':80}))
    answer = forms.CharField(max_length=2000, \
        widget=forms.widgets.Textarea(attrs={'rows':10,'cols':80}))

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = FlatPage
        exclude = ('profile',)
        fields = ('company', 'position', 'date', 'description')
