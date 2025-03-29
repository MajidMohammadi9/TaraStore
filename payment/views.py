import requests
import json

from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.utils.translation import gettext as _

from orders.models import Order

def payment_process(request):
    # Get order id from session
    order_id=request.session.get('order_id')
    # Get the order object
    order=get_object_or_404(Order, id=order_id)

    toman_total_price=order.get_total_price()
    rial_total_price=toman_total_price*10

    zarinpal_request_url='https://api.zarinpal.com/pg/v4/payman/request.json'

    request_header={
        "accept":"application/json",
        "content-type":"application/json",
    }

    request_data={
        'merchat_id':settings.ZARINPAL_MERCHANT_ID,
        'amount':rial_total_price,
        'description':f'#{order.id}: {order.customer.full_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback'))
    }

    res=requests.post(url=zarinpal_request_url,data=json.dumps(request_data),headers=request_header)

    # print(f'res_Json={res.json()['data']}')
    data=res.json()['data']
    authority=data['authority']

    order.authority=authority
    order.save()

    if 'errors' not in data or len(data['errors'])==0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')
    
def payment_callback(request):
    payment_authority=request.GET.get('Authority')
    payment_status=request.GET.get('Status')

    order=get_object_or_404(Order, authority=payment_authority)
    toman_total_price=order.get_total_price()
    rial_total_price=toman_total_price*10

    if payment_status=='OK':
        request_header={
            "accept":"application/json",
            "content-type":"application/json",
        }

        request_data={
            'merchant_id':settings.ZARINPAL_MERCHANT_ID,
            'amount':rial_total_price,
            'authority':payment_authority,
        }

        res=requests.post(
            url='https://api.zarinpal.com/pg/v4/payman/verify.json',
            data=request_data,
            headers=request_header,
        )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors'])==0):
            data=res.json()['data']
            payment_code=data['code']

            if payment_code==100:
                order.status=settings.ORDER_STATUS_PAID
                order.ref_id=data['ref_id']
                order.data=data
                order.save()

                return HttpResponse('your payment was successful.')
            elif payment_code==101:
                return HttpResponse('Your payment was successful however this transaction has already recorded.')
            else:
                error_code=res.json()['errors']['code']
                error_message=res.json()['errors']['messages']
                # you can write a code that prevents the cart from emptying.
                return HttpResponse(f'The transaction was unsuccessful. {error_code:} {error_message}')
            
    else:
          # you can write a code that prevents the cart from emptying.
          return HttpResponse(f'The transaction was unsuccessful.{error_code:} {error_message}')
    
def payment_sandbox_zarinpal(request):

    # Get order id from session or from request (in my_orders.html if unpaid)
    order_id = request.POST.get("order_id") or request.session.get("order_id")
    
    # Get the order object
    order=get_object_or_404(Order,id=order_id)

    total_price=order.get_total_price()
    rial_total_price=total_price*920000

    # zarinpal_request_url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymanRequest.json'
    zarinpal_request_url='https://sandbox.zarinpal.com/pg/v4/payment/request.json'

    request_header={
		"accept":"application/json",
		"content-type":"application/json",
    }

    request_data={
		# 'merchant_id':'87f01487-b706-47a3-97af-49fc1420d97b',
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
		'amount': rial_total_price,
		'description': f'#{order.id}: {order.customer.full_name}',
		'callback_url': request.build_absolute_uri(reverse('payment:callback_zarinpal')),
    }
    
    res=requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    
    # print(f'res json process={res.json()}') # just for test
    data=res.json()['data']
    # print(f'res.json[data]={data}')

    authority=data['authority']
    order.authority=authority
    order.save()

    if 'errors' not in data or len(data['errors'])==0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def callback_sandbox_zarinpal(request):
    
    payment_authority=request.GET.get('Authority')
    payment_status=request.GET.get('Status')

    order=get_object_or_404(Order, authority=payment_authority)
    total_price=order.get_total_price()
    rial_total_price=total_price*920000

    if payment_status=='OK':
        
        request_header={
            "accept":"application/json",
            "content-type":"application/json",
        }

        request_data={
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount':rial_total_price,
            'authority':payment_authority,
        }

        res=requests.post(
            # url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymanVerification.json',
            url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
            )
        # print(f'res json callback={res.json()}')
        # print(f'res json[data] callback={res.json()["data"]}')

        if 'errors' not in res.json()['data'] or len(res.json()['data']['errors']==0):
            data=res.json()['data']
            payment_code=data['code']

            if payment_code==100:
                order.status=settings.ORDER_STATUS_PAID
                order.ref_id=data['ref_id']
                order.data=data
                order.save()

                # return HttpResponse('Your payment was successful.')
                messages.success(request, _('Your payment was successful.'))
                return redirect('home')
            elif payment_code==101:
                # return HttpResponse('Your payment was successful. However, this transaction has already recorded.')
                messages.success(request, _('Your payment was successful. However, this transaction has already recorded.'))
                return redirect('home')
            else:
                error_code=res.json()['data']['errors']['code']
                error_message=res.json()['data']['errors']['messages']
                # you can write a code that prevents the cart from emptying.
                   
                # return HttpResponse(f'The transaction was unsuccessful.{error_code:} {error_message}')
                messages.error(request, _(f'The transaction was unsuccessful.{error_code:} {error_message}'))
                return redirect('home')
    else:
        # you can write a code that prevents the cart from emptying.
        # return HttpResponse(f'The transaction was unsuccessful.')

        messages.error(request, _('The transaction was unsuccessful.'))
        return redirect('home')
    

def payment_sandbox_paypal(request):
    """ Initiates a PayPal sandbox payment """

    # Get order id from session or from request (in my_orders.html if unpaid)
    order_id = request.POST.get("order_id") or request.session.get("order_id")
    order=get_object_or_404(Order, id=order_id)
    total_price=order.get_total_price()

    currency = "USD"

    # PayPal API authentication
    auth_response = requests.post(
        f"{settings.PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )

    if auth_response.status_code == 200:
        access_token = auth_response.json()["access_token"]
        if not access_token:
            messages.error(request, _('Failed to retrieve access token'))
            return redirect('home')
            # return JsonResponse({"error": "Failed to retrieve access token"}, status=401)
        
        # Create a PayPal order
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [{"amount": {"currency_code": currency, "value": total_price}}],
            "application_context": {
                "return_url": request.build_absolute_uri(reverse("payment:callback_paypal")),
                "cancel_url": request.build_absolute_uri(reverse("home")),
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        order_response = requests.post(
            f"{settings.PAYPAL_API_BASE}/v2/checkout/orders",
            json=order_data,
            headers=headers,
        )

        if order_response.status_code == 201:
            order_info = order_response.json()
            order.authority=order_info['id']
            order.save()
            approval_url = next(link["href"] for link in order_info["links"] if link["rel"] == "approve")
            return redirect(approval_url)
    else:
        messages.error(request, _('Authentication failed with PayPal'))
        return redirect('home')
        # return JsonResponse({"error": "Authentication failed with PayPal"}, status=401)

    messages.error(request, _('Unable to create PayPal order'))
    return redirect('home')
    # return JsonResponse({"error": "Unable to create PayPal order"}, status=400)


def callback_sandbox_paypal(request):
    token = request.GET.get("token")
    order=get_object_or_404(Order, authority=token)

    if not token:
        messages.error(request, _('Invalid request'))
        return redirect('home')
        # return JsonResponse({"error": "Invalid request"}, status=400)

    # PayPal API authentication
    auth_response = requests.post(
        f"{settings.PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )

    if auth_response.status_code == 200:
        access_token = auth_response.json()["access_token"]

        # Capture the PayPal order
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        capture_response = requests.post(
            f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{token}/capture",
            headers=headers,
        )

        capture_data = capture_response.json()

        if capture_response.status_code == 201:
            order.status=settings.ORDER_STATUS_PAID
            order.ref_id=capture_data.get('payer', {}).get('payer_id')
            order.save
            order.data=capture_data
            order.save()

            messages.success(request, _('Payment captured successfully'))
            return redirect('home')
            # return JsonResponse({"success": "Payment captured successfully"})
        
        elif capture_response.status_code == 400 and capture_data.get("name") == "ORDER_ALREADY_CAPTURED":
            messages.error(request, _('This order has already been captured'))
            return redirect('home')
            # return JsonResponse({"error": "This order has already been captured"}, status=400)
    else:
        messages.error(request, _('Authentication failed'))
        return redirect('home')
        # return JsonResponse({"error": "Authentication failed"}, status=401)
    
    messages.error(request, _('Payment capture failed'))
    return redirect('home')
    # return JsonResponse({"error": "Payment capture failed"}, status=400)
