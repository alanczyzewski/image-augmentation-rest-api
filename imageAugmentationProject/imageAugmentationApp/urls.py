from django.urls import path
from . import views

urlpatterns = [
    path('resize', views.resizeView),
    path('crop', views.cropView),
    path('rotate', views.rotateView),
    path('negative', views.negativeView)
]
