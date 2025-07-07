import requests
# url = "127.0.0.1:8000/acounts/register/"

def register() :
    url = "http://127.0.0.1:8000/api/auth/register/"
    data = {
        "username": "kimgeon",
        "password": "1234!",
        "role": "admin"
    }

    response = requests.post(url, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)

def login() :
    url = "http://127.0.0.1:8000/acounts/login/"
    data = {
        "username": "kimgeon",
        "password": "1234!",
        "role": "admin"
    }

    response = requests.post(url, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)

def refresh() :
    url = "http://127.0.0.1:8000/acounts/refresh/"
    data = {
        "refresh": 'yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjM3ODEzMCwiaWF0IjoxNzUxNzczMzMwLCJqdGkiOiJhOTQ4ODk5ZTE0Njg0YWM0YTFiZDA2ZTExZjA1MjAxOSIsInVzZXJfaWQiOjN9.zcEUZUB36FE8YrNetZl-sSc8dFrWbaUpvjIV-f5mzO0'
    }

    response = requests.post(url, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)

def logout() :
    url = "http://127.0.0.1:8000/acounts/logout/"

    refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjM3OTE1NywiaWF0IjoxNzUxNzc0MzU3LCJqdGkiOiJjMzA5MmQzNGE5NTE0Njc5YWQ0OTljOGUzYzFjOTNhNiIsInVzZXJfaWQiOjN9.QChxhEcKl7im85lP5iBlsWliTw07p-aLsCmlZdvvkNI"
    access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNzc2MTU3LCJpYXQiOjE3NTE3NzQzNTcsImp0aSI6IjFiOWM4NWYzMTlkNzQ0YmZiNjc4MTEzNzk1OWFjZjFiIiwidXNlcl9pZCI6M30.VGVjTTBVo6-uk3wf4Xp84_NgGqYdmNxjXbROTilcQ8g"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access}"
    }

    data = {
        "refresh": refresh
    }

    response = requests.post(url, headers=headers, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)

def reportsSend() :
    url = "http://127.0.0.1:8000/api/teachers/reports"

    refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjM3OTE1NywiaWF0IjoxNzUxNzc0MzU3LCJqdGkiOiJjMzA5MmQzNGE5NTE0Njc5YWQ0OTljOGUzYzFjOTNhNiIsInVzZXJfaWQiOjN9.QChxhEcKl7im85lP5iBlsWliTw07p-aLsCmlZdvvkNI"
    access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNzc2MTU3LCJpYXQiOjE3NTE3NzQzNTcsImp0aSI6IjFiOWM4NWYzMTlkNzQ0YmZiNjc4MTEzNzk1OWFjZjFiIiwidXNlcl9pZCI6M30.VGVjTTBVo6-uk3wf4Xp84_NgGqYdmNxjXbROTilcQ8g"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access}"
    }

    data = {
    # 1) 공통 메시지: 모든 학생 학부모에게 동일하게 보낼 제목·본문
    "common": {
        "subject": "중간고사 안내",
        "content": "다음 주 월요일부터 금요일까지 중간고사가 있습니다. 준비 잘 해 오세요!"
    },

    # 2) 개인 메시지: 체크된 학생 ID와 개인 메시지만
        "recipients": [
            {
            "studentId": 201,
            "personalMessage": "OO 학생, 수학 준비물 꼭 챙기세요."
            },
            {
            "studentId": 202,
            "personalMessage": "△△ 학생, 영어 단어 암기 꼭 해오도록 알려주세요."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)

register()