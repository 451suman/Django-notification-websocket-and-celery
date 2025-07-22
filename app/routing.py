from django.urls import re_path
from app import consumers

websocket_urlpatterns = [
    re_path(
        r"^ws/notifications/(?P<room_name>\w+)/$",
        consumers.NotificationConsumer.as_asgi(),
    ),
    re_path(
        r"^ws/corntab/(?P<room_name>\w+)/$",
        consumers.CorntabConsumer.as_asgi(),
    ),
]
