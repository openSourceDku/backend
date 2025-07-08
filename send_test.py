import requests
# url = "127.0.0.1:8000/acounts/register/"

ACCESS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxOTk1Mzg5LCJpYXQiOjE3NTE5OTM1ODksImp0aSI6IjVjNTYyZDQxMzRiZTRhMjRhNmRmOTcyNGRlMjYxOThmIiwidXNlcl9pZCI6M30.Lo9xP8BlRSdzt14756BoJodM4eL5sP1A8kf1c3btimg"
REFRESH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjU5ODM4OSwiaWF0IjoxNzUxOTkzNTg5LCJqdGkiOiJkOTk5MDkzY2RkY2U0ODEzYmE4MjE1NGM2NjQzNTBiNCIsInVzZXJfaWQiOjN9.R5FtvbL95nyURU0-gzQO8r_vizvAsiF2D0WVq1f7W1Q"

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
    url = "http://127.0.0.1:8000/api/auth/login/"
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

def create_fixture():
    url = "http://127.0.0.1:8000/api/admin/fixtures/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
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

def update_fixture(itemId):
    url = f"http://127.0.0.1:8000/api/admin/fixtures/{itemId}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    data = {
        "name": "지우개",
        "price": 1200,
        "count": 12
    }
    response = requests.patch(url, headers=headers, json=data)
    print("비품 수정 응담 상태:", response.status_code)
    print("비품 수정 응답 내용:", response.text)

def delete_fixture(itemId):
    url = f"http://127.0.0.1:8000/api/admin/fixtures/{itemId}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    response = requests.delete(url, headers=headers)
    print("비품 삭제 응답 상태:", response.status_code)
    print("비품 삭제 응답 내용:", response.text)

def list_fixtures():
    url = "http://127.0.0.1:8000/api/admin/fixtures"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    response = requests.get(url, headers=headers)
    print("비훔 리스트 조회 응답 상태:", response.status_code)
    print("비품 리스트 조회 응답 내용:", response.text)

'''
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
'''

if __name__ == "__main__":
    # register()
    # token = login()
    # if token:
    #     item_id = create_fixture(token)
    # else:
    #     print("로그인 실패 테스트 진행 불가")
    #login()
    #create_fixture()
    #update_fixture(2)
    delete_fixture(2)