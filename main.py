import streamlit as st

# --- 앱 설정 ---
st.set_page_config(
    page_title="중1 프로그래밍: 순서도 맞추기",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 사이드바 (정보 창) ---
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=150)
    st.title("Streamlit Cloud")
    st.markdown("### 정보")
    st.markdown("- **과목:** 중1 문제해결과 프로그래밍")
    st.markdown("- **주제:** 순서도 그리기 연습")
    st.markdown("---")
    st.markdown("[도움말 문서](https://docs.streamlit.io/)")

# --- 메인 영역 타이틀 ---
st.title("쉽고 재미있는 중1 프로그래밍 문제해결과 순서도 맞추기")
st.markdown("(Fun & Easy Middle School Programming Flowchart Puzzle)")
st.markdown("---")

# --- 문제 및 블록 영역 (왼쪽) ---
col1, col2 = st.columns([1, 1.5]) # 레이아웃 비율 설정

with col1:
    st.subheader("문제")
    st.markdown('**문제: "시험 기간 공부 계획 세우기!"**')
    st.markdown('(내일 시험 공부를 효율적으로 하기 위한 순서도를 완성해 보세요!)')
    st.markdown("---")

    st.subheader("순서도 블록")

    with st.container():
        st.write("#### 1. 시작/끝 (START/FINISH)")
        col_start, col_end = st.columns(2)
        with col_start:
            st.button("시작", key="block_start")
        with col_end:
            st.button("공부 완료!", key="block_end")

    with st.container():
        st.write("#### 2. 처리 (PROCESS)")
        process_blocks = ["과목 선정하기", "1시간 집중 공부", "쉬는 시간 갖기", "복습하기"]
        for block in process_blocks:
            st.button(block, key=f"block_process_{block}")

    with st.container():
        st.write("#### 3. 조건 (DECISION)")
        decision_blocks = ["시험 전 과목인가?", "목표 성과 달성?"]
        for block in decision_blocks:
            st.button(block, key=f"block_decision_{block}")

    with st.container():
        st.write("#### 4. 흐름선 (FLOWLINE)")
        st.button("→ (예)", key="block_flow_yes")
        st.button("→ (아니요)", key="block_flow_no")

# --- 순서도 그리기 영역 (오른쪽 - 현재는 시각화 없음) ---
with col2:
    st.subheader("순서도 그리기 (예시)")
    
    # 격자 무늬 배경 흉내 (실제 그리기 불가)
    st.markdown(
        """
        <style>
        .stCanvasBackground {
            background-image: linear-gradient(#e0e0e0 1px, transparent 1px), linear-gradient(90deg, #e0e0e0 1px, transparent 1px);
            background-size: 20px 20px;
            background-position: center;
            border: 2px solid #bdbdbd;
            border-radius: 8px;
            min-height: 500px;
            padding: 20px;
            overflow: auto;
        }
        .canvas-block {
            border: 1px solid black;
            border-radius: 5px;
            padding: 10px;
            margin: 5px;
            text-align: center;
            display: inline-block;
            background-color: white;
            cursor: pointer;
        }
        .canvas-oval { border-radius: 20px; }
        .canvas-rectangle { border-radius: 5px; }
        .canvas-diamond { border-radius: 50% 50% 50% 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; transform: rotate(-45deg); }
        .canvas-diamond p { transform: rotate(45deg); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # HTML/CSS로 예시 순서도를 그립니다.
    with st.container():
        st.markdown('<div class="stCanvasBackground">', unsafe_allow_html=True)
        
        # 시작
        st.markdown('<div class="canvas-block canvas-oval" style="background-color: lightblue;">시작</div><br>', unsafe_allow_html=True)
        
        # 과목 선정
        st.markdown(' &nbsp;&nbsp;&nbsp; ↓ <br>', unsafe_allow_html=True)
        st.markdown('<div class="canvas-block canvas-rectangle" style="background-color: lightgreen;">과목 선정하기</div><br>', unsafe_allow_html=True)
        
        # 반복문 (HTML/CSS로 완벽한 반복 표현은 복잡하여 생략)
        st.markdown(' &nbsp;&nbsp;&nbsp; ↓ <br>', unsafe_allow_html=True)
        st.markdown('<div class="canvas-block canvas-rectangle" style="background-color: NavajoWhite;">1시간 집중 공부</div> → <div class="canvas-block canvas-rectangle" style="background-color: thistle;">복습하기</div> <br>', unsafe_allow_html=True)

        # 조건문
        st.markdown(' &nbsp;&nbsp;&nbsp; ↓ <br>', unsafe_allow_html=True)
        st.markdown('<div class="canvas-block canvas-diamond" style="background-color: sandybrown;"><p>시험 전 과목인가?</p></div>', unsafe_allow_html=True)
        
        # 예/아니오 흐름
        st.markdown('<br><span style="margin-left: 60px;">예 →</span> <div class="canvas-block canvas-oval" style="background-color: moccasin; margin-left: 20px;">공부 완료!</div>', unsafe_allow_html=True)
        st.markdown('<br><span style="margin-left: -5px;">아니요 → (반복)</span>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# --- 피드백 버튼 ---
st.markdown("---")
if st.button("공부 완료! (순서도 제출)"):
    st.balloons()
    st.success("참 잘했어요! 시험 공부를 효율적으로 하기 위한 순서도를 잘 이해했군요.")
    st.markdown("다시 다른 문제를 풀어볼까요?")
