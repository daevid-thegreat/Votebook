# Generated by Django 4.0.3 on 2022-06-20 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='party',
            old_name='name',
            new_name='party_name',
        ),
        migrations.DeleteModel(
            name='Candidate',
        ),
    ]