from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('room/<int:pk>/', login_required(RoomView.as_view()), name = 'room'),
    path('delete_event/<int:event_id>/', login_required(views.delete_event), name = 'delete_event'),
]