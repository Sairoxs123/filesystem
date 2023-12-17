from django.shortcuts import render, redirect
from core.models import *

# Create your views here.

def index(request):

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            res = Users.objects.get(email=email)

            if res.password == password:
                request.session["email"] = email
                return redirect("/")

            else:
                return render(request, 'login/index.html', {'error': 'Password is incorrect.'})

        except:
            return render(request, 'login/index.html', {"error":'Account doesn\'t exist.'})

    return render(request, 'login/index.html')
