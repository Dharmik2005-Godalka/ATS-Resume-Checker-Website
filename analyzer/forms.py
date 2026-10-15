from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AnalysisForm(forms.Form):
    job_title = forms.CharField(max_length=200)
    job_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))
    resume_file = forms.FileField(label='Resume (PDF)')

    def clean_resume_file(self):
        file = self.cleaned_data['resume_file']
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Please upload a PDF file.')
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File is too large (maximum 5 MB).')
        return file
    
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 8})}


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(label='Resume (PDF)')

    def clean_resume_file(self):
        file = self.cleaned_data['resume_file']
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Please upload a PDF file.')
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File is too large (maximum 5 MB).')
        return file
