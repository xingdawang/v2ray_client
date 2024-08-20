import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PayPalOrder, Product

def get_access_token():
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]

@login_required
def create_order(request, product_id):
    product = Product.objects.get(id=product_id)
    access_token = get_access_token()
    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "EUR",
                "value": str(product.price)
            }
        }],
        "application_context": {
            "return_url": request.build_absolute_uri(f'/payments/capture/{product_id}/'),
            "cancel_url": request.build_absolute_uri('/payments/cancel/')
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    order = response.json()

    # Save the order to the database with the current user
    PayPalOrder.objects.create(
        user=request.user,
        order_id=order["id"],
        status=order["status"],
        amount=product.price,
        currency="EUR"
    )

    approval_url = next(link["href"] for link in order["links"] if link["rel"] == "approve")
    return redirect(approval_url)

@login_required
def capture_order(request, product_id):
    order_id = request.GET.get('token')  # The token returned by PayPal after user approval
    access_token = get_access_token()
    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    capture_response = response.json()

    # Extract details from the capture response
    capture = capture_response.get('purchase_units', [{}])[0].get('payments', {}).get('captures', [{}])[0]
    gross_amount = capture.get('seller_receivable_breakdown', {}).get('gross_amount', {}).get('value', '0.00')
    paypal_fee = capture.get('seller_receivable_breakdown', {}).get('paypal_fee', {}).get('value', '0.00')
    net_amount = capture.get('seller_receivable_breakdown', {}).get('net_amount', {}).get('value', '0.00')
    create_time = capture.get('create_time', '')
    status = capture.get('status', '')

    # Update or create the order record with the additional details
    PayPalOrder.objects.filter(order_id=order_id).update(
        status=capture_response.get('status', ''),
        payer_email=capture_response.get('payer', {}).get('email_address', ''),
        payer_name=f"{capture_response.get('payer', {}).get('name', {}).get('given_name', '')} {capture_response.get('payer', {}).get('name', {}).get('surname', '')}",
        gross_amount=gross_amount,
        paypal_fee=paypal_fee,
        net_amount=net_amount,
        capture_create_time=create_time,
        capture_status=status
    )

    # Redirect to the profile page after payment
    return redirect('/profile')

@login_required
def cancel_payment(request):
    return render(request, 'payments/cancel.html')
