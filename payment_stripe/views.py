import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from .models import StripePaymentLink, Product
from datetime import datetime
import json

# Initialize Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_payment_link(request, product_id):
    print(f'in create_payment_link')
    selected_payment_method = request.POST.get('payment_method', 'card')
    
    # Ensure only allowed payment methods are used
    allowed_payment_methods = ['card', 'wechat_pay', 'alipay']
    if selected_payment_method not in allowed_payment_methods:
        return HttpResponse("Invalid payment method", status=400)
    
    # Define payment method options
    payment_method_options = {}
    if selected_payment_method == 'wechat_pay':
        payment_method_options = {
            'wechat_pay': {
                'client': 'web'
            }
        }
    elif selected_payment_method == 'alipay':
        payment_method_options = {
            'alipay': {}
        }
    
    try:
        product = Product.objects.get(id=product_id)

        # Create a new payment link
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[selected_payment_method],  # Use selected payment method
            payment_method_options=payment_method_options,  # Set payment method options
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),  # amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payments/success/'),
            cancel_url=request.build_absolute_uri('/payments/cancel/'),
        )
        print(f'checkout_session: {checkout_session}')

        # Save the payment link info to the database
        StripePaymentLink.objects.create(
            user=request.user,
            product=product,
            checkout_session_id=checkout_session.id,
            payment_intent=checkout_session.payment_intent,
            status=checkout_session.payment_status,
            amount_total=checkout_session.amount_total / 100,
            currency=checkout_session.currency,
            payer_email=request.user.email,
            payer_name=request.user.get_full_name(),
            payment_method=selected_payment_method,
        )
        
        return redirect(checkout_session.url)
    
    except Exception as e:
        return HttpResponse(str(e), status=500)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        checkout_session_id = session['id']
        print(f'session {session}')
        try:
            StripePaymentLink.objects.filter(checkout_session_id=checkout_session_id).update(
                payment_intent=session.get('payment_intent', ''),
                status=session.get('status', ''),
                amount_total=session.get('amount_total', 0) / 100,
                currency=session.get('currency', ''),
                payer_email=session.get('customer_details', {}).get('email', ''),
                payer_name=session.get('customer_details', {}).get('name', ''),
                created=datetime.fromtimestamp(session.get('created', '')),
            )

        except StripePaymentLink.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'}, status=200)

@login_required
def payment_succeed(request):
    return render(request, 'payment_stripe/success.html')

@login_required
def payment_cancelled(request):
    return render(request, 'payment_stripe/cancelled.html')