from django.db import models

class CrimeReport(models.Model):
    year = models.PositiveIntegerField(null=True)
    month = models.PositiveIntegerField(null=True,choices=[
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ])
    date = models.DateField()
    # day = models.PositiveIntegerField()
    day_of_week = models.CharField(max_length=10,null=True ,choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    minutes = models.PositiveIntegerField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    crime = models.CharField(max_length=100, null =True)

    def __str__(self):
        return f"{self.year}-{self.month:02d} {self.day_of_week} ({self.latitude}, {self.longitude})"
