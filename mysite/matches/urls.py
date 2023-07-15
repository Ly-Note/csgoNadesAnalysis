from django.urls import path
from . import views


app_name = 'match'
urlpatterns = [
    path("", views.SeriesView.as_view(), name="series"),
    path("<str:seriesName>/", views.MatchesView.as_view(), name="matches"),
    path("<str:seriesName>/<str:matchId>/", views.hurtsList, name="hurt"),
    path("sucess", views.sucess, name="sucess"),
    path("uploads", views.upload_json, name="uploads"),
    
]