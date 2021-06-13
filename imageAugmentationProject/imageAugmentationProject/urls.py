from django.urls import path, include

urlpatterns = [
    path('augmentation/', include('imageAugmentationApp.urls'))
]