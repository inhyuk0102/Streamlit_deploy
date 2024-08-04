import json  # JSON 파싱
import random  # Stream response 테스트용
import time  # Stream response 테스트용
import requests  # HTTP 요청 생성을 위한 requests 라이브러리 임포트
import streamlit as st
import pandas as pd
import numpy as np



ENDPOINT_LAMBDA_URL = "https://aou46i2keipjtiyg6pqqhtmfcy0itnge.lambda-url.us-west-2.on.aws/"

st.set_page_config(page_title="IGRUS", layout= "wide")
st.title("인하대학교 코딩동아리 아이그루스(IGRUS) 입니다!")
st.header('아이그루스가 뭐야?')
''':green-background[아이그루스]는 :rainbow[킹갓제너럴엠페러마제스티골져스프레셔스뷰리풀하이클래스엘레강스럭셔리클래식지니어스원더풀러블리월드탑클래스] 코딩동아리 입니다! :sunglasses:'''
st.divider()
st.subheader('1학기 활동')
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8= st.tabs(['아그둥이','원데이 클래스','정기 스터디','AWS 세미나','아그자율학습','아그인의 밤','IGRUS MT','아그톤'])

with tab1:
    st.subheader('아그둥이')
    st.write('아이그루스가 어색해도 상관없다!')
with tab2:
    st.subheader('원데이 클래스')
    st.write('어느 분야로 갈지 고민할 떄는? 원데이 클래스로 찍먹해보기!')
with tab3:
    st.subheader('정기 스터디')
    st.write('이제는 정말 공부 뿐이야..! ')
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1:
        st.subheader('객체지향프로그래밍 스터디')
    with c2:
        st.subheader('기획 스터디')
    with c3:
        st.subheader('웹 스터디')
    with c4:
        st.subheader('머신러닝 스터디')
    with c5:
        st.subheader('클라우드 스터디')
    with c6:
        st.subheader('디자인 스터디')
with tab6:
    st.subheader('아그인의 밤')
    st.write('사실.... 나 코딩얘기 좋아해....')
with tab7:
    st.write("재미있는 피구 ㅋㅋㄹㅃㅃ")
st.divider()
st.header("아이그루스 운영진")
col1,col2,col3,col4 = st.columns(4)

# 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.

with col1 :
  st.header('기술부')
  st.write(1)
with col2 :
    st.header('행정부')
    st.write('행정부장: 심바오')
with col3:
    st.header('홍보편집부')
with col4:
    st.header('재무부')
items =["나는 AI에 관심있다.", "나는 같이 코딩공부를 하고싶다.", "나는 아이그루스를 사랑한다", "나는 인하대학교 학생이다."]
selected_item = st.radio("해당하는 항목을 체크해주세요!", (items[0], items[1], items[2], items[3]))

if selected_item == "A":
    st.write("A!!")
elif selected_item == "B":
    st.write("B!")
elif selected_item == "C":
    st.write("C!")
st.text(body = '이건 텍스트이다', help= 'help')


if "messages" not in st.session_state:
    st.session_state.messages = []

# 세션 상태에 저장된 메시지 순회하며 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # 채팅 메시지 버블 생성
        st.markdown(message["content"])  # 메시지 내용 마크다운으로 렌더링


def get_streaming_response(prompt):
    s = requests.Session()
    response = s.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt}, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            text = chunk.decode()  # 바이트코드인 chunk를 decode

            yield text


# 사용자로부터 입력 받음
if prompt := st.chat_input("Message Bedrock..."):
    # 사용자 메시지 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  # 사용자 메시지 채팅 메시지 버블 생성
        st.markdown(prompt)  # 사용자 메시지 표시

    with st.chat_message("assistant"):  # 보조 메시지 채팅 메시지 버블 생성
        model_output = st.write_stream(get_streaming_response(prompt))

    # 보조 응답 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": model_output})
