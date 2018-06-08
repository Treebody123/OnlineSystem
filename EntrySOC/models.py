from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


@python_2_unicode_compatible
class EntrySOC(models.Model):
    rep_date = models.DateField('Report Date')
    ticket_num = models.CharField(max_length=30)


    def __str__(self):
        return self.ticket_num

    class Meta:
        verbose_name = 'Quality Entries For SOC'
        verbose_name_plural = 'Quality Entries For SOC'
