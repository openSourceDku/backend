import requests
# url = "127.0.0.1:8000/acounts/register/"

def register() :
    url = "http://127.0.0.1:8000/acounts/register/"
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

register()