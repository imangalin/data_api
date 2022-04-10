from django.db import models


class Building (models.Model):
    geom = models.CharField(max_length=200)
    storey = models.IntegerField(u'Этажность', default=0)
    household = models.IntegerField(u'Количество домохозяйств', default=0)
    people = models.IntegerField(u'Население, человек', default=0)
    year = models.IntegerField(u'Год', default=0)
    region = models.CharField(max_length=200)

    class Meta:
        verbose_name = u'Строение'
        verbose_name_plural = u'Строения'
        db_table = 'build'

    def __str__(self):
        return str(self.id)


class PedTraffic(models.Model):
    geom = models.CharField(max_length=200)
    traf_day = models.IntegerField(u'Количество машин в день', default=0)
    region = models.CharField(u'Регион', max_length=200)

    class Meta:
        verbose_name = verbose_name_plural = u'Пешеходный трафик'
        db_table = 'ped_traffic'

    def __str__(self):
        return str(self.id)


class CarTraffic (models.Model):
    geom = models.CharField(max_length=200)
    traf_day = models.IntegerField(u'Количество машин в день', default=0)
    shape_leng = models.FloatField(u'Протяженность участка, км', default=0)
    region = models.CharField(u'Регион', max_length=200)

    class Meta:
        verbose_name = verbose_name_plural = u'Автомобильный трафик'
        db_table = 'car_traffic'

    def __str__(self):
        return str(self.id)