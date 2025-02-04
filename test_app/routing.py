from django.urls import path
from test_app.consumers import LiftDataConsumer

websocket_urlpatterns = [
    path('ws/lift-data/', LiftDataConsumer.as_asgi()),
]
