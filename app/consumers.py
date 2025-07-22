import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        print()
        if user.is_superuser:
            self.room_group_name = "admin_notifications"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()  # Reject if not admin

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    # Custom event handler name must match "type"
    async def admin_order_created(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"type": "admin_notification", "message": message})
        )


import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CorntabConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            # Do something with data, for example:
            print("Received from frontend:", data)

            # Optionally, send a response back:
            await self.send(
                text_data=json.dumps(
                    {"type": "response", "message": "Message received!"}
                )
            )

    async def admin_notification(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"type": "admin_notification", "message": message})
        )
