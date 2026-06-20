import streamlit as st
import random

# --- 세션 상태 초기화 (기존과 동일) ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'shuffled_options' not in st.session_state:
    st.session_state.shuffled_options = []

# --- 퀴즈 데이터 정의 (수정됨) ---
# 각 문제의 보기에 "shape"(도형 형태) 정보를 추가했습니다.
problems = [
    {
        "id": 1,
        "title": "문제 1: 알고리즘의 시작",
        "question": "알고리즘의 '시작'을 나타내는 빈칸에 들어갈 올바른 블록은 무엇일까요?",
        "options": [
            # 정답은 타원 형태의 A입니다.
            {"char": "A", "shape": "타원", "label": "A (시작/타원)"}, 
            {"char": "B", "shape": "직사각형", "label": "B (처리/직사각형)"},
            {"char": "C", "shape": "마름모", "label": "C (조건/마름모)"},
            {"char": "D", "shape": "직사각형", "label": "D (연산/직사각형)"}
        ],
        "answer_char": "A"
    },
    {
        "id": 2,
        "title": "문제 2: 처리 단계",
        "question": "계산이나 동작과 같은 '처리' 단계를 나타내는 도형은?",
        "options": [
            {"char": "A", "shape": "타원", "label": "A (시작/타원)"},
            {"char": "B", "shape": "직사각형", "label": "B (처리/직사각형)"}, # 정답
            {"char": "C", "shape": "마름모", "label": "C (조건/마름모)"},
            {"char": "D", "shape": "평행사변형", "label": "D (입출력/평행사변형)"}
        ],
        "answer_char": "B"
    },
    # 추가 문제들을 이 형식으로 확장할 수 있습니다.
]

# --- 공통 함수 정의 (기존과 동일) ---
def prepare_options():
    p = problems[st.session_state.current_problem]
    options = p['options'].copy()
    random.shuffle(options) # 보기를 셔플합니다.
    st.session_state.shuffled_options = options

def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_problem = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False
    prepare_options()

def next_problem():
    if st.session_state.current_problem < len(problems) - 1:
        st.session_state.current_problem += 1
        prepare_options()

def prev_problem():
    if st.session_state.current_problem > 0:
        st.session_state.current_problem -= 1
        prepare_options()

def submit_quiz():
    st.session_state.quiz_submitted = True

# --- 메인 앱 구성 ---

# 앱 제목 및 기본 스타일
st.set_page_config(layout="wide") # 화면을 넓게 사용
st.title("대화형 순서도 퀴즈 (Interactive Puzzle)")
st.write("---")

# 퀴즈 시작 전
if not st.session_state.quiz_started:
    st.header("대화형 순서도 퀴즈에 오신 것을 환영합니다!")
    st.write("왼쪽에 표시된 순서도의 빈칸 [?]에 들어갈 올바른 도형을 맞추는 퀴즈입니다.")
    st.button("퀴즈 시작", on_click=start_quiz)

# 퀴즈 진행 중 (미제출)
elif not st.session_state.quiz_submitted:
    p = problems[st.session_state.current_problem]
    
    # 퀴즈 진행 상황 표시 (metric 사용)
    st.metric(label=f"진행 상황 (문제 {p['id']})", value=f"{st.session_state.current_problem + 1} / {len(problems)}")
    st.write("---")

    # [수정] 화면 레이아웃 (왼쪽: 문제 및 보기, 오른쪽: 진행 상태 및 제출)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"문제 {p['id']}: {p['title']}")
        st.write(p['question'])
        st.write("---")

        # [핵심 수정] 보기 디자인: 도형 안에 문자가 있는 형태로 변경
        # 보기를 가로 4개 컬럼으로 나눕니다.
        cols_opt = st.columns(len(p['options']))
        for i, opt in enumerate(st.session_state.shuffled_options):
            with cols_opt[i]:
                # 도형 형태에 따라 CSS 스타일을 동적으로 적용합니다.
                border_radius = "25px" if opt['shape'] == "타원" else "5px"
                skew = "skew(-20deg)" if opt['shape'] == "평행사변형" else "none"
                # 평행사변형일 때 내부 텍스트가 같이 찌그러지지 않도록 반대로 찌그려줍니다.
                text_skew = "skew(20deg)" if opt['shape'] == "평행사변형" else "none"

                # HTML/CSS를 사용하여 도형 형태의 보기를 생성합니다.
                # data-testid 속성을 추가하여 나중에 선택 로직에 활용할 수 있게 합니다.
                st.markdown(f"""
                    <div style="border: 2px solid #bdbdbd; border-radius: {border_radius}; transform: {skew}; padding: 20px; text-align: center; background-color: white; min-width: 150px; min-height: 100px; margin: 10px 0; cursor: pointer;" 
                         data-testid="option-block" data-char="{opt['char']}">
                        <div style="font-size: 32px; font-weight: bold; transform: {text_skew};">{opt['char']}</div>
                        <div style="font-size: 12px; color: #757575; transform: {text_skew};">({opt['shape']})</div>
                    </div>
                """, unsafe_allow_html=True)

                # 실제 선택을 위한 라디오 버튼 (간접 선택)
                # 이 예시에서는 버튼 클릭을 직접 감지하는 복잡한 JavaScript 없이,
                # 라디오 버튼을 하단에 배치하여 선택하도록 합니다.
                st.radio(label="", options=["선택 안 함", opt['char']], index=0, key=f"prob_{p['id']}_opt_{opt['char']}_radio")

    with col2:
        st.subheader("진행 상태")
        st.write(f"현재 풀고 있는 문제: **{p['id']}**")
        
        # 이전/다음 문제 이동 버튼
        cols_nav = st.columns([1, 1])
        with cols_nav[0]:
            st.button("⬅️ 이전 문제", on_click=prev_problem, disabled=st.session_state.current_problem == 0)
        with cols_nav[1]:
            st.button("다음 문제 ➡️", on_click=next_problem, disabled=st.session_state.current_problem == len(problems) - 1)
        
        st.write("---")
        
        # 마지막 문제일 때 제출 버튼 활성화
        if st.session_state.current_problem == len(problems) - 1:
            st.write("모든 문제를 풀었다면 제출하세요.")
            st.button("🚀 퀴즈 제출", on_click=submit_quiz, type="primary")

    # 실제 앱에서는 사용자가 각 라디오 버튼을 선택했을 때 세션 상태에 저장하는 로직이 필요합니다.
    # 예: user_ans = st.session_state.user_answers.get(idx, "미답변")

# 퀴즈 제출 후 (결과 화면)
else:
    st.header("🏁 퀴즈 결과 및 분석 리포트")
    st.write("---")
    
    score = 0
    detailed_results = []
    
    # 결과를 채점하고 리스트에 저장합니다.
    for idx, p in enumerate(problems):
        # [수정] 실제 사용자 답변을 세션 상태에서 가져오는 로직 추가
        # 사용자가 선택한 라디오 버튼 값을 가져옵니다. 
        # (이 예시에서는 답변 수집 로직이 생략되었으므로, 실제 앱에서는 보완해야 합니다.)
        # user_ans = st.session_state.user_answers.get(idx, "미답변") 
        
        # 임시 답변 (사용자 답변 수집 로직이 완성된 후 주석 해제하세요)
        # st.session_state.user_answers[0] = "A" 
        # st.session_state.user_answers[1] = "D"
        
        # 답변 수집 로직 보완 전까지는 '미답변'으로 처리됩니다.
        user_ans = st.session_state.user_answers.get(idx, "미답변")
        
        correct_ans = p["answer_char"]
        is_correct = (user_ans == correct_ans)
        
        if is_correct:
            score += 1
            result_symbol = "⭕ (정답)"
        else:
            result_symbol = "❌ (오답)"

        results_list.append(f"**문제 {p['id']}:** {p['title']} - 사용자 답변: `{user_ans}`, 정답: `{correct_ans}` - 결과: {result_symbol}")

    # 최종 점수 표시
    st.write(f"### 🏆 최종 점수: {score} / {len(problems)}")
    st.write("---")
    
    # 문항별 세부 결과 표시
    st.subheader("문항별 분석")
    for r in results_list:
        st.markdown(r)

    if st.button("🔄 다시 풀기"):
        start_quiz()
