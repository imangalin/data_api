from django.db import models

class Building (models.Model):
   geom = models.CharField(max_length=200)
   storey = models.IntegerField(u'Кол-во чего-то', default=0)
   household = models.IntegerField(u'Кол-во домохозяйств', default=0)
   people = models.IntegerField(u'Кол-во человек', default=0)
   year = models.IntegerField(u'Год', default=0)
   region = models.CharField(max_length=200)

   class Meta:
        verbose_name = u'Строение'
        verbose_name_plural = u'Строения'
        db_table = 'data_building'

   def __str__(self):
        return self.id
