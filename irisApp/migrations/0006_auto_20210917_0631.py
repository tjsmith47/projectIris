# Generated by Django 2.2 on 2021-09-17 06:31

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irisApp', '0005_auto_20210917_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/server/media/'), upload_to='server/media/'),
        ),
    ]
