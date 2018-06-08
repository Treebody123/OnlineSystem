# Generated by Django 2.0.5 on 2018-06-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EntryNOC', '0003_entrynoc_last_modify_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrynoc',
            name='acknowledge_status',
            field=models.CharField(choices=[('-', '--------'), ('P', 'Partial Accept'), ('A', 'Accept'), ('R', 'Reject')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='entrynoc',
            name='finding_source',
            field=models.CharField(choices=[('--', '--------'), ('QC', 'NOC Daily QC'), ('PM', 'WAN PMA report'), ('QM', 'NOC QM'), ('DM', 'Dept. QM'), ('N2', 'CI/OSN2'), ('N3', 'CI/OSN3'), ('N6', 'CI/OSN6'), ('N7', 'CI/OSN7'), ('N8', 'CI/OSN8'), ('R5', 'CI/OSR5-SG'), ('AM', 'CI/OSR1-AM')], default='--', max_length=2),
        ),
    ]
