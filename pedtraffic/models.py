from django.db import models


class PedTraffic(models.Model):
    geom = models.CharField(max_length=200)
    traf_day = models.IntegerField(u'Количество машин в день', default=0)

    class Meta:
        verbose_name = verbose_name_plural = u'Пешеходный трафик'
        db_table = 'ped_traffic'

    def __str__(self):
        return str(self.id)
