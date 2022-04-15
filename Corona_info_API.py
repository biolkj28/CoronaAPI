import json
from datetime import date, datetime, timedelta

import requests
import xmltodict

from api_exception import CheckErr, ApiException
from service_key import ServiceKey

# pos: 도, [경기, 부산, 서울, 전북, 경북, ...]
service_key = ServiceKey.corona_key


def get_corona_info(pos="경기"):
    position = pos

    # 오늘
    today = datetime.today()
    today_date = today.strftime("%Y%m%d")

    # 4일전 날짜
    pre_weeks_day = date.today() - timedelta(days=4)
    pre_weeks_day_date = pre_weeks_day.strftime('%Y%m%d')

    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    params = {'serviceKey': service_key, 'pageNo': '1', 'numOfRows': '10', 'startCreateDt': pre_weeks_day_date,
              'endCreateDt': today_date}
    try:

        response = requests.get(url, params=params)
        corona_data_dic = xmltodict.parse(response.content)

        corona_state = corona_data_dic['response']['header']['resultCode']
        CheckErr(corona_state)

    except ApiException as e:
        print(e)

    corona_data = corona_data_dic['response']['body']['items']
    result = []

    # incDec: 신규 확진자
    # defCnt: 누적 확진자
    for data in corona_data['item']:
        require_data = dict()

        if data['gubun'] == position:
            require_data['createDt'] = data['createDt']
            require_data['incDec'] = data['incDec']
            require_data['defCnt'] = data['defCnt']
            result.append(require_data)

    result = list(reversed(result))
    return result


if __name__ == "__main__":
    print(get_corona_info("전남"))
