# Generated by Django 3.1.7 on 2021-04-13 17:09

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='profile_image\\%Y\\%m\\%d'),
        ),
    ]
