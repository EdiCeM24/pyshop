# Generated by Django 4.0.3 on 2022-03-30 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_offer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='offer',
            new_name='offers',
        ),
    ]