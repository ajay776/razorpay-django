from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# # Create your views here.


# def index(request):

#     context = {"demo": "data"}
#     import razorpay

#     if request.method == "POST":
#         import pdb
#         pdb.set_trace()
# client = razorpay.Client(
#     auth=("key_id", "key_secret"))

#         data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}
#         payment = client.order.create(data=data)

#     return render(request, "index.html", payment)


# def app(request):

#     return render(request, "app.html")

# # @csrf_exempt
# # def webhook_handler(request):
# #     payload = request.body

# #     print("----------------------------------------------", payload)
# #     return HttpResponse(status=200)


# myapp/views.py


# myapp/views.py

# from django.shortcuts import render, redirect
# from django.views import View
# from django.conf import settings
# import razorpay
# from .models import Order


# class PaymentView(View):
#     def get(self, request):
#         return render(request, 'payment_form.html')

#     def post(self, request):
#         amount = int(request.POST.get('amount')) * 100  # Convert to paise
#         client = razorpay.Client(
#             auth=("key_id", "key_secret"))
#         payment_data = {
#             'amount': amount,
#             'currency': 'INR',
#             'receipt': 'order_rcptid_11',
#             'payment_capture': 1,
#         }
#         import pdb
#         pdb.set_trace()
#         payment = client.order.create(data=payment_data)
#         order = Order.objects.create(
#             amount=amount / 100, payment_id=payment['id'])

#         return render(
#             request,
#             'payment_form.html',
#             {'order': order, 'razorpay_key': "key_id"},
#         )


# class PaymentResponseView(View):
#     def post(self, request):
#         payment_id = request.POST.get('razorpay_payment_id')
#         order_id = request.POST.get('razorpay_order_id')
#         signature = request.POST.get('razorpay_signature')

#         client = razorpay.Client(
#             auth=("key_id", "key_secret"))

#         params_dict = {
#             'razorpay_order_id': order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature,
#         }

#         try:
#             client.utility.verify_payment_signature(params_dict)
#             order = Order.objects.get(payment_id=order_id)
#             order.payment_id = payment_id
#             order.save()
#             return render(request, 'payment_success.html', {'order': order})
#         except Exception as e:
#             return render(request, 'payment_failure.html', {'error': str(e)})

import razorpay

from .models import Order
from .constants import PaymentStatus
import json


def home(request):
    return render(request, "index.html")


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(
            auth=("key_id", "key_secret"))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR",
             "payment_capture": "1"}
        )
        # print("-------------------------------------", ra)
        import pdb
        # pdb.set_trace()
        order = Order.objects.create(
            # payment_order["id"]
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": "key_id",
                "order": order,
            },
        )
    return render(request, "payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(
            auth=("key_id", "key_secret"))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get(
            "error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})
