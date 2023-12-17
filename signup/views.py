from django.shortcuts import render, redirect
from .forms import *
from core.models import *

# Create your views here.

def index(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        email = request.POST["email"]

        try:
            res = Users.objects.get(email=email)
            return render(request, "signup/index.html", {"form":SignupForm(), "exists":True})

        except:
            if form.is_valid():
                form.save()
                request.session["email"] = email
                return redirect("/")

    return render(request, "signup/index.html", {"form":SignupForm()})
