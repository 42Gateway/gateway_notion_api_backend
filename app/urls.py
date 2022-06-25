from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('checkin/<str:user>', views.CheckInView.as_view())
]
