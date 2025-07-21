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
