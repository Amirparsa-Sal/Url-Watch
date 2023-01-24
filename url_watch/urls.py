from django.urls import path, include
from api import urls

urlpatterns = [
    path('api/', include(urls)),
]
