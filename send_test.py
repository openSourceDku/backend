import requests
# url = "127.0.0.1:8000/acounts/register/"

ACCESS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMDYxMTU2LCJpYXQiOjE3NTIwNTczNjcsImp0aSI6IjU4Njg0ODgwODY0MDQ3M2M5OTJiYTIwNTNjZTlhODM2IiwidXNlcl9pZCI6M30.t1PdkKsEmc0F7seiwrndw0bwWDrIuCdwJI8vrWgn_Sg"
REFRESH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjY2NDE1NiwiaWF0IjoxNzUyMDU5MzU2LCJqdGkiOiJiNTQwOGQ1ZmJlZTQ0NzIwYThhM2IwYmQ2ODU2MGQzYSIsInVzZXJfaWQiOjN9.-dcSpTsJSeqamdf9nIxJUCJCf2tbjEOL5UUW2qGd0jU"
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

def create_fixture(access_token):
    url = "http://127.0.0.1:8000/fixtures"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "name": "노트북",
        "price": 1200000,
        "count": 3
    }
    response = requests.post(url, headers=headers, json=data)
    print("비품 등록 응답 상태:", response.status_code)
    print("비품 등록 응답 내용", response.text)
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
        "name": "노트북",
        "price": 1000000,
        "count": 2
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

# def create_teacher():
#     url = "http://127.0.0.1:8000/api/admin/teachers/"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {ACCESS}"
#     }
#     data = {
#         "teacher_name": "김선생",
#         "age": 29,
#         "position": "수석 교사",
#         "sex": "M"
#     }
#     response = requests.post(url, headers=headers, json=data)
#     print("선생님 등록 응답 상태:", response.status_code)
#     print("선생님 등록 응답 내용", response.text)
#     if response.status_code == 201:
#         return response.json().get("teacher_id")
#     return None

def create_sudent(teacher_id, passwd):
    url = f"http://127.0.0.1:8000/api/students/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    data = {

        'teacher_id':teacher_id,
        "passwd": passwd,
        "class_id": 101,
        "name": "홍길동",
        "email": "hong@naver.com",
        "birth_date": 20001010,
        "gender": "male"
    }
    response = requests.post(url, json=data, headers=headers)
    print("학생 등록 응답 상태:", response.status_code)
    print("학생 등록 응답 내용", response.text)
    if response.status_code == 201:
        return response.json().get("class_id")
    return None


def list_students():
    url = f"http://127.0.0.1:8000/api/students/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    response = requests.get(url, headers=headers)
    print("학생 목록조회 응답 상태:", response.status_code)
    print("학생 목록조회 응답 내용", response.text)

def update_student(student_id):
    url = f"http://127.0.0.1:8000/api/students/"
    headers = {"Authorization": f"Bearer {ACCESS}"}
    data = {"id": student_id, "email": "new@naver.com"}
    response = requests.patch(url, json=data, headers=headers)
    print("학생 정보 수정 응답 상태:", response.status_code)
    print("학생 정보 수정 응답 내용", response.text)

def delete_student(student_id):
    url = f"http://127.0.0.1:8000/api/students/"
    headers = {"Authorization": f"Bearer {ACCESS}"}
    data = {"id": student_id}
    resp = requests.delete(url, json=data, headers=headers)
    print("학생 삭제:", resp.status_code)
    return resp

def list_teacherclasses():
    url = f"http://127.0.0.1:8000/api/teachers/classes"
    headers = {"Authorization": f"Bearer {ACCESS}"}
    response = requests.get(url, headers=headers)
    print("수업 목록조회 응답 상태:", response.status_code)
    print("수업 목록조회 응답 내용", response.text)

def create_schedule():
    url = f"http://127.0.0.1:8000/api/classes/schedule"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS}"
    }
    data = {
        "classroom": "201호",
        "teacherName":{"teacherId":2},
        "className": "영어",
        "daysofweek":["화", "목"],
        "todos": [
            {
                "title": "단어시험", "data": "2024-07-15", "task": "단어 50개 암기"
            }
        ]
    }
    response = requests.patch(url, json=data, headers=headers)
    print("반/스케줄 등록 응답 상태:", response.status_code)
    print("반/스케줄 등록 수정 응답 내용", response.text)

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
    #register()
    # token = login()
    # if token:
    #     item_id = create_fixture(token)
    # else:
    #     print("로그인 실패 테스트 진행 불가")
    #login()
    #refresh()
    #create_fixture()
    #update_fixture(4)
    #list_fixtures()
    #delete_fixture(4)
    #create_sudent()
    #list_students()
    #update_student(2)
    #delete_student(2)
    list_teacherclasses()
    #create_schedule()
