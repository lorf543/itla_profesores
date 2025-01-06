from django.urls import path
from . import views

urlpatterns = [
    path('',views.loging_view, name="login_view")
]