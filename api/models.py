from django.db import models
from django.contrib.gis.db.models import PointField


class Building(models.Model):
    storey = models.IntegerField("Этажность", default=0)
    household = models.IntegerField("Количество домохозяйств", default=0)
    people = models.IntegerField("Население, человек", default=0)
    year = models.IntegerField("Год", default=0)
    lat = models.DecimalField(max_digits=22, decimal_places=12)
    long = models.DecimalField(max_digits=22, decimal_places=12)
    h3_12 = models.CharField("H3_12", max_length=20)
    h3_13 = models.CharField("H3_13", max_length=20)
    geom = PointField()
    region = models.ForeignKey(
        "account.DataRegion",
        on_delete=models.SET_NULL,
        related_name="buildings",
        null=True,
    )

    class Meta:
        verbose_name = "Строение"
        verbose_name_plural = "Строения"
        db_table = "build"

    def __str__(self):
        return str(self.id)


class PedTraffic(models.Model):
    geom = PointField()
    traffic_total = models.IntegerField("Количество машин в день", default=0)
    lat = models.DecimalField(max_digits=22, decimal_places=12)
    long = models.DecimalField(max_digits=22, decimal_places=12)
    h3_12 = models.CharField("H3_12", max_length=20)
    h3_13 = models.CharField("H3_13", max_length=20)
    region = models.ForeignKey(
        "account.DataRegion", on_delete=models.SET_NULL, related_name="ped", null=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "Пешеходный трафик"
        db_table = "ped_traffic"

    def __str__(self):
        return str(self.id)


class CarTraffic(models.Model):
    geom = PointField()
    traffic_total = models.IntegerField("Количество машин в день", default=0)
    lat = models.DecimalField(max_digits=22, decimal_places=12)
    long = models.DecimalField(max_digits=22, decimal_places=12)
    h3_12 = models.CharField("H3_12", max_length=20)
    h3_13 = models.CharField("H3_13", max_length=20)
    region = models.ForeignKey(
        "account.DataRegion", on_delete=models.SET_NULL, related_name="cars", null=True
    )

    class Meta:
        verbose_name = verbose_name_plural = "Автомобильный трафик"
        db_table = "car_traffic"

    def __str__(self):
        return str(self.id)
