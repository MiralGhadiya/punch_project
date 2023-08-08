# from django.contrib import admin
from django.urls import path
from .views import registerview,loginview,PunchInView,PunchOutView

urlpatterns = [
    path('register/',registerview.as_view()),
    path('login/',loginview.as_view()),
    path('punch_in/<int:id>/',PunchInView.as_view()),
    path('punch_out/<int:id>/',PunchOutView.as_view()),

]