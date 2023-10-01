from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .models import *

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_registered = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'email', 'password', 'shift', 'department', 'is_superuser', 'is_staff', 'is_registered')

    password = forms.CharField(widget=forms.PasswordInput)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.password = make_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.fullname = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
