from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    # as_view()
    path("uploads", views.upload_json, name="uploads"),
    path("uploads_sucess", views.sucess, name="uploads_sucess"),
]