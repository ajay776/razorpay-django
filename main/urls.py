# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('index/', index, name="index"),

#     path('', app, name="app"),
# ]


# myapp/urls.py

# from django.urls import path
# from .views import PaymentView, PaymentResponseView

# urlpatterns = [
#     path('payment/', PaymentView.as_view(), name='payment'),
#     path('payment/response/', PaymentResponseView.as_view(),
#          name='payment_response'),
# ]


from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("payment/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),
]
