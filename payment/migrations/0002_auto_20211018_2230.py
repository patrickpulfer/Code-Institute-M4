# Generated by Django 3.2.8 on 2021-10-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='product_files/'),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
