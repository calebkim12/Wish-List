# Generated by Django 2.2 on 2019-04-25 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190425_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='date_added',
        ),
    ]
