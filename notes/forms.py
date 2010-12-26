from django import forms
from django.contrib.flatpages.models import FlatPage
from django.forms.models import ModelForm
from notes.models import Interview

class InterviewForm(forms.Form):
    company = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'size':50}))
    position = forms.CharField(max_length=50, \
        widget=forms.TextInput(attrs={'size':50}))
    date = forms.DateField(label='Date of interview')
    description = forms.CharField(max_length=2000, \
        widget=forms.widgets.Textarea(attrs={'rows':6,'cols':80}))

    question = forms.CharField(max_length=2000, \
        widget=forms.widgets.Textarea(attrs={'rows':6,'cols':80}))
    answer = forms.CharField(max_length=2000, required=False, \
        widget=forms.widgets.Textarea(attrs={'rows':6,'cols':80}))

    def clean(self):
        for k in self.cleaned_data:
            if k.startswith('id_question'):
                # allow questions with no answers
                answer = k.replace('question', 'answer')
                if not answer in self.cleaned_data:
                    self.cleaned_data[answer] = ''
            elif k.startswith('id_answer'):
                # prevent answers with no questions
                question = k.replace('answer', 'question')
                if not question in self.cleaned_data or \
                    self.cleaned_data[question].strip() == '':
                    raise forms.ValidationError('Provided answer without a question')
        return self.cleaned_data

    class Meta:
        fields = ('company', 'position', 'date', 'description', 'question', 'answer')

class InterviewEditForm(ModelForm):
    class Meta:
        model = Interview
