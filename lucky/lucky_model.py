import random
from typing import List


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
        print(result)
        return result


lucky = LuckyModel()
lucky.get_several_lucky_number(1)
