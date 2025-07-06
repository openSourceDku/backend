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

def token() :
    url = "http://127.0.0.1:8000/acounts/token/"
    data = {
        "username": "kimgeon",
        "password": "1234!",
        "role": "admin"
    }

    response = requests.post(url, json=data)
    print("응답 상태", response.status_code)
    print("응답 상태", response.text)
    print(response.json())

token()