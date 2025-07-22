from time import sleep
from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from channels.layers import get_channel_layer

from app.models import Order
from asgiref.sync import async_to_sync


@shared_task
def delayed_order_task(order_id):
    sleep(5)
    print(f"Order ID: {order_id}")


@shared_task
def send_order_mail(customer_name, order_total):

    send_mail(
        subject=f"New Order from {customer_name}",
        message=f"Order total: ${order_total}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["q76t6myb9j@vwhins.com"],
        fail_silently=False,  # So you can see errors
    )


@shared_task
def get_all_orders():
    from app.models import Order  # Adjust to your app name
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from time import sleep

    print("Getting all orders...")
    try:
        # Use 'order_date' instead of 'created_at'
        orders = Order.objects.all()
        channel_layer = get_channel_layer()
        for order in orders:
            async_to_sync(channel_layer.group_send)(
                "admin",
                {
                    "type": "admin_notification",
                    "message": f"🛒 New order by {order.customer_name} - ${order.order_total}",
                },
            )
        print("Notification sent.")
    except Order.DoesNotExist:
        print("No orders found.")
