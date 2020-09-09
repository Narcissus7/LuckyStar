from django.conf.urls import url
from .lucky_view import LuckyView

urlpatterns = [
    url(r'^lucky-number', LuckyView.as_view(), name='lucky-number'),
]