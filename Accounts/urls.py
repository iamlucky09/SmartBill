from django.urls import path
from . import views
urlpatterns=[
    path('add-user/',views.add_user,name="add-user")
]