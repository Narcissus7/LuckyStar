from .lucky_model import LuckyModel
from base.base_view import BaseView


class LuckyView(BaseView):

    def do_logic(self, request):
        data = self.request_params
        count = data.get('count', None)

        lucky = LuckyModel()

        if count:
            result = lucky.get_several_lucky_number(count)
        else:
            result = lucky.get_several_lucky_number()

        return {
            'data': result
        }
