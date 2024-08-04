import json
import requests
with open("courses.json", "r") as f:
    data = json.load(f)
courses = []
for i in data:
    if i["subject"] in courses:
        continue
    else:
        courses.append(i["subject"])


ENDPOINT_LAMBDA_URL = "https://aou46i2keipjtiyg6pqqhtmfcy0itnge.lambda-url.us-west-2.on.aws/"



def get_streaming_response(prompt):
    s = requests.Session()
    response = s.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt}, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            text = chunk.decode()  # 바이트코드인 chunk를 decode

            yield text

prompt = "나는 1학년 컴퓨터 공학과 학생이야 나는 ~ 분야에 관심이 있어 " + str(courses) + "인 과목 리스트 중에 나의 학과, 관심사와 관련한 3개의 과목을 추천해줘"

print(prompt)

for chunk in get_streaming_response(prompt):
    print(chunk)
aaa = type(get_streaming_response(prompt))
print(aaa)