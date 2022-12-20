from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class Container(models.Model):
    price = models.IntegerField('Стоимость контейнера')
    dimensions = models.CharField('Габариты контейнера', max_length=8)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1)
    rent_deadline = models.DateField('Дата окончания аренды')  # рассчитывается из баланса клиента
    loaded = models.BooleanField(default=False)  # привез ли клиент свои вещи

    class Meta:
        verbose_name = 'Карточка контейнера'
        verbose_name_plural = 'Контейнеры'

    def __str__(self):
        s = ""
        if self.owner.username == 'davolkoff':
            s += "- "
        else:
            s += "+ "
        s += f'{self.dimensions} {self.owner}'
        return s


class ManagerCallRequest(models.Model):
    full_name = models.CharField('ФИО', max_length=60)
    phone_number = models.CharField('Номер телефона', max_length=20)
    time_created = models.DateTimeField('Время поступления заявки', auto_now_add=True, auto_now=False)
    time_called = models.DateTimeField('Время ответа на заявку', auto_now_add=False, auto_now=True)
    status = models.BooleanField('Выполнен', default=False)

    class Meta:
        verbose_name = 'Запрос на обратный звонок'
        verbose_name_plural = 'Запросы на обратный звонок'

    def __str__(self):
        return f'{self.full_name} | {self.phone_number}'