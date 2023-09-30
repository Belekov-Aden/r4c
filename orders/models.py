from django.db import models

from customers.models import Customer
from robots.models import Robot
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string


import os

from dotenv import load_dotenv

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)


@receiver(post_save, sender=Robot)
def send_notification_email(sender, instance, **kwargs):
    if instance.available:
        orders = Order.objects.filter(robot=instance)
        for order in orders:
            subject = 'Робот доступен'
            message = render_to_string('notification_email.txt', {
                'model': instance.model,
                'version': instance.version,
            })
            from_email = os.environ.get('EMAIL_HOST_USER')
            recipient_list = [order.customer.email]
            send_mail(subject, message, from_email, recipient_list)

