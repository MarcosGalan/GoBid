from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.core.validators import EmailValidator, MinValueValidator, RegexValidator, MaxValueValidator

from django import forms
from django.core.validators import EmailValidator, MinValueValidator, RegexValidator
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta

from access.fields import DNIField
from core.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    age = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[MaxValueValidator(limit_value=date.today() - timedelta(days=365 * 18),
                                      message='You must be at least 18 years old to register.')],
        initial=date.today() - timedelta(days=365 * 18)
    )
    dni = DNIField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'dni', 'age')

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        dni = cleaned_data.get('dni')

        if age is not None and dni:
            birth_year = date.today().year - age.year
            if birth_year < 18:
                self.add_error('age', 'You must be at least 18 years old to register.')

        return cleaned_data

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            dni = dni[:-1]
        return dni

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid  # If the basic validation fails, no need to proceed with custom validation

        return valid

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.age = self.cleaned_data['age']
        user.dni = self.cleaned_data['dni']

        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'photo')

    def clean_photo(self):
        return self.cleaned_data['photo']

    def clean_age(self):
        return self.cleaned_data['age']

    def clean_dni(self):
        return self.cleaned_data.get('dni')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.photo = self.cleaned_data['photo']
        if commit:
            user.save()
        return user


class ChangePasswordForm(PasswordChangeForm):
    pass
