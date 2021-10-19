from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from profiles.models import Profile


#from .webhook_handler import StripeWH_Handler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print('**********')
    print(payload)
    print('**********')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        print('invalid payload')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('invalid signature')
        return HttpResponse(status=400)
    except Exception as e:
        print('invalid anything lol')
        return HttpResponse(content=e, status=400)

    if event['type'] == 'checkout.session.completed':
        payment_date = ['created']
        session = event['created']['object']
        session_id = session["id"]
        customer_email = session["customer_details"]["email"]
        currency = session["currency"]
        payment_status = session["payment_status"]
        amount_total = session["amount_total"]

        user = get_object_or_404(User, email=customer_email)
        profile = get_object_or_404(Profile, user_id=user.id)

        profile.premium = True
        profile.save()

    return HttpResponse(
        content=f'Webhook received: {event["type"]}',
        status=200)
