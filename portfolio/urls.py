from django.urls import path
from . import views

urlpatterns = [
    path("work/", views.work, name="work"),
    path("work/<slug:slug>", views.case_study, name="case_study"),
]
