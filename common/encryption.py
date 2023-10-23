# _*_coding: utf-8 -*-

# SHA 512 암호화

import hashlib


class encryption:
    def encrypt(self, data):
        return hashlib.sha512(data.encode("utf-8")).hexdigest()
