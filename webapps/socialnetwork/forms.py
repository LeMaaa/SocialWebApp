from django import forms
from django.contrib.auth.models import User
from models import *  
from .models import Posts,Comment
from django.contrib.auth import authenticate
from django.core.validators import MinValueValidator,MaxValueValidator

MAX_UPLOAD_SIZE = 2500000
CONTENT_TYPES = ['image','jpeg','jpg','png']

class LoginForm(forms.Form):        
    username = forms.CharField()        
    password = forms.CharField(widget=forms.PasswordInput,required = True)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return cleaned_data

class RegistrationForm(forms.Form):
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    picture = models.FileField(upload_to="images/", blank=True)
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    username   = forms.CharField(max_length = 20)
    userage = forms.IntegerField()
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def  clean_userage(self):
        userage = self.cleaned_data.get('userage')
        if(userage < 0):
            raise forms.ValidationError("Invalid age, please input valid age")
        return userage




class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ( 'posts_content', 'posts_title' )

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username',)

class EditProForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','userage','bio')
        
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        try:
            if picture:
                content_type = picture.content_type.split('/')[0]
        except:
            pass
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

