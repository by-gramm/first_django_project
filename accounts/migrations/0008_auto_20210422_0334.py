# Generated by Django 3.1.7 on 2021-04-21 18:34

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210421_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='따로 지정하지 않으면 기본 이미지로 저장됩니다.', upload_to='profile_image/%Y/%m/%d'),
        ),
    ]
