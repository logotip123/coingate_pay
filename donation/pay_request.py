from django.conf import settings
import requests


def get_pay_url(donation_sum):
    response = requests.post('https://api-sandbox.coingate.com/v2/orders',
                             data={
                                 "price_amount": donation_sum,
                                 "price_currency": "USD",
                                 "receive_currency": "USD",
                                 "success_url": settings.SITE_URL + "success",
                                 "cancel_url": settings.SITE_URL + "cancel",
                                 "callback_url": settings.SITE_URL + "callback",
                             },
                             headers={
                                 "Authorization": settings.COINGATE_TOKEN
                             })
    try:
        if response.status_code == 200:
            return {
                "payment_url": response.json()["payment_url"],
                "payment_id": response.json()["id"],
                "token": response.json()["token"],
                "price_amount": response.json()["price_amount"],
            }
        return False
    except KeyError:
        return False