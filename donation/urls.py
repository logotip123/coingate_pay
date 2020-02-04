from django.urls import path

from .views import GetIndex, Success, Cancel, Callback


app_name = "donation"

urlpatterns = [
    path('', GetIndex.as_view(), name="index"),
    path('success', Success.as_view(), name="success"),
    path('cancel', Cancel.as_view(), name="cancel"),
    path('callback', Callback.as_view(), name="callback"),
]