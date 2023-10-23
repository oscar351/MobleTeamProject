# _*_coding: utf-8 -*-

# 패스워드를 생성 한다.

upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
lower = list("abcdefghijklmnopqrstuvwxyz")
symbol = list("!@#$%")
number = list("0123456789")

passList = [upper, lower, symbol, number]

import random as rd


class passwordGenerator:
    def generate(self, pwLen):

        # pwLen = int(length)

        passStr = ""
        for v in range(pwLen):
            n = rd.randint(0, 3)
            passStr += rd.choice(passList[n])

        return passStr
