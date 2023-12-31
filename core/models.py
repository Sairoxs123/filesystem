from django.db import models
import datetime

def filePath(instance, filename):
    return f"{instance.uploaded_by.email}{instance.folder}/{filename}"

# Create your models here.

class Users(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    email = models.EmailField("Email", max_length=30)
    password = models.CharField("Password", max_length=30)

    def __str__(self):
        return self.email

class Files(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    uploaded_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to=filePath)
    folder = models.CharField("Folder", max_length=35)
    date = models.DateField(name="date", verbose_name="Date")
    time = models.TimeField(name="time", verbose_name="Time")

    def __str__(self):
        return self.file.name

class Folders(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField('Folder Name', max_length=128)
    specialname = models.CharField("Special Name", max_length=30, unique=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    url = models.CharField("URL", max_length=128)
    files = models.ManyToManyField(Files, related_name="files", blank=True)
    public = models.BooleanField("Public")
    access = models.ManyToManyField(Users, related_name="access", blank=True)
    date = models.DateField(name="fdate", verbose_name="Date")
    time = models.TimeField(name="ftime", verbose_name="Time", default=datetime.datetime.now().strftime("%H:%M:%S"), null=True)
