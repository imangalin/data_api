from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class AccountDataType(models.Model):
    title = models.CharField('Название', max_length=50)
    slug = models.SlugField('Слаг для поиска', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'


class DataRegion(models.Model):
    title = models.CharField('Название', max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class AccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user')

    def active(self):
        return self.get_queryset().filter(active=True)


class Account(models.Model):
    objects = AccountManager()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('ФИО', max_length=128)
    company = models.CharField('Компания', max_length=128)
    created = models.DateField('Создан', auto_now_add=True)
    active = models.BooleanField('Активен', default=False)
    access_start = models.DateField('Старт срока оплаты', blank=True, null=True)
    access_expiration = models.DateField('Срок оплаты истекает', blank=True, null=True)
    data_type = models.ManyToManyField('AccountDataType', verbose_name='Доступные типы данных', blank=True)
    region = models.ManyToManyField('DataRegion', verbose_name='Доступные регионы', blank=True)
    limit_data_size = models.PositiveIntegerField('Максимальное число отображаемых объектов', default=1000)

    request_total_count = models.PositiveIntegerField('Общее число запросов', default=0)
    request_day_count = models.PositiveIntegerField('Число запросов в сутки', default=0)
    request_month_count = models.PositiveIntegerField('Число запросов в месяц', default=0)
    request_total_limit = models.PositiveIntegerField('Общий лимит запросов', default=100000)
    request_day_limit = models.PositiveIntegerField('Лимит запросов в сутки', default=1000)
    request_month_limit = models.PositiveIntegerField('Лимит запросов в месяц', default=30000)

    token = models.CharField('Токен', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name

    def check_active(self):
        status = True if self.access_expiration > datetime.today() else False
        self.active = status
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_user_model()._default_manager.create_user(username=self.name)
            self.user = user
        super().save(*args, **kwargs)
