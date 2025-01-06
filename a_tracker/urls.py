from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('toggle_favorito/<int:grupo_id>/', views.toggle_favorito, name='toggle_favorito'),
]