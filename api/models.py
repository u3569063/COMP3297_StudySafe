from django.db import models


# Create your models here.
class Venue(models.Model):
    venue_code = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    type = models.CharField(max_length=2)
    capacity = models.IntegerField()

    def __str__(self):
        return self.venue_code


class Member(models.Model):
    hkuid = models.CharField(max_length=10)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.hkuid


class AccessRecord(models.Model):
    hkuid = models.ForeignKey(Member, on_delete=models.CASCADE)
    venue_code = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    action = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.hkuid}: {self.venue_code} {self.action} | {self.date_time}"


class PositiveCases(models.Model):
    hkuid = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_of_diagnosis = models.DateField()

    def __str__(self):
        return f"{self.hkuid}: {self.date_of_diagnosis}"
