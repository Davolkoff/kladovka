import decimal
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView

from accounts.forms import LoginUserForm, ProfileForm, UserForm, ReserveContainerForm, ReplenishBalance
from accounts.models import Profile
from core.models import Container


def logout_user(request):
    logout(request)
    return redirect('main')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'


def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            cd = user_form.cleaned_data
            form_info = profile_form.cleaned_data

            new_user = User.objects.create_user(cd["email"],
                                                cd["email"],
                                                cd['password'])
            new_user.first_name = cd["first_name"]
            new_user.last_name = cd["last_name"]
            new_user.save()

            new_user.profile.patronymic = form_info["patronymic"]
            new_user.profile.phone_number = form_info["phone_number"]
            new_user.profile.birth_date = form_info["birth_date"]
            new_user.save()

            login(request, new_user)
            return(redirect('main'))

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    context = {'form1': user_form, 'form2': profile_form}
    return render(request, 'registration/register.html', context)


class UserContainers(ListView):
    model = Container
    template_name = 'profile/containers.html'
    context_object_name = 'containers_list'


# все контейнеры пользователя
def container_list(request):
    containers = Container.objects.filter(owner=request.user.id)
    if not request.user.is_authenticated:
        return (redirect('login'))
    if len(containers) > 0:
        full_price = 0
        small = []
        middle = []
        large = []
        for container in containers:
            full_price += container.price
        for container in containers:
            if container.dimensions == '10x10x2':
                large.append(container)
            elif container.dimensions == '5x3x2':
                middle.append(container)
            else:
                small.append(container)
        context = {'small_containers': small,
                   'middle_containers': middle,
                   'large_containers': large,
                   'full_price': full_price}
    else:
        context = {'error': "У вас еще нет арендованных контейнеров"}
    return render(request, 'profile/containers.html', context)


# форма регистрации контейнера
def reserve_container_form(request):
    form = ReserveContainerForm()
    if request.method == 'POST':
        form = ReserveContainerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            period = data.get('period')
            container = Container.objects.filter(dimensions=data.get('container_type'), owner=1)[0]
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            if profile.balance >= container.price * period:
                container.owner = User.objects.get(id=request.user.id)
                profile.balance -= container.price * period
                container.rent_deadline = (datetime.now() + relativedelta(months=period)).date()
                container.loaded = False
                container.save()
                profile.save()
            return redirect('user_containers')
    return render(request, 'profile/available_containers.html', {'form': form})


# отмена резервации контейнера
def cancel_reservation(request, container_id):
    container = Container.objects.get(id=container_id)
    user = User.objects.get(id=request.user.id)

    if container.owner.id == request.user.id and not container.loaded:

        last_money = decimal.Decimal(container.price*((container.rent_deadline - datetime.now().date()).days/31))

        container.owner = User.objects.get(id=1)
        user.profile.balance += last_money
        container.save()
        user.save()

    return redirect('user_containers')


# пополнение баланса
def replenish_balance(request):
    form = ReplenishBalance()
    if request.method == 'POST':
        form = ReplenishBalance(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(id=request.user.id)
            user.profile.balance += cd["amount"]
            user.save()
            return redirect('user_containers')
        else:
            form = ReplenishBalance()
    return render(request, 'profile/replenish_balance.html', {'form': form})
