# Generated by Django 3.2.8 on 2021-11-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20211024_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniquesourceaddr',
            name='tolerence_level',
            field=models.FloatField(default=1),
        ),
    ]
