from flask import abort, request
from flask import Flask

app = Flask(__name__)

#### 특정 IP에 대해서만 접속을 허용한다 추후 해외 IP 차단 구현예정####
@app.before_request
def limit_overseas_addr():
    # if request.remote_addr != "192.168.0.1":
    #    abort(403)  # Forbidden
    return
