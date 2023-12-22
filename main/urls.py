from django.urls import path

from main.apps import MainConfig
from main.views import SecretCreateAPIView, show_secret

app_name = MainConfig.name

urlpatterns = [
    path('generate/', SecretCreateAPIView.as_view(), name='generate'),
    path('secrets/<str:secret_key>/', show_secret, name='show_secret')
]
