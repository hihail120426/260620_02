import streamlit as st
import graphviz

# --- 페이지 설정 및 스타일 ---
st.set_page_config(page_title="중1 프로그래밍: 순서도 챌린지 (퀴즈형)", layout="wide")

st.markdown("""
    <style>
    .stSelectbox label { font-size: 1.1rem; font-weight: bold; color: #1f77b4; }
    .stRadio label { font-size: 1.1rem; }
    div[data-testid="stRadio"] > div { display: flex; flex-direction: column; gap: 10px; } /* 보기를 세로로 깔끔하게 정리 */
    </style>
""", unsafe_allow_html=True)

# --- 5가지 문제 데이터 정의 (이모지 제거됨) ---
PROBLEMS = [
    {
        "title": "1번 미션: 스마트 가로등 제어",
        "scenario": "[시나리오] 주변 밝기에 따라 가로등을 자동으로 제어합니다.\n"
                    "밝기가 50 미만이면 전등을 켭니다.\n"
                    "종료 버튼을 누를 때까지 반복합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "밝기 값 읽기", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", "전등 켜기", "box"),
            ("E", "전등 끄기", "box"),
            ("F", "종료 버튼 클릭?", "diamond")
        ],
        "edges": [("A
