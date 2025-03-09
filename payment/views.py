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
        # 'callback_url': request.build_absolute_uri(reverse('payment:payment_callback'))
        'callback_url':'127.0.0.1:8000'
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
