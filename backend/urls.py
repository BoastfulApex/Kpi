from django.urls import path
from backend import views
from backend.api_views import SimpleCheckAPIView


urlpatterns = [

    path('', views.index, name='home'),
    path('api/check/', SimpleCheckAPIView.as_view(), name='simple-check'),]
