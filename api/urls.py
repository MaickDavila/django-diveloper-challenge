from django.urls import path
from .views import *

urlpatterns = [
    path("user/", UserView.as_view()),
    path("pet/<str:user_email>/", PetView.as_view()),
    path("pet/<str:user_email>/<int:pk>/", PetView.as_view()),
    path("toy/<str:user_email>/", ToyView.as_view()),
]
