import random
import requests
import json
import redis
from typing import List
from itool import redis_helper
HISTORY_NUMBER_KEY = 'history_number_data'
HEADERS = {
    'Accept': 'application/json;text/javascript;*/*;q=0.01',
    # 'Accept': 'application/json;charset=utf-8;',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '_ga=GA1.3.1698897776.1599634932; _gid=GA1.3.874786695.1599739256; _gat_gtag_UA_113065506_1=1'
}


class LuckyModel:
    @staticmethod
    def random_lucky_number(total_count: int, result_count: int) -> List:
        """
        :param total_count: 总数
        :param result_count: 随机n个数
        :return: 结果
        """
        elements = [x + 1 for x in range(total_count)]
        lucky_number = []
        for i in range(result_count):
            number = elements[random.randint(0, len(elements) - 1)]
            elements.remove(number)
            lucky_number.append(number)

        lucky_number.sort()
        lucky_number = ['0' + str(x) if x < 10 else str(x) for x in lucky_number]

        return lucky_number

    # def get_one_lucky_number(self) -> List:
    #     result = self.random_lucky_number(33, 6) + self.random_lucky_number(16, 1)
    #     return result

    def get_several_lucky_number(self, count=5) -> List:
        result = []
        for i in range(count):
            lucky_number = self.random_lucky_number(33, 6) + self.random_lucky_number(16, 1)
            result.append(lucky_number)
        return result

    # 获取往期中奖号码
    def fetch_history_number(self, num=1) -> List:
        cache = redis_helper.get_redis_helper()

        cache_data = cache.get(cache.get(HISTORY_NUMBER_KEY))
        if cache_data:
            result = self.resolve_fetch_data(cache_data)
            return result

        url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=%s' % num

        print('no cache data')
        data = requests.get(url, headers=HEADERS)
        if not data.text:
            return []

        result = self.resolve_fetch_data(data.text)

        cache.set(HISTORY_NUMBER_KEY, data.text)
        cache.expire(HISTORY_NUMBER_KEY, 300)  # 1h
        return result

    # 解析数据
    def resolve_fetch_data(self, data: str) -> List:
        j_data = json.loads(data)

        result = []

        for x in j_data.get('result', []):
            result.append({
                'code': x['code'],
                'date': x['date'],
                'number': x['red'].split(',') + [x['blue']]
            })

        return result



