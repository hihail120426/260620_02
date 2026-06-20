import streamlit as st
import graphviz

# --- 페이지 설정 ---
st.set_page_config(page_title="스마트 전등 알고리즘 챌린지", layout="wide")

# --- 스타일 설정 ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stSelectbox label { font-size: 1.1rem; font-weight: bold; color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

st.title("💡 스마트 가로등 순서도 퍼즐")
st.subheader("중학교 1학년 문제해결과 프로그래밍 실습")

# --- 문제 제시 (구체적인 조건 포함) ---
with st.expander("📝 이번 시간의 미션 확인하기 (클릭)", expanded=True):
    st.info("""
    **[문제 상황]** 
    주변이 어두워지면 자동으로 켜지는 '스마트 가로등' 시스템의 논리 구조(알고리즘)를 설계해야 합니다.
    
    1. 시스템이 작동하면 **[시작]**합니다.
    2. 조도 센서로부터 주변의 **[밝기 값]**을 읽어옵니다.
    3. 만약 **[밝기가 50 미만]**이라면, 가로등의 **[전등을 켭니다]**.
    4. 밝기가 50 이상(밝음)이라면, **[전등을 끕니다]**.
    5. 전등 상태를 조절한 후에는 다시 밝기를 확인하기 위해 **[밝기 값을 읽는 단계]**로 돌아가 반복합니다.
    6. 사용자가 **[종료 버튼]**을 누르면 시스템은 작동을 멈추고 종료됩니다.
    
    위 시나리오에 맞게 아래 블록들을 순서대로 배치해보세요!
    """)

# --- 데이터 정의 ---
options = [
    "선택하세요", "시작", "밝기 값 읽기", "밝기가 50 미만인가?", 
    "전등 켜기", "전등 끄기", "종료 버튼 클릭?", "끝"
]

# 정답 시퀀스 (논리 흐름)
# 시작 -> 읽기 -> 조건(밝기) -> (참)켜기/(거짓)끄기 -> 조건(종료) -> 끝
correct_answer = ["시작", "밝기 값 읽기", "밝기가 50 미만인가?", "전등 켜기", "전등 끄기", "종료 버튼 클릭?"]

# --- 입력 섹션 ---
col1, col2 = st.columns([1, 1.5])

user_choices = []
with col1:
    st.write("### 🧩 알고리즘 블록 배치")
    for i in range(6):
        choice = st.selectbox(f"{i+1}번 단계 블록", options, key=f"step_{i}")
        user_choices.append(choice)

# --- 시각화 섹션 (Graphviz) ---
with col2:
    st.write("### 📊 실시간 순서도 확인")
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB')
    
    # 노드 모양 설정 함수
    def get_shape(label):
        if label in ["시작", "끝"]: return "oval"
        if "?" in label: return "diamond"
        return "box"

    # 선택된 블록들로 실시간 그래프 생성
    valid_choices = [c for c in user_choices if c != "선택하세요"]
    
    if not valid_choices:
        st.warning("왼쪽에서 블록을 선택하면 순서도가 여기에 그려집니다!")
    else:
        for i, choice in enumerate(valid_choices):
            dot.node(str(i), choice, shape=get_shape(choice))
            if i > 0:
                # 기본 흐름 연결
                dot.edge(str(i-1), str(i))
        
        # 반복(루프) 시각화 예시 (특정 조건 만족 시)
        if "종료 버튼 클릭?" in valid_choices and "밝기 값 읽기" in valid_choices:
            idx_end = valid_choices.index("종료 버튼 클릭?")
            idx_read = valid_choices.index("밝기 값 읽기")
            dot.edge(str(idx_end), str(idx_read), label="아니오(반복)")

        st.graphviz_chart(dot)

# --- 결과 확인 ---
st.divider()
if st.button("🚀 정답 확인하기", use_container_width=True):
    if user_choices == correct_answer:
        st.balloons()
        st.success("🎉 완벽합니다! 스마트 가로등의 논리 구조를 정확하게 설계했습니다!")
    else:
        # 어디가 틀렸는지 힌트 제공
        st.error("앗! 순서가 조금 틀린 것 같아요. 문제 시나리오를 다시 천천히 읽어보세요.")
        # 간단한 힌트 로직
        correct_count = sum(1 for u, c in zip(user_choices, correct_answer) if u == c)
        st.info(f"현재 6단계 중 {correct_count}단계를 맞췄습니다. 힘내세요!")
