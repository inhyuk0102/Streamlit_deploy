import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from tkinter.tix import COLUMN
from pyparsing import empty
import json
import requests



with open("common_culture.json", "r") as f:
    data = json.load(f)
courses = []
for i in data:
    if i["subject"] in courses:
        continue
    else:
        courses.append(i["subject"])

st.set_page_config(layout="wide")
ENDPOINT_LAMBDA_URL = "https://aou46i2keipjtiyg6pqqhtmfcy0itnge.lambda-url.us-west-2.on.aws/"

def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&family=Noto+Sans+KR:wght@100..900&display=swap');
         .stApp {{
             background-image: url("https://i.imgur.com/hX2CXYV.png");
             background-attachment: fixed;
             background-size: cover

         }}
         </style>
         """,
        unsafe_allow_html=True
    )
def get_streaming_response(prompt):
    s = requests.Session()
    response = s.post(ENDPOINT_LAMBDA_URL, json={"prompt": prompt}, stream=True)
    for chunk in response.iter_lines():
        if chunk:
            text = chunk.decode()  # 바이트코드인 chunk를 decode

            yield text

def make_table(reco):
    st.session_state.courses = reco
    if 'selects' not in st.session_state:
        st.session_state.selects = len(reco)
    if st.session_state.selects != len(reco) and st.session_state.courses != reco:
        st.session_state.selects = len(reco)
    df = pd.DataFrame({"과목명": reco, "select": selects})
    st.data_editor(
        df,
        width= 1000,
        column_config={
            "select": st.column_config.CheckboxColumn(
                "선택",
                help="희망하시는 과목을 선택하세요!",
                default=False,
            )
        },
        disabled=["widgets"],
        hide_index=True,
    )
def get_interest():
    add_bg_from_url()
    recomends = []
    empty1, col1, empty2 = st.columns([0.3, 1.0, 0.3])

    with empty1:
        empty()
    with col1:
        num = st.selectbox("추천 갯수", [1,2,3,4,5,6,7,8,9,10])
        if prompt := st.text_input(label="", placeholder="Interest"):
            prompt_1 = "나는 1학년 컴퓨터 공학과 학생이야 나는 " + prompt + " 분야에 관심이 있어 " + str(
                courses) + "인 과목 리스트 중에 나의 학과, 관심사와 관련한 "+str(num)+"개의 과목을 추천해줘 추천할 때 과목명 앞과뒤에 *를 붙여줘"

            model_output = " "
            model_output = model_output.join(str(a) for a in get_streaming_response(prompt_1))
            model_output = model_output[10:-1]

            # Simulate stream of response with milliseconds delay
            full_response = ""
            for chunk in (model_output).replace("\\n", "  \n"):
                full_response += chunk + " "

            for i in range(1, 1+2*num, 2):
                recomends.append((full_response.split("*"))[i])
        df = pd.DataFrame(
            np.random.randn(5, 3), columns=("col %d" % i for i in range(3))
        )

    with empty2:
        empty()
    make_table(recomends)

if 'courses' not in st.session_state:
    st.session_state.courses = []

# Session State also supports attribute based syntax

get_interest()