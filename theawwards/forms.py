from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Profile, Project, Rating

INT_CHOICES= [tuple([x,x]) for x in range(1,10)]


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt srch_explore'}), max_length=50, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = ['user']
		widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'location': forms.Textarea(attrs={'class':'form-control'}),
        }

class NewProjectForm(forms.ModelForm):

    project_image = forms.ImageField(required=True)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Title'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Description'}), required=True)
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Link'}), required=True)


    class Meta:
        model = Project
        fields = ['title', 'project_image','description', 'link']

class RatingForm(forms.ModelForm):

     class Meta:
        model = Rating
        design= forms.IntegerField(label="Design Rates")
        usability = forms.IntegerField(label="Usability Rates")
        content = forms.IntegerField(label="Content Rates")
        
                
        widget=forms.Select(choices=INT_CHOICES)
        exclude =['project','user']
   
