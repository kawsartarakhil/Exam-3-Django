from django.contrib import admin
from .models import Trip,CompanionRequest

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display =("start_location","end_location","date","user","seats_available")
    search_fields = ("start_location","end_location","user_email")


@admin.register(CompanionRequest)
class CompanionRequestAdmin(admin.ModelAdmin):
    list_display =("start_location","end_location","date","user")
    search_fields = ("start_location","end_location","user_email")