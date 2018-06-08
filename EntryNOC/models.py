from django.db import models
from django.utils.encoding import python_2_unicode_compatible
#import datetime
from django.contrib.auth.models import User
from django.utils.html import format_html


# Create your models here.

SOURCE_CHOICES =(
    ('--','--------'),
    ('QC','NOC Daily QC'),
    ('PM','WAN PMA report'),
    ('QM','NOC QM'),
    ('DM','Dept. QM'),
    ('N2','CI/OSN2'),
    ('N3','CI/OSN3'),
    ('N6','CI/OSN6'),
    ('N7','CI/OSN7'),
    ('N8','CI/OSN8'),
    ('R5','CI/OSR5-SG'),
    ('AM','CI/OSR1-AM'),
    ('UF','User Feedback'),
)

STATUS_CHOICES = (
    ('-','--------'),
    ('R','Resolved'),
    ('C','Cancelled'),
    ('A','Assigned'),
)

LEVEL_CHOICES=(
    ('--','--------'),
    ('Mi','Minor'),
    ('Ma','Major'),
    ('Cr','Critical'),
)

ACK_CHOICES=(
    ('-','--------'),
    ('P','Partial Accept'),
    ('A','Accept'),
    ('R','Reject'),
)

@python_2_unicode_compatible
class UserFullName(User):
    class Meta:
        proxy=True
    def __str__(self):
        return self.get_full_name()


@python_2_unicode_compatible
class EntryNOC(models.Model):
    rep_date = models.DateField('Report Date')
    last_modify_date = models.DateField('Last Modified',auto_now=True)
    finding_source = models.CharField(max_length=2,choices=SOURCE_CHOICES,default='--')
    ticket_num = models.CharField(max_length=100)
    finding_description = models.TextField(blank=False)
    finding_level = models.CharField(max_length=2,choices=LEVEL_CHOICES,default='--')
    finding_responsible = models.ForeignKey(UserFullName,on_delete=models.CASCADE,null=True,blank=True,default=None,limit_choices_to ={'groups__name':'NOC_Group_Members'})
#    finding_responsible = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, default=None)
    quality_track_measurement = models.TextField(blank=True)
    acknowledge_status = models.CharField(max_length=1,choices=ACK_CHOICES,default='-')
    email_send = models.BooleanField(default=False)
    quality_track_comments = models.TextField(blank=True)
    finding_final_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='-')


    def __str__(self):
        return self.ticket_num


    def Colored_status(self):
        color_code = 'black'
        if self.finding_level == 'Ma':
            color_code = 'orange'
        elif self.finding_level == 'Cr':
            color_code = 'red'
        return format_html(
            '<span style ="color: {};">{}</span>',
            color_code,
            self.get_finding_level_display(),
        )

    class Meta:
        verbose_name = 'Quality Entries'           # in the change or add page, the name on add button
        verbose_name_plural = 'Quality Entries For NOC'    # colum name in Admin page


    Colored_status.short_description = 'finding_level'
    Colored_status.admin_order_field = 'finding_level'




