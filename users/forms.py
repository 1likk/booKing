from django import forms 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User 
from django.core.exceptions import ValidationError

def validate_no_special_character(value):
    if any(char in "@#!$%" for char in value):
        raise ValidationError("Символы @, #, !, %, $ запрещены!")

class UserLoginForm(AuthenticationForm):
    username = forms.CharField
    password = forms.CharField

    class Meta:
        model = User 
        fields = ['username', 'password']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        validators=[validate_no_special_character]
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        validators=[validate_no_special_character]
    )
    username = forms.CharField(
        max_length=150,
        validators=[validate_no_special_character]
    )
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("Никнейм не может быть короче 3 символов")
        return username 
    
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2'
                  ]

class ProfileForm(UserChangeForm):
    image = forms.ImageField
    first_name = forms.CharField
    last_name = forms.CharField
    username = forms.CharField
    email = forms.EmailField
    
    class Meta:
        model = User
        fields = [
            'image',
            'first_name',
            'last_name',
            'username',
            'email'
        ]
        
        
        
        