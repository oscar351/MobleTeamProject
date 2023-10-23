# _*_coding: utf-8 -*-

# 메일 전송 서비스

import smtplib
from email.mime.text import MIMEText


class mailService:
    def __init__(self, smtpTrustValue, smtpTrustPort, smtpPassword, smtpLogin):
        self.smtpTrustValue = smtpTrustValue
        self.smtpTrustPort = smtpTrustPort
        self.smtpPassword = smtpPassword
        self.smtpLogin = smtpLogin

    def sendMail(self, recver, subject, message):
        # 세션 생성
        s = smtplib.SMTP(self.smtpTrustValue, int(self.smtpTrustPort))

        # TLS 보안 시작
        s.starttls()

        # 로그인 인증
        s.login(self.smtpLogin, self.smtpPassword)

        # 보낼 메시지 설정
        msg = MIMEText(message)
        msg["Subject"] = subject

        # 메일 보내기
        s.sendmail(self.smtpLogin, recver, msg.as_string())

        # 세션 종료
        s.quit()
