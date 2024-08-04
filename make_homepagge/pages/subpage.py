import json  # JSON 파싱
import random  # Stream response 테스트용
import time  # Stream response 테스트용
import requests  # HTTP 요청 생성을 위한 requests 라이브러리 임포트
import streamlit as st
import pandas as pd
import numpy as np
import streamlit_tags as st_tags

import streamlit as st

# Streamlit 세션 상태에서 현재 페이지를 추적하기 위한 초기 설정
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

# 다른 페이지로 이동하는 함수
def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# 메인 페이지 내용 정의
def main_page():
    st.title('메인 페이지')
    st.write('여기는 메인 페이지입니다.')
    if st.button('서브 페이지로 이동'):
        navigate_to('sub')

# 서브 페이지 내용 정의
def sub_page():
    st.title('서브 페이지')
    st.write('여기는 서브 페이지입니다.')
    if st.button('메인 페이지로 돌아가기'):
        navigate_to('main')

# 페이지 네비게이션 로직
if st.session_state['page'] == 'main':
    main_page()
elif st.session_state['page'] == 'sub':
    sub_page()