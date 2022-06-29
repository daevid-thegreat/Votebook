# Generated by Django 4.0.3 on 2022-06-21 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_user_party_user_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('President', 'President'), ('Prime Minister', 'Prime Minister'), ('Head of State', 'Head of State'), ('Honorable', 'Honorable')], default='Honorable', max_length=255),
        ),
    ]