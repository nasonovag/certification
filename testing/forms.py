from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия", required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Фамилия'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'profile_picture', 'is_active']

from django import forms
from .models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description']
        labels = {
            'title': 'Название теста',
            'description': 'Описание теста',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название теста'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Краткое описание содержания теста'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("Название должно быть не короче 3 символов.")
        return title