from django.contrib import admin
from django.urls import path
from accounts.forms import LoginUserForm
from accounts.views import LoginUser, logout_user, register_user, container_list, cancel_reservation, \
    reserve_container_form, replenish_balance

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', register_user, name='registration'),
    path('containers/', container_list,  name='user_containers'),
    path('containers/cancel/<int:container_id>/', cancel_reservation, name='rent_cancel'),
    path('reservation/', reserve_container_form, name='reservation'),
    path('replenish/', replenish_balance, name='replenish')
]
