from django.urls import path, re_path

from .views import wildcard_redirect

urlpatterns = [
    re_path('(?P<path>.*)', wildcard_redirect)
]
