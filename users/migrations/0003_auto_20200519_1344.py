# Generated by Django 3.0.6 on 2020-05-19 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='users'),
        ),
    ]