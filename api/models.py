from django.db import models

# Create your models here.
class Venue(models.Model):
    Venue_Code = models.CharField(max_length=20, unique=True)
    Location = models.CharField(max_length=150)
    Type = models.CharField(max_length=2)
    Capacity = models.IntegerField()
    def __str__(self):
        return self.Location

class Member(models.Model):
    HKU_ID = models.CharField(max_length=10, unique=True)
    Name = models.CharField(max_length=150)
    def __str__(self):
        return self.Name

class AccessRecord(models.Model):
    HKU_ID = models.ForeignKey(Member, on_delete=models.CASCADE)
    Venue_Code = models.ForeignKey(Venue, on_delete=models.CASCADE)
    Date_Time = models.DateTimeField()
    Action = models.CharField(max_length=5)
    def __str__(self):
        return f"{self.HKU_ID}: {self.Venue_Code} {self.Action} | {self.Date_Time}"

class PositiveCase(models.Model):
    HKU_ID = models.ForeignKey(Member, on_delete=models.CASCADE)
    Date_Of_Diagnosis = models.DateField()
    def __str__(self):
        return f"{self.HKU_ID}: {self.Date_Of_Diagnosis}"