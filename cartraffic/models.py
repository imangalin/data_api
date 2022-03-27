from django.db import models

class CarTraffic (models.Model):
   geom = models.CharField(max_length=200)
   traf_day = models.IntegerField(u'Количество машин в день', default=0)
   shape_leng = models.FloatField(u'Протяженность участка, км', default=0)
   region = models.CharField(u'Регион', max_length=200)

   class Meta:
        verbose_name = verbose_name_plural = u'Автомобильный трафик'
        db_table = 'car_traffic'

   def __str__(self):
        return self.id
