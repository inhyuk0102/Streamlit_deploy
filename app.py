import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from tkinter.tix import COLUMN
from pyparsing import empty
from streamlit_calendar import calendar
import itertools
import json
import requests

st.set_page_config(layout="wide", page_title="시간표 마법사", page_icon="📆")
#################################################################
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'


def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()


#########################################################

# 관심사 추천 함수
with open("commonGyoyang.json", "r", encoding="utf-8") as f:
    data = json.load(f)
courses = []
for i in data:
    if i["subject"] in courses:
        continue
    else:
        courses.append(i["subject"])
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
    selects = False * len(reco)
    st.session_state.selects = selects
    df = pd.DataFrame({"과목명": reco, "select": selects})
    edited_table = st.data_editor(
        df,
        width=1000,
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
    st.session_state.selects = edited_table["select"]


def get_interest():
    add_bg_from_url()
    recomends = []
    empty1, col1, empty2 = st.columns([0.3, 1.0, 0.3])

    with empty1:
        empty()
    with col1:
        num = st.selectbox("추천 갯수", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        prompt = st.text_input(label="", placeholder="Interest")
        if st.session_state.get("courses") != None and st.session_state.get(
                "courses") != [] and st.session_state.get("num") == num and st.session_state.get(
            "prompt") == prompt:
            recomends = st.session_state.courses

        elif prompt != None and prompt != "":
            st.session_state.prompt = prompt
            st.session_state.num = num
            prompt_1 = "나는 " + str(
                st.session_state.grades_main) + "학년" + st.session_state.dapartment_main + "학생이야 나는 " + prompt + " 분야에 관심이 있어 " + str(
                courses) + "인 과목 리스트 중에 나의 학과, 관심사와 관련한 " + str(num) + "개의 과목을 추천해줘 추천할 때 과목명 앞과뒤에 *를 붙여줘"
            model_output = " "
            model_output = model_output.join(str(a) for a in get_streaming_response(prompt_1))
            model_output = model_output[10:-1]

            # Simulate stream of response with milliseconds delay
            full_response = ""
            for chunk in (model_output).replace("\\n", "  \n"):
                full_response += chunk + " "
            for i in range(1, 1 + 2 * num, 2):
                recomends.append((full_response.split("*"))[i])

    with empty2:
        empty()
    make_table(recomends)


#######################################################

# 시간표 관련 함수

def check_day(data, days):
    if data["isWeb"]:
        return True
    if len(data["time"]) <= 1:
        return False
    for day in days:
        if day in data["time"]:
            return False
    return True


def check_hour(data, hours):
    if data["isWeb"]:
        return True
    if len(data["time"]) <= 1:
        return False
    for hour in hours:
        times = data["time"].split(',')
        for time in times:
            cur_hour = int(time[1:])
            if cur_hour == hour:
                return False
    return True


def check_subject(data, subjects):
    for subject in subjects:
        if data["subject"] == subject:
            return True
    return False


def check_match(subjects, combination):
    week_days = ["월", "화", "수", "목", "금", "토", "일", "셀"]
    schedule = {day: [0] * 24 for day in week_days}

    for subject, section in zip(subjects, combination):
        times = section["time"].split(',')
        for time in times:
            day = time[0]
            hour = int(time[1:])
            if schedule[day][hour] != 0:
                return False
            schedule[day][hour] = subject
    return True


def print_schedule(subjects, combination):
    week_days = ["월", "화", "수", "목", "금", "토", "일", "셀"]
    schedule = {day: [0] * 24 for day in week_days}

    for subject, section in zip(subjects, combination):
        times = section["time"].split(',')
        for time in times:
            day = time[0]
            hour = int(time[1:])
            if schedule[day][hour] != 0:
                return False
            schedule[day][hour] = subject



def print_to_html(subjects, combination, file_name='result.html'):
    week_days = ["월", "화", "수", "목", "금", "토", "일", "셀"]
    schedule = {day: [0] * 24 for day in week_days}

    for subject, section in zip(subjects, combination):
        times = section["time"].split(',')
        for time in times:
            day = time[0]
            hour = int(time[1:])
            if schedule[day][hour] != 0:
                return False
            schedule[day][hour] = subject

    colorbody = ["#FFD9EC", "#D4F4FA", "#E4F7BA", "#EAEAEA", "#FAECC5", "#FAE0D4", "#E8D9FF", "#FAECC5", "#FFFFFF",
                 "#ffff00"]

    with open(file_name, 'w', encoding='utf-8') as fout:
        fout.write("<table border=1 width=700 style='table-layout:fixed'>\n<tr>\n<td width=5%></td>\n")
        for day in week_days[:5]:
            fout.write(f"<td width=19%>{day}</td>\n")
        fout.write("</tr>")

        for hour in range(1, 22):
            fout.write(f"<tr><td>{hour}</td>\n")
            for day in week_days[:5]:
                if schedule[day][hour] == 0:
                    fout.write("<td></td>\n")
                else:
                    subject_index = next(i for i, subject in enumerate(subjects) if subject == schedule[day][hour])
                    fout.write(f"<td bgcolor={colorbody[subject_index % len(colorbody)]}>{schedule[day][hour]}</td>\n")
            fout.write("</tr>\n")
        fout.write("</table>")


def print_streamlit(subjects, valid_combination):
    week_days = ["월", "화", "수", "목", "금", "토", "일", "셀"]
    day_id = {"월": "a", "화": "b", "수": "c", "목": "d", "금": "e", "토": "f", "일": "g", "셀": "h"}
    schedules = []
    calendars = []
    colorbody = ["#FF6C6C", "#FFBD45", "#3DD56D", "#3D9DF3", "#FF4B4B"]

    for combination in valid_combination:
        calendar_subjects = []
        for i in range(len(combination)):
            subject = combination[i]
            times = subject["time"].split(',')
            time_dicts = []
            for time in times:
                day = time[0]
                hour = int(time[1:])
                if len(time_dicts) == 0:
                    time_dicts.append({"day": day, "start": hour, "end": hour})
                else:
                    for time_dict in time_dicts:
                        found = False
                        if time_dict["day"] == day and time_dict["end"] == hour - 1:
                            time_dict["end"] = hour
                            found = True
                    if not found:
                        time_dicts.append({"day": day, "start": hour, "end": hour})
            for time_dict in time_dicts:
                subject_info = {
                    "title": subject["subject"],
                    "color": colorbody[i % len(colorbody)],
                    "start": "2024-01-01T" + str(9 + time_dict["start"] // 2) + ":" + str(
                        time_dict["start"] % 2 * 3) + "0:00",
                    "end": "2024-01-01T" + str(9 + (time_dict["end"] + 1) // 2) + ":" + str(
                        (time_dict["end"] + 1) % 2 * 3) + "0:00",
                    "resourceId": day_id[time_dict["day"]],
                    "allDay": day == "셀"
                }
                calendar_subjects.append(subject_info)
        calendars.append(calendar_subjects)

    if len(calendars) <= 0:
        st.write("가능한 시간표가 없습니다!")
        return

    calendar_number = st.selectbox(
        "시간표 번호:",
        tuple(range(len(calendars))),
    )

    calendar_resources = [
        {"id": "a", "title": "월"},
        {"id": "b", "title": "화"},
        {"id": "c", "title": "수"},
        {"id": "d", "title": "목"},
        {"id": "e", "title": "금"},
        {"id": "h", "title": "웹"},
    ]

    calendar_options = {
        "editable": "false",
        "navLinks": "true",
        "resources": calendar_resources,
        "selectable": "true",
        "initialDate": "2024-01-01",
        "initialView": "resourceTimeGridDay",
        "resourceGroupField": "id",
    }

    state = calendar(
        events=calendars[calendar_number],
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        """,
        key=calendar_number,
    )

    # if state.get("eventsSet") is not None:
    #    st.session_state["events"] = state["eventsSet"]

    # st.write(state)


##########################################################################
def main_page():
    title_alignment = """
    <style>
    * {
        margin: 0 auto;
        opacity: 100%;
        text-align: center;
    }
    h1 {
        font-size: 96px;
    }
    h4 {
        font-size: 24px;
    }
    button {
        background-color: black;
        border-radius: 30px;
        width: 150px;
        height: 20px;
        padding: 20px;
        color: #F0F0F0;
        font-size: 24px;}

    </style>
    """

    add_bg_from_url()

    st.markdown(title_alignment, unsafe_allow_html=True)

    st.markdown("<h1 style='color: black; opacity: 100%; display: inline; text-align: center;'>당신의 변화를</h1>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='color: black; opacity: 100%; display: block; text-align: center;'>시간표로 기록하세요</h1>",
                unsafe_allow_html=True, )
    st.markdown("<h4 style='color: black; opacity: 100%; display: inline; text-align: center;'>번거롭고 복잡한 시간표 짜기!</h4>",
                unsafe_allow_html=True)
    st.markdown(
        "<h4 style='color: black; opacity: 100%; display: block; text-align: center;'>관심사를 기반으로 자신만의 커리어를 만들어가세요.</h4>",
        unsafe_allow_html=True, )
    st.markdown("</br></br>", unsafe_allow_html=True)

    if st.button("Click", type="primary"):
        navigate_to('login')


###############################################################################
def login_page():
    empty1, col1, empty2 = st.columns(3)
    with empty1:
        empty()

    with col1:
        st.markdown(
            "<h1 style='text-align: center; color: #3A95EA;@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&family=Noto+Sans+KR:wght@100..900&display=swap');'>인하대 시간표</h1>",
            unsafe_allow_html=True)
        id = st.text_input("id")
        pw = st.text_input("pw", type="password")

        btn = st.button("ㅁㄴㅇㄹ", use_container_width=True)

        isMatch = False

        if (pw == '1234567'):
            isMatch = True

        if btn and isMatch == True:
            navigate_to('info')
        elif btn and isMatch == False:
            st.write("비밀번호를 다시 확인해주세요")

    with empty2:
        empty()
    #########################################################################


def getUserInfo():
    grades = [1, 2, 3, 4]
    hackgis = [1, 2, 3, 4, 5, 6, 7, 8]
    departments = ['경영학과', '아태물류학부', '글로벌금융학과', '국제통상학과', '국어교육과', '영어교육과', '사회교육과',
                   '교육학과', '체육교육과', '수학교육과', '한국어문학과', '사학과', '철학과', '중국학과', '일본언어문화학과',
                   '경제학과', '행정학과', '정치외교학과', '미디어커뮤니케이션학과', '소비자학과', '아동심리학과', '사회복지학과',
                   '조형예술학과', '디자인융합학과', '스포츠과학과', '연극영화학과', '의류디자인학과',
                   '기계공학과', '항공우주공학과', '조선해양공학과', '산업경영공학과', '화학공학과', '고분자공학과', '신소재공학과',
                   '사회인프라공학과', '환경공학과', '공간정보공학과', '건축공학전공', '건축학전공', '에너지자원공학과', '전기공학과',
                   '전자공학과', '정보통신공학과', '반도체시스템공학과', '수학과', '통계학과', '물리학과', '화학과', '해양과학과',
                   '식품영양학과', '인공지능공학과', '데이터사이언스학과', '스마트모빌리티공학과', '디자인테크놀로지학과', '컴퓨터공학과',
                   '의예과/의학과', '간호학과', 'IBT학과', 'ISE학과', 'KLC학과', '산업경영학과', '금융투자학과', '메카트로닉스학과',
                   '소프트웨어융합공학과', '자유전공학부', '생명공학과', '생명과학과', '바이오제약공학과']
    mg = ["전공필수", "전공선택", "핵심교양", "일반교양"]
    other_department = [12]
    img, input = st.columns(2)

    # stylesheet
    title_alignment = """
    <style>
    * {
        margin: 0px;
        padding: 0px;
    }
    </style>
    """

    # add_bg_from_url()

    st.markdown(title_alignment, unsafe_allow_html=True)
    with img:
        st.image("page2.png")
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

        other_department = st.multiselect(
            "복수전공",
            departments
        )
        sub_department = st.multiselect(
            "부전공",
            departments,
        )
        subtitle = """
            <h3 style="color: #0F0F0F; text-align: left; margin-top: 0px; font-size: 16px;">이미 수강한 수업을 선택하세요.</h3>
        """
        st.markdown(subtitle, unsafe_allow_html=True)

        select_major = st.multiselect(
            "전공을 선택하세요.",  # 멘트 애매
            departments,
        )

        select_mg = st.multiselect(
            "",
            mg,
        )

        select_subject = []
        if (select_mg and select_major):
            jungong = open("jungong.json", 'r', encoding='utf-8')  # json 파일 입력
            commonGyoyang = open("commonGyoyang.json", 'r', encoding='utf-8')  # json 파일 입력
            essentialGyoyang = open("essentialGyoyang.json", 'r', encoding='utf-8')  # json 파일 입력
            data_table = json.load(jungong)
            data_table = data_table + json.load(commonGyoyang)
            data_table = data_table + json.load(essentialGyoyang)
            data_table = [data for data in data_table if data["category"] in select_mg]
            subjects = []
            for data in data_table:
                subjects.append(data["subject"])
            select_subject = st.multiselect("수업", set(subjects))

        if 'grades_main' not in st.session_state:
            st.session_state.grades_main = 1
        if 'dapartment_main' not in st.session_state:
            st.session_state.dapartment_main = ''
        if 'hackgi_main' not in st.session_state:
            st.session_state.hackgi_main = 1
        if 'ex_subjects_main' not in st.session_state:
            st.session_state.ex_subjects_main = []
        if 'page' not in st.session_state:
            st.session_state['page'] = 'main'

        if st.session_state.grades_main != grade:
            st.session_state.grades_main = grade
        if st.session_state.hackgi_main != hackgi:
            st.session_state.hackgi_main = hackgi
        if st.session_state.dapartment_main != department:
            st.session_state.dapartment_main = department
        if st.session_state.ex_subjects_main != select_subject:
            st.session_state.ex_subjects_main = select_subject

        if st.button("제출"):
            navigate_to('favorite')


#######################################################
def favorite():
    get_interest()
    if st.button("다음으로"):
        navigate_to('timetable')

    #############################################################


def timeTable():
    week_days = ["월", "화", "수", "목", "금"]
    ex_days = []
    ex_hours = []
    in_subjects = []
    # ex_days = ["금"] #제외할 요일 입력
    # ex_hours = [1, 2, 3] #제외할 교시 입력
    # in_subjects = ["객체지향프로그래밍 2", "이산구조", "자바기반응용프로그래밍", "명언으로 배우는 한자와 한문"] #들을 과목 입력

    jungong = open("jungong.json", 'r', encoding='utf-8')  # json 파일 입력
    commonGyoyang = open("commonGyoyang.json", 'r', encoding='utf-8')  # json 파일 입력
    essentialGyoyang = open("essentialGyoyang.json", 'r', encoding='utf-8')  # json 파일 입력
    data_table = json.load(jungong)
    data_table = data_table + json.load(commonGyoyang)
    data_table = data_table + json.load(essentialGyoyang)

    for i in range(len(st.session_state.courses)):
        if st.session_state.selects[i]:
            st.markdown(st.session_state.courses[i])

    st.markdown(
        "## 시간표 마법사 📆"
    )

    st.write("쉬고 싶은 날")
    day_row = st.columns(5)
    for day, row in zip(week_days, day_row):
        checked = row.checkbox(day + "요일")
        if checked and not day in ex_days:
            ex_days.append(day)
        elif not checked and day in ex_days:
            ex_days.remove(day)

    with st.expander("제외할 교시 입력"):
        hour_row = [st.columns(5)] * 6
        for i in range(6):
            for j in range(5):
                hour = i * 5 + j + 1
                checked = hour_row[i][j].checkbox(str(hour) + "교시")
                if checked and not hour in ex_hours:
                    ex_hours.append(hour)
                elif not checked and hour in ex_hours:
                    ex_hours.remove(hour)

    subject_titles = set([title for title in (data["subject"] for data in data_table)])
    in_subjects = st.multiselect(label="수강할 과목", options=subject_titles)

    data_table = [data for data in data_table if check_day(data, ex_days)]
    data_table = [data for data in data_table if check_hour(data, ex_hours)]
    data_table = [data for data in data_table if check_subject(data, in_subjects)]

    sections = []
    for subject in in_subjects:
        sections.append([data for data in data_table if data["subject"] == subject])

    all_combinations = list(itertools.product(*[section for section in sections]))

    valid_combinations = [comb for comb in all_combinations if check_match(in_subjects, comb)]


######################################################################

def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
            margin: 0 0px;
            background: url("https://i.imgur.com/pELEAXB.png") no-repeat center;
            opacity: 80%;
            background-attachment: fixed;
            height: 100vh;
            background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


if st.session_state['page'] == 'main':
    main_page()
elif st.session_state['page'] == 'login':
    login_page()
elif st.session_state['page'] == 'info':
    getUserInfo()
elif st.session_state['page'] == 'favorite':
    favorite()
elif st.session_state['page'] == 'timetable':
    timeTable()
