from django.contrib import admin
from .models import EntrySOC

# Register your models here.



@admin.register(EntrySOC)
class EntrySOCAdmin(admin.ModelAdmin):
    list_display = ('ticket_num','rep_date')
