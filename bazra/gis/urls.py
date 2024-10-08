from django.urls import path
from gis import views

urlpatterns = [
    path("reverse-geocode/", views.reverse_geocode, name="reverse-geocode"),
    path("location-search/", views.location_search, name="location-search"),
    path("route/", views.route, name="route"),
    path("map/", views.map, name="map"),
    path(
        "distance_and_duration/",
        views.distance_and_duration,
        name="distance_and_duration",
    ),
]
