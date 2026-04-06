import requests
from django.conf import settings
import json
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import render_to_string

def generate_ssl_commerz_payment(request, order):
    post_body = {}
    post_body['store_id'] = settings.SSL_COMMERZE_STORE_ID
    post_body['store_passwd'] = settings.SSL_COMMERZE_STORE_PASSWORD
    post_body['total_amount'] = float(order.get_total_cost())
    post_body['currency'] = 'BDT'
    post_body['tran_id'] = str(order.id)
    post_body['success_url'] = request.build_absolute_uri(reverse('payment_success', args=[order.id]))
    post_body['fail_url'] = request.build_absolute_uri(reverse('payment_fail', args=[order.id]))
    post_body['cancel_url'] = request.build_absolute_uri(reverse('payment_cancel', args=[order.id]))
    post_body['cus_name'] = f'{order.first_name} {order.last_name}'
    post_body['cus_email'] = order.email
    post_body['cus_add1'] = order.address
    post_body['cus_city'] = order.city
    post_body['cus_country'] = 'Bangladesh'
    post_body['cus_phone'] = order.phone
    post_body['shipping_method'] = 'NO'
    post_body['product_name'] = 'Order'
    post_body['product_category'] = 'Mixed'
    post_body['product_profile'] = 'general'

    response = requests.post(settings.SSL_COMMERZE_PAYMENT_URL, data=post_body)
    try:
        return json.loads(response.text)
    except Exception:
        return {}

def send_order_confirmation_email(order):
    subject = f'Order Confirmation - Mallava (Order #{order.id})'
    html_content = render_to_string('emails/order_confirmation.html', {'order': order})
    text_content = f"Thank you for your order! Your order ID is #{order.id}."
    
    # Get unique recipient emails
    recipients = list(set([order.email, order.user.email]))
    
    email = EmailMultiAlternatives(
        subject, 
        text_content, 
        getattr(settings, 'EMAIL_HOST_USER', 'noreply@mallava.com'), 
        recipients
    )
    email.attach_alternative(html_content, "text/html")
    email.send()