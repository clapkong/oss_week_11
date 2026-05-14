from datetime import datetime

from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

app = FastAPI()  # FastAPI: 웹 앱 객체 생성

# Rate Limit
limiter = Limiter(key_func=get_remote_address) # get_remote_address: 요청에서 IP를 꺼내 IP별로 횟수를 셈
app.state.limiter = limiter  # 앱에 limiter 등록
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # 제한 초과(RateLimitExceeded)시 429 응답(_rate_limit_exceeded_handler) 연결

# GET 요청
@app.get("/hello")
@limiter.limit("10/minute") # IP 당 1분에 10회 초과면 RateLimitExceeded
async def hello(request: Request):
    now = datetime.now().strftime("%H:%M:%S")
    return {"message": "hello", "time": now}  # 통과 시 응답 본문 (시각 포함)
