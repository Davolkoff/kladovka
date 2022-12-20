from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Profile
from core.models import Container

User = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__input',
                                                                            'placeholder': " "}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__input',
                                                                                 'placeholder': " "}))


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={"class": "form__input", "placeholder": " "}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={"class": "form__input", "placeholder": " "}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form__input", "placeholder": " "}),
            'last_name': forms.TextInput(attrs={"class": "form__input", "placeholder": " "}),
            'email': forms.EmailInput(attrs={"class": "form__input", "placeholder": " "})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('patronymic', 'phone_number', 'birth_date')
        widgets = {
            'patronymic': forms.TextInput(attrs={"class": "form__input", "placeholder": " "}),
            'phone_number': forms.TextInput(attrs={"class": "form__input", "placeholder": " "}),
            'birth_date': forms.TextInput(attrs={"class": "form__input", "placegolder": " ", "type": "date"})
        }


class ReserveContainerForm(forms.Form):
    available_types = []
    available_containers = Container.objects.filter(owner=1)
    for container in available_containers:
        if container.dimensions == '10x10x2' and not '10x10x2' in available_types:
            available_types.append('10x10x2')
        elif container.dimensions == '5x3x2' and not '5x3x2' in available_types:
            available_types.append('5x3x2')
        elif container.dimensions == '2x2x2' and not '2x2x2' in available_types:
            available_types.append('2x2x2')

        if len(available_types) == 3:
            break

    variants = []
    types = {'2x2x2': 'Базовый (2x2x2) - 1300 руб/мес',
             '5x3x2': 'Средний (5x3x2) - 1500 руб/мес',
             '10x10x2': 'Большой (10x10x2) - 3000 руб/мес'}
    for t in available_types:
        variants.append([t, types[t]])

    def correct_period(self):
        cd = self.cleaned_data
        if cd["period"] < 1:
            raise forms.ValidationError("Введите корректное число месяцев")

    container_type = forms.ChoiceField(choices=variants, widget=forms.Select(attrs={"class": "form__input", "placeholder": " "}))
    period = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form__input", "placeholder": " "}))


class ReplenishBalance(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form__input", "placeholder": " "}))

    def min_amount(self):
        cd = self.cleaned_data
        if cd["amount"] < 300:
            raise forms.ValidationError("Минимальная сумма пополнения 300 рублей")