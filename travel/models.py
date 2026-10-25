from django.db import models
from django.conf import settings

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="trips")
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    date = models.DateTimeField()
    seats_available = models.PositiveIntegerField()
    description = models.TextField(null=True,blank=True)
    car_picture = models.ImageField(upload_to="car_pics/",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("manage_all_trips","Can manage all trips"),
        ]

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"


class CompanionRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="companion_requests")
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("manage_all_companionrequests","Can manage all companion requests"),
        ]

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"