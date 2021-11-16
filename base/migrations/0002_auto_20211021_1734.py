# Generated by Django 3.2.8 on 2021-10-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationAddr',
            fields=[
                ('sequence_number', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('destination_addr', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceAddr',
            fields=[
                ('sequence_number', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('source_addr', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Destination_Addr',
        ),
        migrations.DeleteModel(
            name='Source_Addr',
        ),
        migrations.DeleteModel(
            name='KnxDump',
        ),
        migrations.DeleteModel(
            name='LogKzh',
        ),
        migrations.DeleteModel(
            name='LogKzhOld',
        ),
        migrations.DeleteModel(
            name='UnknownTelegram',
        ),
    ]
