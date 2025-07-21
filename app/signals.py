import os
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.tasks import send_order_mail
from .models import Order


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, **kwargs):
    if created:
        # Send real-time WebSocket notification to admin group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "admin_notifications",
            {
                "type": "admin.order_created",
                "message": f"🛒 New order by {instance.customer_name} - ${instance.order_total}",
            },
        )

        # Send email notification
        send_order_mail.delay(instance.customer_name, instance.order_total)
        # send_mail(
        #     subject=f"New Order from {instance.customer_name}",
        #     message=f"Order total: ${instance.order_total}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=["q76t6myb9j@vwhins.com"],
        #     fail_silently=False,  # So you can see errors
        # )
