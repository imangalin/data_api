from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token


class AccountDataType(models.Model):
    title = models.CharField("Название", max_length=50)
    slug = models.SlugField("Слаг для поиска", null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип данных"
        verbose_name_plural = "Типы данных"


class DataRegion(models.Model):
    title = models.CharField("Название", max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class AccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def active(self):
        return self.get_queryset().filter(active=True)


class Account(models.Model):
    objects = AccountManager()
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField("ФИО", max_length=128)
    company = models.CharField("Компания", max_length=128)
    created = models.DateField("Создан", auto_now_add=True)
    active = models.BooleanField("Активен", default=False)
    access_start = models.DateField("Старт срока оплаты", blank=True, null=True)
    access_expiration = models.DateField("Срок оплаты истекает", blank=True, null=True)
    data_type = models.ManyToManyField(
        "AccountDataType", verbose_name="Доступные типы данных", blank=True
    )
    region = models.ManyToManyField(
        "DataRegion", verbose_name="Доступные регионы", blank=True
    )
    limit_data_size = models.PositiveIntegerField(
        "Максимальное число отображаемых объектов", default=1000
    )

    request_total_count = models.PositiveIntegerField("Общее число запросов", default=0)
    request_day_count = models.PositiveIntegerField("Число запросов в сутки", default=0)
    request_month_count = models.PositiveIntegerField(
        "Число запросов в месяц", default=0
    )
    request_total_limit = models.PositiveIntegerField(
        "Общий лимит запросов", default=100000
    )
    request_day_limit = models.PositiveIntegerField(
        "Лимит запросов в сутки", default=1000
    )
    request_month_limit = models.PositiveIntegerField(
        "Лимит запросов в месяц", default=30000
    )

    token = models.CharField("Токен", max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name

    def check_active(self):
        status = True if self.access_expiration >= date.today() else False
        self.active = status
        self.save()

    def create_token(self):
        if not self.token:
            token = Token.objects.create(user=self.user)
            self.token = token.key
            self.save()

    def clear_day_count(self):
        self.request_day_count = 0
        self.save()

    def clear_month_count(self):
        self.request_month_count = 0
        self.save()

    def allowed_data_types(self) -> list:
        return self.data_type.values_list("slug", flat=True)

    def check_daily_access(self) -> bool:
        return True if self.request_day_count < self.request_day_limit else False

    def check_monthly_access(self) -> bool:
        return True if self.request_month_count < self.request_month_limit else False

    def check_total_access(self) -> bool:
        return True if self.request_total_count < self.request_total_limit else False

    # метод для списка регионов

    def save(self, *args, **kwargs):
        if not self.pk:
            user = get_user_model()._default_manager.create_user(username=self.name)
            self.user = user
        super().save(*args, **kwargs)
