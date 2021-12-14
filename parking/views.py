from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import ParkingReservation, ParkingSpace

from .forms import RegisterUserForm, LoginUserForm, ReservationForm, ReservationFormStart, NewParkingSpace, \
    ReservationFormForManager, EditReservationForm, EditReservationFormForManager

from .utils import date_intersection


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'parking/register.html'
    success_url = reverse_lazy('main')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'parking/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


def main(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "POST":
            form = ReservationFormStart(request.POST)
            if form.is_valid():
                day = form.cleaned_data['data']
                place_number = form.cleaned_data['parking_number']
                return redirect('parking_manager', day=day, place_number=place_number)

        else:
            form = ReservationFormStart
        return render(request, 'parking/main.html', context={'form': form})


def edit_space(request):
    if not request.user.is_authenticated and hasattr(request.user, "status"):
        return redirect('login')
    else:
        if request.method == "POST":
            form = NewParkingSpace(request.POST)
            if form.is_valid():
                space = form.save(commit=False)
                space.save()
                return redirect('edit_space')
        else:
            form = NewParkingSpace

        context = {
            'space': ParkingSpace.objects.all(),
            'form': form,
        }
        return render(request, 'parking/edit_space.html', context=context)


def parking_manager(request, day, place_number):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        parking_number = ParkingSpace.objects.get(number=place_number)
        info = ParkingReservation.objects.filter(data=day, parking_number=parking_number)
        data = {'user': request.user}
        if request.method == "POST":
            form = ReservationFormForManager(request.POST) if request.user.status else ReservationForm(request.POST)
            if form.is_valid():
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
                user = form.cleaned_data['user'] if request.user.status else request.user
                if start_time >= end_time:
                    messages.add_message(request, messages.INFO, 'Wrong time')
                elif date_intersection(start_time, end_time, info):
                    messages.add_message(request, messages.INFO, 'The selected time is already booked')
                else:
                    ParkingReservation.objects.create(parking_number=parking_number, data=day, start_time=start_time,
                                                      end_time=end_time, user=user)
                    messages.add_message(request, messages.SUCCESS, 'Entry added successfully')
                    return redirect('parking_lots')
        else:
            form = ReservationFormForManager(initial=data) if request.user.status else ReservationForm(initial=data)
        context = {
            'form': form,
            'info': info,
            'place_number': place_number,
            'day': day,
        }
        return render(request, 'parking/parking_manager.html', context=context)


def delete_space(request, place_number):
    if request.user.is_authenticated and hasattr(request.user, "status"):
        ParkingSpace.objects.filter(pk=place_number).delete()
        return redirect('edit_space')
    else:
        return redirect('login')


def delete_rezerv(request, place_number):
    rezerv_number = ParkingReservation.objects.get(pk=place_number)
    if request.user == rezerv_number.user or hasattr(request.user, "status"):
        rezerv_number.delete()
        return redirect('parking_lots')
    else:
        return redirect('login')


def parking_lots(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.status:
            reserves = ParkingReservation.objects.all()
        else:
            reserves = ParkingReservation.objects.filter(user=request.user)
        context = {
            'reserves': reserves
        }
        return render(request, 'parking/parking_lots.html', context=context)


def edit_parking_lots(request, rezerv):
    if not request.user.is_authenticated:
        redirect('login')
    else:
        rezerv_space = ParkingReservation.objects.get(pk=rezerv)
        data = {'parking_number': rezerv_space.parking_number, 'data': rezerv_space.data,
                'start_time': rezerv_space.start_time, 'end_time': rezerv_space.end_time}
        if request.method == "POST":
            form = EditReservationFormForManager(request.POST) if request.user.status else EditReservationForm(
                request.POST)
            if form.is_valid():
                rezerv_space.parking_number = form.cleaned_data['parking_number']
                rezerv_space.data = form.cleaned_data['data']
                rezerv_space.start_time = form.cleaned_data['start_time']
                rezerv_space.end_time = form.cleaned_data['end_time']
                info = ParkingReservation.objects.filter(data=rezerv_space.data,
                                                         parking_number=rezerv_space.parking_number)
                if request.user.status:
                    rezerv_space.user = form.cleaned_data['user']
                else:
                    rezerv_space.user = request.user
                if rezerv_space.start_time >= rezerv_space.end_time:
                    messages.add_message(request, messages.INFO, 'Wrong time')
                elif date_intersection(rezerv_space.start_time, rezerv_space.end_time, info, rezerv_space):
                    messages.add_message(request, messages.INFO, 'The selected time is already booked')
                else:
                    rezerv_space.save()
                    messages.add_message(request, messages.SUCCESS, 'Record updated successfully')
                    return redirect('parking_lots')
        else:
            form = EditReservationFormForManager(initial=data) if request.user.status else EditReservationForm(
                initial=data)
        context = {
            'form': form,
            'rezerv_space': rezerv_space,
            'info_user': rezerv_space.user,
        }
        return render(request, 'parking/edit_parking_lots.html', context=context)
