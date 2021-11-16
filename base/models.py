from django.db import models

# Create your models here.

class SourceAddr(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.address)

class DestinationAddr(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.address)

class UniqueSourceAddr(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=20, unique=True)
    tolerence_level = models.FloatField(default=1)

    def __str__(self):
        return str(self.address)

    class Meta:
        ordering = ['address']


class UniqueDestinationAddr(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return str(self.address)

    class Meta:
        ordering = ['address']

class SourceToDestination(models.Model):
    sequence_number = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source_addr = models.CharField(max_length=20, blank=True, null=True)
    destination_addr = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.timestamp)