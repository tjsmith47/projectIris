# Generated by Django 2.2 on 2021-09-21 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irisApp', '0008_auto_20210920_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
