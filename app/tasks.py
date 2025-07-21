from time import sleep
from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


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
