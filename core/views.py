from django.shortcuts import render, redirect, HttpResponse
from core.models import *
from random import choice
import datetime
import os
from pathlib import Path


# Create your views here.

def specialNameGenerator():
    chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']

    special = ""

    for i in range(32):
        special += choice(chars)

    try:
        res = Folders.objects.get(specialname=special)
        specialNameGenerator()

    except:
        return special

def folderPath(url, links, owner):

    if url.count("/") > 1:
        lexers = url.split("/")

        name = lexers[len(lexers) - 1]

        L = len(url) - len(name)

        parent = url[:L - 1]

        res = Folders.objects.get(url=parent, owner=owner)

        links.insert(0, [parent, res.specialname])

        folderPath(parent, links, owner)

    return links


def index(request):
    if not request.session.get("email"):
        return redirect("/login")

    emailinst = Users.objects.get(email=request.session["email"])

    results = Folders.objects.all().filter(owner=emailinst)

    folders = []

    for i in results:
        if i.url.count("/") == 1:
            folders.append(i)


    return render(request, "main/index.html", {"folders":folders})


def createFolder(request):

    if request.method == "POST":
        if not request.session.get("email"):
            return redirect("/login")
        name = request.POST["name"]
        owner = request.session["email"]
        parentdir = request.POST["parentdir"]
        url = parentdir + name
        typeof = int(request.POST["type"])

        ownerinst = Users.objects.get(email=owner)

        try:
            res = Folders.objects.get(url=url, owner=ownerinst, name=name)
            return HttpResponse("<h1>Folder with this name already exists</h1>")

        except:
            Folders.objects.create(name=name, owner=ownerinst, url=url, specialname=specialNameGenerator(), public=typeof, fdate=datetime.date.today())

            result = Folders.objects.get(name=name, owner=ownerinst, url=url)

            return redirect(f"/folder/{result.specialname}")

    return redirect("/")


def folder(request, special):
    try:
        res = Folders.objects.get(specialname=special)
    except:
        return redirect("/")

    if res.public == False:
        if not request.session.get("email"):
            return redirect("/login")
            #return HttpResponse("<h1>You cannot view this folder.</h1>")

        access = False

        for i in res.access.all():
            if i.email == request.session.get("email"):
                access = True

            else:
                access = False

        if res.owner.email != request.session.get("email") and access == False:
            return HttpResponse("<h1>You cannot view this folder.</h1>")

    n = res.url.count("/") + 1

    url = res.url + "/"

    folders = []

    z = Folders.objects.all().filter(url__contains=url)

    for i in z:
        if i.url.count("/") == n:
            folders.append(i)

    results = res.files.all()

    files = []

    ownerinst = Users.objects.get(email=request.session.get("email"))

    folderPaths = folderPath(res.url, [], ownerinst)

    links = []

    for i in folderPaths:
        x = i[0].split("/")
        y = x[len(x) - 1]
        links.append(f"""
<a href="/folder/{i[1]}">{y}</a>
""")

    files = results

    for i in files:
        name = str(i.file).split("/")
        i.file = name[len(name) - 1]

    users = list()

    Type = res.public

    if request.session.get("email") == str(res.owner):
        if Type == False:
            x = Users.objects.all()

            for i in x:
                if i.email != request.session.get("email") and i not in res.access.all():
                    users.append(i)

        return render(request, "main/folder.html", {"url":url, "folders":folders, "files":files, "special":special, "users":users, "type":Type, "links":links, "name":res.name})

    return render(request, "main/folder.html", {"url":url, "folders":folders, "files":files, "special":special, "owner":False, "links":links, "name":res.name})

def uploadFile(request):
    if request.method == 'POST':
        if not request.session.get("email"):
            return redirect("/login")

        file = request.FILES.get("file")
        special = request.POST["special"]

        last = None

        try:
            last = Files.objects.all().last().id + 1
        except:
            last = 1

        uploadinst = Users.objects.get(email=request.session.get("email"))

        folderinst = Folders.objects.get(specialname=special)

        file_create = Files.objects.create(id=last, uploaded_by=uploadinst, folder=folderinst.url, file=file, date=datetime.date.today(), time=datetime.datetime.now().strftime("%H:%M:%S"))

        #file_create.file = file

        file_create.save()

        file_inst = Files.objects.get(id=last)

        res = Folders.objects.get(specialname=special)

        res.files.add(file_inst)

        res.save()

        return redirect(f"/folder/{special}")

    redirect("/login")


def grantAccess(request):
    if request.method == "POST":
        special = request.POST.get("special")

        res = Folders.objects.get(specialname=special)

        if str(res.owner) != request.session.get("email"):
            return HttpResponse("<h1>You cannot change the settings of this folder.</h1>")

        access = request.POST.get("access")

        users = access.split(",")

        for i in users:
            inst = Users.objects.get(email=i)

            if i not in res.access.all():
                res.access.add(inst)

        res.save()

        return redirect(f"/folder/{special}")

    return redirect("/login")

def changeType(request):
    if request.method == "POST":
        special = request.POST.get("special")
        public = int(request.POST.get("access"))

        res = Folders.objects.get(specialname=special)

        res.public = public

        res.save()

        return redirect(f"/folder/{special}")


def deleteFolder(request):
    if request.method == "POST":
        special = request.POST.get("special")
        returnto = request.POST.get("from")

        location = request.POST.get("location")

        res = Folders.objects.get(specialname=special)

        name = res.name

        owner = request.session.get("email")

        ownerinst = Users.objects.get(email=owner)

        results = Folders.objects.all().filter(url__contains=name).filter(owner=ownerinst)

        for i in results:
            i.delete()

        if location == "home":
            return redirect("/")

        else:
            return redirect(f"/folder/{returnto}")

def deleteFile(request):
    if request.method == "POST":
        returnto = request.POST.get("from")
        fileid = request.POST.get("id")

        location = request.POST.get("location")

        res = Files.objects.get(id=fileid)

        res.delete()

        assets = os.path.join(str(os.getcwd()), 'assets')

        filepath = os.path.join(assets, res.file.name)

        os.remove(filepath)


        if location == "home":
            return redirect("/")

        else:
            return redirect(f"/folder/{returnto}")

def search(request):
    query = request.GET.get("query")

    owner = request.session.get("email")

    ownerinst = Users.objects.get(email=owner)

    folders = Folders.objects.all().filter(name__contains=query).filter(owner=ownerinst)

    files = Files.objects.all().filter(file__contains=query).filter(uploaded_by=ownerinst)

    text = []


    if not folders and not files:

        text.append(f"""

            <a href="">
                <div class="item">
                    <div id="main">
                        <center>No results found.</center>
                    </div>
                </div>
            </a>

    """)

    else:

        for i in folders:
            text.append(f"""

                <a href="/folder/{i.specialname}">
                    <div class="item">
                        <div id="main">
                            <div class="item-name">
                                <svg height="35px" width="30px" focusable="false" viewBox="0 0 24 24" fill="#5f6368"
                                class="a-s-fa-Ha-pa">
                                <g>
                                    <path
                                        d="M20 6h-8l-2-2H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-5 3c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm4 8h-8v-1c0-1.33 2.67-2 4-2s4 .67 4 2v1z">
                                    </path>
                                    <path d="M0 0h24v24H0z" fill="none"></path>
                                </g>
                            </svg>
                                <h3> {i.name} </h3>
                            </div>
                            <div class="owner">
                                <p>{i.owner.email}</p>
                            </div>
                        </div>
                        <div id="date">
                            { i.fdate }
                        </div>
                    </div>
                </a>

    """)

        for i in files:
            text.append(f"""

                <a href="/assets/{i.file}" target="_blank">
                    <div class="item">
                        <div id="main">
                            <div class="item-name">
                                <h3> {i.file.name} </h3>
                            </div>
                            <div class="owner">
                                <p>{i.uploaded_by.email}</p>
                            </div>
                        </div>
                        <div id="date">
                            { i.date }
                        </div>
                    </div>
                </a>

    """)

    return HttpResponse(text)


def logout(request):
    del request.session["email"]
    return redirect("/login")


