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

#logout()

def create_fixture(access_token):
    url = "http://127.0.0.1:8000/fixtures"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "name": "마커펜",
        "price": 2000,
        "count": 10
    }
    response = requests.post(url, headers=headers, json=data)
    print("비품 등록 응답 상태:", response.status_code)
    print("비품 등록 응담 내용", response.text)
    if response.status_code == 201:
        return response.json().get("itemId")
    return None

def update_fixture(access_token, itemId):
    url = "http://127.0.0.1:8000/fixtures/{itemId}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "name": "지우개",
        "price": 1200,
        "count": 12
    }
    response = requests.patch(url, headers=headers, json=data)
    print("비품 수정 응담 상태:", response.status_code)
    print("비품 수정 응답 내용:", response.text)

def delete_fixture(access_token, itemId):
    url = "http://127.0.0.1:8000/fixtures/{itemId}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.delete(url, headers=headers)
    print("비품 삭제 응답 상태:", response.status_code)
    print("비품 삭제 응답 내용:", response.text)

def list_fixtures(access_token):
    url = "http://127.0.0.1:8000/fixtures"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print("비훔 리스트 조회 응답 상태:", response.status_code)
    print("비품 리스트 조회 응답 내용:", response.text)

#전체 테스트 실행
if __name__ == "__main__":
    register()
    access_token = login()
    if access_token:
        #비품등록
        itemId = create_fixture(access_token)
        #비품리스트조회
        list_fixtures(access_token)
        #비품 수정
        if itemId:
            update_fixture(access_token, itemId)
            #비품삭제
            delete_fixture(access_token, itemId)
        list_fixtures(access_token) #비품 리스트 재조회
    else:
        print("로그인 실패로 비품관리 테스트 진행할 수 없습니다.")