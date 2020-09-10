from .lucky_model import LuckyModel
from base.base_view import BaseView


class HistoryView(BaseView):

    def do_logic(self, request):
        data = self.request_params
        # count = data.get('count', None)

        lucky = LuckyModel()

        result = lucky.fetch_history_number()

        return {
            'data': result
        }
