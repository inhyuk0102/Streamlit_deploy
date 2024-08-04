
import streamlit as st

st.set_page_config(page_title="시간표 만들기", layout= "wide")
grades = [1,2,3,4]
hackgis = [1,2,3,4,5,6,7,8]
departments = ["없다","컴퓨터공학과",'정보통신공학과','생명공학과','기계공학과']
other_department = [12]
img, input =st.columns(2)

with img:
    st.image("input_img.png")
with input:

    grade = st.selectbox(
        "학년",
        grades,
    )
    hackgi = st.selectbox(
        "학기",
        hackgis,
    )
    department = st.selectbox(
        "전공",
        departments,
    )

    other_department =st.multiselect(
    "복수전공",
    departments,
    )
    sub_department = st.multiselect(
        "부전공",
        departments,
    )
    st.header("공강 날짜")
    mon = st.checkbox("월요일")
    tue = st.checkbox("화요일")
    wen = st.checkbox("수요일")
    thu = st.checkbox("목요일")
    fri = st.checkbox("금요일")
    st.header("피하고 싶은 시간")
    time_1 = st.checkbox("09:00~10:30")
    time_2 = st.checkbox("10:30~12:00")
    time_3 = st.checkbox("12:00~13:30")
    time_4 = st.checkbox("13:30~15:00")
    time_5 = st.checkbox("15:00~16:30")
    time_6 = st.checkbox("16:30~18:00")