from django.urls import include, path

urlpatterns = [
    path('buildings', include('buildings.urls')),
]
