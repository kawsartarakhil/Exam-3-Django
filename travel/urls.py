from django.urls import path
from .views import *

urlpatterns = [
    path("",trip_list_view,name='trip_list'),
    path('trip/create/', trip_create_view, name='trip_create'),
    path("trip/<int:pk>/", trip_detail_view, name="trip_detail"),
    path("trip/<int:pk>/edit/", trip_update_view, name="trip_update"),
    path("trip/<int:pk>/delete/", trip_confirm_delete, name="trip_delete"),
]
