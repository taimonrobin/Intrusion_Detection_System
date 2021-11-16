# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class KnxDump(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source_addr = models.CharField(max_length=9)
    destination_addr = models.CharField(max_length=9)
    apci = models.CharField(max_length=50)
    tpci = models.CharField(max_length=50)
    priority = models.CharField(max_length=6)
    repeated = models.IntegerField()
    hop_count = models.PositiveIntegerField()
    apdu = models.TextField(blank=True, null=True)
    payload_length = models.PositiveSmallIntegerField(blank=True, null=True)
    cemi = models.TextField(blank=True, null=True)
    payload_data = models.CharField(max_length=100, blank=True, null=True)
    is_manipulated = models.IntegerField()
    attack_type_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'knx_dump'


class LogKzh(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source_addr = models.CharField(max_length=9, blank=True, null=True)
    destination_addr = models.CharField(max_length=9, blank=True, null=True)
    extended_frame = models.PositiveIntegerField(blank=True, null=True)
    priority = models.CharField(max_length=6, blank=True, null=True)
    repeat = models.PositiveIntegerField(blank=True, null=True)
    ack_req = models.PositiveIntegerField(blank=True, null=True)
    confirm = models.PositiveIntegerField(blank=True, null=True)
    system_broadcast = models.PositiveIntegerField(blank=True, null=True)
    hop_count = models.PositiveIntegerField(blank=True, null=True)
    tpci = models.CharField(max_length=25, blank=True, null=True)
    tpci_sequence = models.PositiveIntegerField(blank=True, null=True)
    apci = models.CharField(max_length=50, blank=True, null=True)
    payload_data = models.CharField(max_length=256, blank=True, null=True)
    payload_length = models.PositiveSmallIntegerField(blank=True, null=True)
    is_manipulated = models.PositiveIntegerField()
    attack_type_id = models.PositiveIntegerField(blank=True, null=True)
    sensor_addr = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'log_kzh'


class LogKzhOld(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source_addr = models.CharField(max_length=9, blank=True, null=True)
    destination_addr = models.CharField(max_length=9, blank=True, null=True)
    apci = models.CharField(max_length=50, blank=True, null=True)
    tpci = models.CharField(max_length=50, blank=True, null=True)
    priority = models.CharField(max_length=6, blank=True, null=True)
    repeated = models.IntegerField(blank=True, null=True)
    hop_count = models.PositiveIntegerField(blank=True, null=True)
    apdu = models.TextField(blank=True, null=True)
    payload_length = models.PositiveSmallIntegerField(blank=True, null=True)
    cemi = models.TextField(blank=True, null=True)
    payload_data = models.CharField(max_length=100, blank=True, null=True)
    is_manipulated = models.IntegerField()
    attack_type_id = models.PositiveIntegerField(blank=True, null=True)
    sensor_addr = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'log_kzh_old'


class UnknownTelegram(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    cemi = models.TextField(blank=True, null=True)
    sensor_addr = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'unknown_telegram'

