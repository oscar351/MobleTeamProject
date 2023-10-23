# _*_coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import urllib
import json

import sys

# 날씨 요청 API 서비스
class weatherService:
    def __init__(self, apiUrl, serviceKey, nowOfRows, pageNo, dataType):
        self.apiUrl = apiUrl
        self.serviceKey = serviceKey
        self.numOfRows = nowOfRows
        self.pageNo = pageNo
        self.dataType = dataType

    def reqWeatherInfo(self, base_date, base_time, nx, ny):

        # print('base_date : ' + base_date + ', base_time : ' + base_time + ', nx : ' + nx + ', ny : ' + ny, file=sys.stderr)

        params = "?" + urlencode(
            {
                # "serviceKey" : unquote(self.serviceKey),
                "serviceKey": self.serviceKey,
                "numOfRows": str(self.numOfRows),
                "pageNo": str(self.pageNo),
                "dataType": self.dataType,
                "base_date": base_date,
                "base_time": base_time,
                "nx": str(nx),
                "ny": str(ny),
            }
        )

        req = urllib.request.Request(self.apiUrl + params)
        response = urlopen(req).read()
        # print('weather : ' + response.decode('utf-8'), file=sys.stderr)
        data = json.loads(response.decode("utf-8"), encoding="utf-8")
        return data["response"]["body"]["items"]["item"]
