# Generated by Django 4.0.2 on 2022-05-02 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subapps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='coin',
            field=models.CharField(default='', max_length=10),
        ),
    ]