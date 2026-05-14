from fastapi.testclient import TestClient

from main import app, limiter

client = TestClient(app)  # 서버를 띄우지 않고 코드 안에서 요청을 보내는 가짜 클라이언트

# FastAPI 앱 연결 확인
print(f"FastAPI 연결됨 (title={app.title}, 경로={[r.path for r in app.routes]})")
print("-" * 40)

limiter.reset()  # limiter가 메모리에 들고 있는 이전 카운트 초기화

# 1~10회: 통과해야 함 (200)
for i in range(10):
    res = client.get("/hello")
    print(i + 1, res.status_code, res.json())  # res.json(): 응답 본문 전체
    assert res.status_code == 200

# 11회째: 막혀야 함 (429)
res = client.get("/hello")
print(11, res.status_code, res.json())
assert res.status_code == 429

print("테스트 통과: 10회 허용, 11회째 차단 확인")
