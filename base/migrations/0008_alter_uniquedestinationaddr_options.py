# Generated by Django 3.2.8 on 2021-10-23 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20211022_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uniquedestinationaddr',
            options={'ordering': ['-address']},
        ),
    ]
