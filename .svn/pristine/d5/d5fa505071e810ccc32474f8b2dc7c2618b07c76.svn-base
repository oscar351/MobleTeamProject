# _*_coding: utf-8 -*-

import requests

# 주소좌표 요청 API 서비스
class geoService:
    def __init__(
        self, GeoUrl, GeoService, GeoRequest, GeoCrs, GeoFormat, GeoType, GeoServiceKey
    ):
        self.GeoUrl = GeoUrl
        self.GeoService = GeoService
        self.GeoRequest = GeoRequest
        self.GeoCrs = GeoCrs
        self.GeoFormat = GeoFormat
        self.GeoType = GeoType
        self.GeoServiceKey = GeoServiceKey

    def reqGeoInfo(self, address):

        params = {
            "service": self.GeoService,
            "request": self.GeoRequest,
            "crs": self.GeoCrs,
            "address": address,
            "format": self.GeoFormat,
            "type": self.GeoType,
            "key": self.GeoServiceKey,
        }

        response = requests.get(self.GeoUrl, params=params)
        if response.status_code == 200:
            return response.json()["response"]["result"]["point"]
