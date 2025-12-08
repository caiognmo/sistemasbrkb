from django import forms
from django.contrib.auth.models import User
from .models import Feedback, Profile

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'reason', 'comment']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']