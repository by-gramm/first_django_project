# Generated by Django 3.1.7 on 2021-04-13 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210412_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]