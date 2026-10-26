from django.shortcuts import render,redirect
from .models import *
from .helpers import *
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group

def home_view(request):
    return render(request,'home.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email:
            return render(request,"register.html",{"error":"Email field must be filled "})

        if password1!=password2:
            return render(request,"register.html",{"error":"Passwords Do not match"})

        if CustomUser.objects.filter(email=email).exists():
            return render(request,"register.html",{"error":"User with this email already exists"})

        user=CustomUser.objects.create_user(email=email,password=password2,first_name=first_name,last_name=last_name)
        passenger_group = Group.objects.get(name="Passengers")
        user.groups.add(passenger_group)
        token = EmailConfimation.objects.create(user=user)

        send_confirmation_email(token)
        return HttpResponse("""Please check your email""")

    return render(request,"register.html")

            
def confirm_token_view(request, token):
    confirmation = EmailConfimation.objects.filter(token=token).first()
    if not confirmation:
        return HttpResponse("Invalid token")
    confirmation.user.is_active = True
    confirmation.user.save()
    confirmation.delete()
    return redirect("login")


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,email=email,password=password)

        if not user:
            return render(request,"login.html",{"error":"incorrect crediantials"})

        login(request,user)

        return redirect("home")
    return render(request,"login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    if request.method == 'POST':
        picture = request.FILES.get("profile_picture")
        if not picture:
            return render(request,'profile.html',{"error":"choose an image file first"})
        elif not picture.content_type.startswith("image/"):
            return render(request,'profile.html',{"error":"The file must be an image"})
        else:
            request.user.profile_picture = picture
            request.user.save(update_fields=["profile_picture"])
            return redirect("profile")
         
    trips = request.user.trips.all().order_by("-created_at")
    requests = request.user.companion_requests.all().order_by("-created_at")
    return render(request,'profile.html',{"trips":trips,"requests":requests})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get("old_password")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if not password1:
            return render(request, "change_password.html", {"error": "Password cannot be empty"})
        if not request.user.check_password(old_password):
            return render(request, "change_password.html", {"error": "incorrect old password"})
        if password1 != password2:
            return render(request, "change_password.html", {"error": "Passwords do not match"})
        request.user.set_password(password1)
        request.user.save()
        return redirect("login")
    return render(request, "change_password.html")




def reset_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return HttpResponse("User does not exist")
        token = EmailConfimation.objects.filter(user=user).first()
        if not token:
            token = EmailConfimation.objects.create(user=user)
        send_reset_password_email(token)
        return HttpResponse("Check your email for the token")
    return render(request, "reset_password.html")


def confirm_reset_password_view(request, token):
    confirmation = EmailConfimation.objects.filter(token=token).first()
    if not confirmation:
        return HttpResponse("Invalid or expired token")
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if not password1:
            return render(request, "confirm_reset_password.html", {"error": "Password cannot be empty"})
        if password1 != password2:
            return render(request, "confirm_reset_password.html", {"error": "Passwords do not match"})
        user = confirmation.user
        user.set_password(password1)
        user.save()
        confirmation.delete()
        return redirect("login")

    return render(request, "confirm_reset_password.html")




def resend_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user:
            return render(request, "resend.html", {"error": "User does not exist"})
        if user.is_active:
            return render(request, "resend.html", {"error": "Your email is already confirmed"})
        token = EmailConfimation.objects.filter(user=user).first()
        if not token:
            token = EmailConfimation.objects.create(user=user)
        send_confirmation_email(token)
        return render(request, "resend.html", {"success": "Confirmation email sent. Check your inbox."})

    return render(request, "resend.html")


def resend_reset_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = CustomUser.objects.filter(email__iexact=email).first()

        if not user:
            return render(request, "reset_password.html", {
                "error": "User does not exist",
                "email": email
            })

        token = EmailConfimation.objects.filter(user=user).first()

        if not token:
            token = EmailConfimation.objects.create(user=user)

        send_reset_password_email(token)

        return render(request, "reset_password.html", {
            "success": "Reset email sent. Check your inbox.",
            "email": email
        })

    return redirect("reset_password")
