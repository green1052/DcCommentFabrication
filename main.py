import random
import string
from hashlib import sha256
from urllib.parse import urlparse, parse_qsl

import requests


def get_app_check():
    return requests.get("http://json2.dcinside.com/json0/app_check_A_rina.php").json()


def get_client_token():
    randomString = string.ascii_letters
    result = ""

    for i in range(11):
        result += random.choice(randomString)

    result += ":APA91bFMI-0d1b0wJmlIWoDPVa_V5Nv0OWnAefN7fGLegy6D76TN_CRo5RSUO-6V7Wnq44t7Rzx0A4kICVZ7wX-hJd3mrczE5NnLud722k5c-XRjIxYGVM9yZBScqE3oh4xbJOe2AvDe"

    return result


def get_app_id(token):
    app_key = f"dcArdchk_{get_app_check()[0]['date']}"
    app_key = sha256(app_key.encode("ascii")).hexdigest()

    data = {
        "value_token": app_key,
        "signature": "ReOo4u96nnv8Njd7707KpYiIVYQ3FlcKHDJE046Pg6s=",
        "client_token": token
    }

    return session.post("https://dcid.dcinside.com/join/mobile_app_key_verification_3rd.php", data=data).json()[0][
        "app_id"]


def write(gall_id, article_no, nickname, password, memo):
    body = {
        "id": gall_id,
        "no": article_no,
        "app_id": app_id,
        "mode": "com_write",
        "client_token": token,
        "comment_memo": memo,
        "comment_nick": nickname,
        "comment_pw": password
    }

    session.post("http://m.dcinside.com/api/comment_ok.php", body)

    print("작성 완료")

    return


loop = input("몇번 반복하겠습니까: ")
url = input("게시글 주소를 입력해주세요: ")
memo = input("내용을 입력해주세요: ")
nickname = input("닉네임을 입력해주세요: ")
password = input("비밀번호를 입력해주세요: ")

if not loop.isdigit() or not url or not memo or not nickname or not password:
    print("올바르지 못한 입력")
    exit()

url = urlparse(url)
query = dict(parse_qsl(url.query))

if not query["id"] or not query["no"]:
    print("올바르지 못한 URL")
    exit()

session = requests.session()
session.headers = {
    "User-Agent": "dcinside.app",
    "Referer": "http://m.dcinside.com",
    "Content-Type": "application/x-www-form-urlencoded"
}

token = get_client_token()
app_id = get_app_id(token)

for i in range(int(loop)):
    write(query["id"], query["no"], nickname, password, memo)
