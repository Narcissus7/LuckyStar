import random
import requests
import json
import redis
from typing import List
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
    def fetch_history_number(self, num=5) -> List:
        # url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=%s' % num
        #
        # res = requests.get(url, headers=HEADERS)
        # print(res.status_code)
        # print(res.text)
        # print(type(res.text))
        # if res.text:
        #     print(json.loads(res.text))
        res_text = '''
            {
            "state":0,
            "message":"查询成功",
            "pageCount":1,
            "countNum":0,
            "Tflag":0,
            "result":[{
                "name":"双色球",
                "code":"2020087",
                "detailsLink":"/c/2020-09-08/473855.shtml",
                "videoLink":"/c/-08/473854.shtml",
                "date":"2020-09-08(二)",
                "week":"二",
                "red":"11,15,20,23,25,33",
                "blue":"10",
                "blue2":"",
                "sales":"351393474",
                "poolmoney":"1066743130",
                "content":"北京1注,山东1云南1注,陕西1注,共5注。",
                "addmoney":"",
                "addmoney2":"",
                "msg":"",
                "z2add":"",
                "m2add":"",
                "prizegrades":[
                    {"type":1,"typenum":"5","typemoney":"7940558"},
                    {"type":2,"typenum":"44",y":"417692"},
                    {"type":3,"typenum":"1430","typemoney":"3000"},
                    {"type":4,"typenum":"67064","typemoney":"200"},
                    {"type":5,"typenum":"1248566","typemoney":"10"},
                    {"type":6,"typenum":"13696077","typemoney":"5"},
                    {"type":7,"typenum":"","typemoney":""}
                ]},
                
                {"name":"双色球","code":"2020086","detailsLink":"/c/2020-09-06/473745.shtml","videoLink":"/c/2020-09/473744.shtml","date":"2020-09-06(日)","week":"日","red":"02,04,06,15,24,27","blue":"06","blue2":"","sales":"383150704","poolmoney":"1051310454","content":"黑龙江2注,福建1注广东1注,广西1注,宁夏1注,共7注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typenum":"7","typemoney":"7452652"},{"type":2,"typenupemoney":"183424"},{"type":3,"typenum":"1870","typemoney":"3000"},{"type":4,"typenum":"91887","typemoney":"200"},{"type":5,"typenum":"1703740","typemoney":"10"},{"type":6,"typenum":"12175241","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]},{"name":"双色球","code":"2020085","detailsLink":"/c/2020-09-03/473632.shtml","videoLink":"/c/2-09-03/473631.shtml","date":"2020-09-03(四)","week":"四","red":"01,02,05,09,19,24","blue":"16","blue2":"","sales":"349243256","poolmoney":"1039096893","content":"江苏1注,安1注,共3注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typenum":"3","typemoney":"10000000"},{"type":2,"typenum":"135","typemoney75949"},{"type":3,"typenum":"1659","typemoney":"3000"},{"type":4,"typenum":"78797","typemoney":"200"},{"type":5,"typenum":"1363570","typemoney":"10"},{"type":6,"typenum":"8348914","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]},{"name":"双色球","code":"2020084","detailsLink":"/c/2020-09-01/473522.shtml","videoLink":"/c/2020-09-01/471.shtml","date":"2020-09-01(二)","week":"二","red":"03,07,16,17,23,30","blue":"07","blue2":"","sales":"340223360","poolmoney":"997837500","content":"北京1注,山西2注,内蒙古1,浙江1注,安徽1注,福建1注,山东1注,河南1注,湖北1注,四川1注,云南1注,陕西1注,共15注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typ5"},{"type":2,"typenum":"265","typemoney":"45386"},{"type":3,"typenum":"3166","typemoney":"3000"},{"type":4,"typenum":"127083","typemoney":"200"},{"type":5,"typenum":"1845213","typemoney":"10"},{"type":6,"typenum":"13046559","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]},{"name":"双色球","code":"2020083","detailsLink":"/c/2020-08-373412.shtml","videoLink":"/c/2020-08-30/473411.shtml","date":"2020-08-30(日)","week":"日","red":"01,19,25,26,30,31","blue":"12","blue2":"","sales":"375628538","poolmoney":"46377044","content":"吉林1注,江苏1注,福建1注,河南1注,广东2注,甘肃1注,共7注。","addmoney":"","addmoney2":"","msg":"","z2add":"","m2add":"","prizegrades":[{"type":1,"typenum"6189"},{"type":2,"typenum":"96","typemoney":"265798"},{"type":3,"typenum":"1266","typemoney":"3000"},{"type":4,"typenum":"63131","typemoney":"200"},{"type":5,"typenum":"1192139","typemoney":"10"},{"type":6,"typenum":"10729153","typemoney":"5"},{"type":7,"typenum":"","typemoney":""}]}]
            }
        '''
        # print(json.loads(res_text))
        return [{
            "code": "2020087",
            "date": "2020-09-08(二)",
            "number": "11,15,20,23,25,33".split(',') + ["10"],
        }]

