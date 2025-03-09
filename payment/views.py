import requests
import json

from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse

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

    order=get_object_or_404(Order,zarinpal_authority=payment_authority)
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
    
def payment_process_sandbox(request):

    # Get order id from session
    order_id=request.session.get('order_id')
    
    # Get the order object
    order=get_object_or_404(Order,id=order_id)

    toman_total_price=order.get_total_price()
    rial_total_price=toman_total_price*10

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
		'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
		'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }
    
    res=requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    
    print(f'res json process={res.json()}') # just for test
    data=res.json()['data']
    print(f'res.json[data]={data}')

    authority=data['authority']
    order.authority=authority
    order.save()

    if 'errors' not in data or len(data['errors'])==0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback_sandbox(request):
    
    payment_authority=request.GET.get('Authority')
    payment_status=request.GET.get('Status')

    order=get_object_or_404(Order,zarinpal_authority=payment_authority)
    toman_total_price=order.get_total_price()
    rial_total_price=toman_total_price*10

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
        print(f'res json callback={res.json()}')
        print(f'res json[data] callback={res.json()["data"]}')

        if 'errors' not in res.json()['data'] or len(res.json()['data']['errors']==0):
            data=res.json()['data']
            payment_code=data['code']

            if payment_code==100:
                order.is_paid=True
                order.ref_id=data['ref_id']
                order.data=data
                order.save()

                return HttpResponse('Your payment was successful.')
            elif payment_code==101:
                return HttpResponse('Your payment was successful. However, this transaction has already recorded.')
            else:
                error_code=res.json()['data']['errors']['code']
                error_message=res.json()['data']['errors']['messages']
                # you can write a code that prevents the cart from emptying.
                   
                return HttpResponse(f'The transaction was unsuccessful.{error_code:} {error_message}')
               
    else:
        # you can write a code that prevents the cart from emptying.
        return HttpResponse(f'The transaction was unsuccessful.')



def payment_process_omannet(request):
    pass

def  payment_callback_omannet(request):
    pass
