from django.shortcuts import render,redirect
from .models import *
from django.utils import timezone
from django.utils.dateparse import parse_date,parse_datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from .permissions import can_manage_trip,can_manage_companion_requeest
from django.core.exceptions import PermissionDenied


def trip_list_view(request):
    trips = Trip.objects.all().order_by("date")
    start = request.GET.get("start_location")
    end = request.GET.get("end_location")
    date_text = request.GET.get("date")
    if start:
        trips = trips.filter(start_location__icontains=start)
    if end:
        trips = trips.filter(end_location__icontains=end)
    if date_text:
        search_date = parse_date(date_text)
        if search_date:
            trips = trips.filter(date__date=search_date)
    return render(request, "trip_list.html", {"trips": trips})

def trip_detail_view(request, pk):
    trip = Trip.objects.get(pk=pk)
    can_manage = request.user.is_authenticated and can_manage_trip(request.user, trip)

    return render(request, "trip_detail.html", {"trip": trip,"can_manage": can_manage})

@login_required
@permission_required("travel.add_trip", raise_exception=True)
def trip_create_view(request):
    if request.method == 'POST':
        start = request.POST.get("start_location")
        end = request.POST.get("end_location")
        date = request.POST.get("date")
        seats = int(request.POST.get("seats_available"))
        description = request.POST.get("description")
        car_picture = request.FILES.get("car_picture")
        if not start or not end:
            return render(request, "trip_create.html", {"error": "Start and end destination are required"})
        if not date:
            return render(request, "trip_create.html", {"error": "Enter a valid date and time"})
        if seats < 1:
            return render(request, "trip_create.html", {"error": "Available seats must be at least 1"})

        Trip.objects.create(user=request.user,start_location=start,end_location=end,date=date, seats_available=seats, description=description,car_picture=car_picture)
        return redirect("trip_list")

    return render(request, "trip_create.html")

        
@login_required
def trip_update_view(request, pk):
    trip = Trip.objects.get(pk=pk)
    if not can_manage_trip(request.user, trip):
        raise PermissionDenied
    
    if request.method == "POST":
        start = request.POST.get("start_location")
        end = request.POST.get("end_location")
        date_text = request.POST.get("date")
        seats_text = request.POST.get("seats_available")
        description = request.POST.get("description")
        car_picture = request.FILES.get("car_picture")
        date_value = parse_datetime(date_text)
        seats = int(seats_text)

        if not start or not end or not date_value or seats < 1:
            return render(request, "trip_update.html", {"trip": trip,"error": "Enter valid locations, date/time, and at least one seat."})
        trip.start_location = start
        trip.end_location = end
        trip.date = date_value
        trip.seats_available = seats
        trip.description = description
        if car_picture:
            trip.car_picture = car_picture
        trip.save()
        return redirect("trip_detail", pk=trip.pk)

    return render(request, "trip_update.html", {"trip": trip})

@login_required
def trip_confirm_delete(request, pk):
    trip = Trip.objects.get(pk=pk)

    if not can_manage_trip(request.user, trip):
        raise PermissionDenied
    if request.method == "POST":
        trip.delete()
        return redirect("trip_list")
    return render(request, "trip_delete.html", {"trip": trip})


def request_list_view(request):
    requests = CompanionRequest.objects.all().order_by("date")
    start = request.GET.get("start_location")
    end = request.GET.get("end_location")
    date_text = request.GET.get("date")
    if start:
        requests = requests.filter(start_location__icontains=start)
    if end:
        requests = requests.filter(end_location__icontains=end)
    if date_text:
        search_date = parse_date(date_text)
        if search_date:
            requests = requests.filter(date__date=search_date)

    return render(request, "request_list.html", {"requests": requests})


@login_required
def request_create_view(request):
    if not request.user.has_perm("travel.add_companionrequest"):
        raise PermissionDenied
    if request.method == "POST":
        start = request.POST.get("start_location")
        end = request.POST.get("end_location")
        date_text = request.POST.get("date")
        description = request.POST.get("description")
        if not start or not end:
            return render(request, "request_create.html", {"error": "Start and end destination are required"})
        date = parse_datetime(date_text)

        CompanionRequest.objects.create(user=request.user,start_location=start,end_location=end,date=date,description=description)
        return redirect("request_list")
    
    return render(request, "request_create.html")

@login_required
def request_update_view(request, pk):
    companion_request = CompanionRequest.objects.get(pk=pk)
    if not request.user.has_perm("travel.change_companionrequest"):
        raise PermissionDenied

    if request.method == "POST":
        start = request.POST.get("start_location")
        end = request.POST.get("end_location")
        date_text = request.POST.get("date")
        description = request.POST.get("description")
        date_value = parse_datetime(date_text)
        if not start or not end or not date_value:
            return render(request, "request_update.html", {"request": companion_request,"error": "Enter valid locations and date/time."})
        companion_request.start_location = start
        companion_request.end_location = end
        companion_request.date = date_value
        companion_request.description = description
        companion_request.save()
        return redirect("request_list")
    return render(request, "request_update.html", {"request": companion_request})

@login_required
def request_confirm_delete_view(request, pk):
    companion_request = CompanionRequest.objects.get(pk=pk)
    if not request.user.has_perm("travel.delete_companionrequest"):
        raise PermissionDenied
    
    if request.method == "POST":
        companion_request.delete()
        return redirect("request_list")
    return render(request, "request_delete.html", {"request": companion_request})
