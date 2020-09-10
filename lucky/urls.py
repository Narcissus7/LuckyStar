from django.conf.urls import url
from .lucky_view import LuckyView
from .history_view import HistoryView

urlpatterns = [
    url(r'^lucky-number', LuckyView.as_view(), name='lucky-number'),
    url(r'^history-number', HistoryView.as_view(), name='history-number'),
]