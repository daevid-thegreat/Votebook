# Generated by Django 4.0.3 on 2022-06-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]