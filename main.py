import streamlit as st
import graphviz

# --- 페이지 설정 및 스타일 ---
st.set_page_config(page_title="중1 프로그래밍: 순서도 챌린지", layout="wide")

st.markdown("""
    <style>
    .stSelectbox label { font-size: 1.1rem; font-weight: bold; color: #1f77b4; }
    .stRadio label { font-size: 1.1rem; }
    div[data-testid="stRadio"] > div { display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 문제 데이터 정의 (아이콘 및 이모지 제거) ---
PROBLEMS = [
    {
        "title": "1번 미션: 스마트 가로등 제어",
        "scenario": "[시나리오] 주변 밝기에 따라 가로등을 자동으로 제어합니다.\n밝기가 50 미만이면 전등을 켭니다.\n종료 버튼을 누를 때까지 반복합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "밝기 값 읽기", "box"),
            ("C", "[ ? ]", "diamond"),
            ("D", "전등 켜기", "box"),
            ("E", "전등 끄기", "box"),
            ("F", "종료 버튼 클릭?", "diamond")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "참"), ("C", "E", "거짓"), ("D", "F"), ("E", "F"), ("F", "B", "아니오")],
        "options": ["밝기가 50 미만인가?", "전등을 더 밝게 하기", "센서 고장 확인", "현재 시각 확인?"],
        "answer": "밝기가 50 미만인가?"
    },
    {
        "title": "2번 미션: 청소년 버스 요금 계산",
        "scenario": "[시나리오] 나이에 따라 요금을 계산합니다.\n나이가 13세 이상 18세 이하면 청소년 요금을 차감합니다.\n아니라면 일반 요금을 차감합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "나이 입력받기", "box"),
            ("C", "나이가 13세 이상 ~ 18세 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"),
            ("E", "일반 요금 차감", "box"),
            ("F", "끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "F"), ("E", "F")],
        "options": ["일반 요금 차감", "청소년 요금 차감", "무료 통과 처리", "카드 잔액 충전"],
        "answer": "청소년 요금 차감"
    },
    {
        "title": "3번 미션: 스마트 온실 자동 급수",
        "scenario": "[시나리오] 습도에 따라 자동으로 물을 줍니다.\n습도가 30% 이하면 5초간 물을 줍니다.\n계속 반복합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "토양 습도 측정", "box"),
            ("C", "습도가 30% 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"),
            ("E", "밸브 닫힘 유지", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": ["창문 열기", "5초간 물 주기", "히터 켜기", "스마트폰 알림 전송"],
        "answer": "5초간 물 주기"
    },
    {
        "
