from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View

from .forms import PayForm
from .pay_request import get_pay_url
from .models import Payment


class GetIndex(View):
    form_class = PayForm
    initial = {'key': 'value'}
    template_name = 'donation/donation.html'
    payments = Payment.objects.filter(Q(status="S") | Q(status="N")).all()

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form,
                                                    "payments": self.payments})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            payment_info = get_pay_url(form.cleaned_data["donation"])
            if payment_info:
                url = payment_info["payment_url"]
                Payment(payment_id=payment_info["payment_id"],
                        token=payment_info["token"],
                        price_amount=payment_info["price_amount"]).save()
                return HttpResponseRedirect(url)
            messages.warning(request, "Something wrong, try again")
        return render(request, self.template_name, {"form": form,
                                                    "payments": self.payments})


class Success(View):
    def get(self, request):
        messages.success(request, "The payment was successful")
        return redirect(reverse("donation:index"))


class Cancel(View):
    def get(self, request):
        messages.error(request, "Payment error")
        return redirect(reverse("donation:index"))


class Callback(View):
    def post(self, request):
        payment = Payment.objects.filter(token=request.POST["token"]).first()
        if payment:
            payment.status = request.POST["status"][0]
            payment.save()