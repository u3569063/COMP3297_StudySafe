from django.db import models

# Create your models here.
class Venue(models.Model):
    venue_code = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    type = models.CharField(max_length=2)
    capacity = models.IntegerField()

class Member(models.Model):
    hkuid = models.CharField(max_length=10)
    name = models.CharField(max_length=150)

class Record(models.Model):
    hkuid = models.ForeignKey(Member, on_delete=models.CASCADE)
    venue_code = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    action = models.BinaryField()