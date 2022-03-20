from django.db import models

class CarTraffic (models.Model):
   geom = models.CharField(max_length=200)
   traf_day = models.IntegerField(u'Кол-во машин в день', default=0)
   shape_leng = models.FloatField(u'Протяженность участка (км)', default=0)
   region = models.CharField(max_length=200)

   class Meta:
        verbose_name = u'Автомобильный трафик'
        verbose_name_plural = u'Автомобильный трафик'
        db_table = 'data_car_traffic'

   def __str__(self):
        return self.id
