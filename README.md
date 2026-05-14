# Rate Limit 테스트

분당 10회 요청 제한(`slowapi`) 동작 확인 예제.

## 빠른 확인 — 테스트 코드

서버를 띄우지 않고 코드로 바로 확인:

```bash
pip install fastapi uvicorn slowapi httpx
python3 test_main.py > test_result.txt
```

예상 출력:

```
1~10  -> 200
11    -> 429
테스트 통과: 10회 허용, 11회째 차단 확인
```

---

## 1. 설치

```bash
pip install fastapi uvicorn slowapi
```

## 2. 서버 실행

```bash
uvicorn main:app --port 8000
```

## 3. Rate Limit 테스트

다른 터미널에서 12번 연속 요청:

```bash
for i in $(seq 1 12); do
  curl -s -o /dev/null -w "request $i -> HTTP %{http_code}\n" http://127.0.0.1:8000/hello
done
```

### 예상 결과

10회까지 `HTTP 200`, 11회째부터 `HTTP 429`:

```
request 1 -> HTTP 200
...
request 10 -> HTTP 200
request 11 -> HTTP 429
request 12 -> HTTP 429
```

`429` 응답 본문:

```json
{"error":"Rate limit exceeded: 10 per 1 minute"}
```

IP(`127.0.0.1`) 기준으로 카운트되며, 1분이 지나면 카운터가 리셋된다.
