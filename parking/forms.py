from datetime import date
from django.core.validators import MinValueValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

from .widget import DatePickerInput, TimePickerInput

DEFAULT_STYLE= {'attrs': {'class': 'form-control w-50'}}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(**DEFAULT_STYLE))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(**DEFAULT_STYLE))
    password2 = forms.CharField(label='Password Repeat',
                                widget=forms.PasswordInput(attrs={'class': 'form-control w-50'}))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(**DEFAULT_STYLE))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(**DEFAULT_STYLE))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(**DEFAULT_STYLE))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(**DEFAULT_STYLE))


class NewParkingSpace(forms.ModelForm):
    number = forms.CharField(label='', widget=forms.TextInput(**DEFAULT_STYLE))

    class Meta:
        model = ParkingSpace
        fields = ('number',)


class ReservationForm(forms.ModelForm):
    start_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))
    end_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))

    class Meta:
        model = ParkingReservation
        fields = ('start_time', 'end_time')


class ReservationFormForManager(ReservationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(status=False, is_staff=False)

    class Meta:
        model = ParkingReservation
        fields = ('start_time', 'end_time', 'user')


class ReservationFormStart(forms.ModelForm):
    data = forms.DateField(label='Select a day', widget=DatePickerInput(**DEFAULT_STYLE),
                           validators=[MinValueValidator(limit_value=date.today)])

    class Meta:
        model = ParkingReservation
        fields = ('parking_number', 'data')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class EditReservationFormForManager(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(status=False, is_staff=False)

    data = forms.DateField(widget=DatePickerInput(**DEFAULT_STYLE),
                           validators=[MinValueValidator(limit_value=date.today)])
    start_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))
    end_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))

    class Meta:
        model = ParkingReservation
        fields = ('parking_number', 'data', 'start_time', 'end_time', 'user')


class EditReservationForm(forms.ModelForm):
    data = forms.DateField(widget=DatePickerInput(**DEFAULT_STYLE))
    start_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))
    end_time = forms.TimeField(widget=TimePickerInput(**DEFAULT_STYLE))

    class Meta:
        model = ParkingReservation
        fields = ('parking_number', 'data', 'start_time', 'end_time')
