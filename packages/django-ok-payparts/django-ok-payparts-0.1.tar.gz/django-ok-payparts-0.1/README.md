# django-ok-payparts

Simple django integration for API "Оплата Частями в Интернете": [Схема взаимодействия №1 (Создание платежа по сервису Оплата частями/Мгновенная рассрочка)](https://bw.gitbooks.io/api-oc/content/pay.html)

## Installation

Install with pip:

```shell
$ pip install django-ok-payparts
```

Update INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'payparts',
    ...
]
```

Add `payparts.urls` to your project urlpatterns:

```python
urlpatterns = [
    ...
    path('', include('payparts.urls')),
    ...
]
```

Make migrations
```shell
$ python manage.py migrate
```

### Available settings

`PAYPARTS_API_PASSWORD` - Password of your store.

`PAYPARTS_API_STORE_ID` - Your store's ID.

`PAYPARTS_API_URL` - Url for creation of a payment. By default: `https://payparts2.privatbank.ua/ipp/v2/`.

`PAYPARTS_API_REDIRECT_URL` - Url to redirect after a success payment. By default: `https://payparts2.privatbank.ua/ipp/v2/payment`.

### Usage

#### How to create a payment

1. Prepare your order's data:

```python
data = {
    "order_id": f"order-123",
    "amount": 400.00,
    "parts_count": 2,  # optional, default value is '2'
    "merchant_type": "II",  # optional, default value is 'II'
    "products": [
        {
            "name": "Телевизор",
            "count": 2,
            "price": 100.00
        },
        {
            "name": "Микроволновка",
            "count": 1,
            "price": 200.00
        }
    ],
    # also optional fields (can be set in your cabinet):
    "response_url": "http://shop.com/response",  
    "redirect_url": "http://shop.com/redirect",
}
```

2. Get your redirect url:

```python
from payparts.use_cases import GetRedirectUrlUseCase

redirect_url = GetRedirectUrlUseCase().execute(data)
```

3. Redirect a user to the url.

#### How to process a callbalk

Whenever a callback is processed a signal will be sent with the result of the transaction.

There are two signals (`payparts.signals`):

1) `pay_parts_success_callback` - if signature is valid.
2) `pay_parts_invalid_callback` - if signature is not valid.

Connect the signals to actions to perform the needed operations when a successful payment is received:

```python
from payparts.signals import pay_parts_success_callback, pay_parts_invalid_callback

from orders.models import Order


def success_callback(sender, log, request, **kwargs):
    # ensure success state
    if log.is_success:
        order = Order.objects.get(pk=log.order_id)
        order.set_success_payment_state()

pay_parts_success_callback.connect(success_callback)

```