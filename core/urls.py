from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('create/folder', createFolder, name="createFolder"),
    path('folder/<str:special>', folder, name="folder"),
    path('upload/file', uploadFile, name="uploadFile"),
    path('folder/grant/access', grantAccess, name="grantAccess"),
    path('folder/change/type', changeType, name="changetype"),
    path('delete/folder', deleteFolder, name="deletefolder"),
    path('file/delete', deleteFile, name="deletefile"),
    path('search/', search, name="search"),
    path('logout/', logout, name = "logout")
]
