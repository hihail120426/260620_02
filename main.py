import streamlit as st
import random

# --- 세션 상태 초기화 ---
# 퀴즈 상태를 관리하기 위한 세션 상태 변수들을 초기화합니다.
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

# --- 퀴즈 데이터 ---
# 퀴즈 문제, 정답, 그리고 각 문제에 대한 보기를 정의합니다.
# 각 보기는 문자와 모양(형태)을 가집니다.
problems = [
    {
        "id": 1,
        "title": "문제 1: 알고리즘의 시작",
        "question": "알고리즘의 시작을 나타내는 도형은 무엇일까요?",
        "options": [
            {"char": "A", "shape": "타원"}, # Oval (타원)
            {"char": "B", "shape": "직사각형"}, # Process (직사각형)
            {"char": "C", "shape": "마름모"}, # Decision (마름모)
            {"char": "D", "shape": "평행사변형"} # Input/Output (평행사변형)
        ],
        "answer_char": "A"
    },
    {
        "id": 2,
        "title": "문제 2: 처리 단계",
        "question": "계산이나 동작과 같은 처리 단계를 나타내는 도형은?",
        "options": [
            {"char": "A", "shape": "타원"}, 
            {"char": "B", "shape": "직사각형"},
            {"char": "C", "shape": "마름모"},
            {"char": "D", "shape": "평행사변형"}
        ],
        "answer_char": "B"
    },
    # 다른 문제들을 추가할 수 있습니다.
]

# --- 함수 정의 ---

# 퀴즈 시작 함수
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_problem = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False
    prepare_options()

# 다음 문제 함수
def next_problem():
    if st.session_state.current_problem < len(problems) - 1:
        st.session_state.current_problem += 1
        prepare_options()

# 이전 문제 함수
def prev_problem():
    if st.session_state.current_problem > 0:
        st.session_state.current_problem -= 1
        prepare_options()

# 보기를 셔플하고 준비하는 함수
def prepare_options():
    p = problems[st.session_state.current_problem]
    options = p['options'].copy()
    random.shuffle(options)
    st.session_state.shuffled_options = options

# 퀴즈 제출 함수
def submit_quiz():
    st.session_state.quiz_submitted = True

# --- 메인 앱 ---

# 앱 제목
st.title("대화형 순서도 퀴즈")

# 퀴즈가 시작되지 않은 경우
if not st.session_state.quiz_started:
    st.header("대화형 순서도 퀴즈에 오신 것을 환영합니다!")
    st.write("이 퀴즈는 순서도 도형과 그 의미를 배우는 데 도움이 됩니다.")
    st.button("퀴즈 시작", on_click=start_quiz)

# 퀴즈가 진행 중이고 제출되지 않은 경우
elif not st.session_state.quiz_submitted:
    p = problems[st.session_state.current_problem]
    st.header(f"문제 {p['id']}: {p['title']}")
    st.write(p['question'])

    # 보기를 표시합니다.
    st.write("---")
    cols = st.columns(len(p['options']))
    for i, opt in enumerate(st.session_state.shuffled_options):
        with cols[i]:
            # 각 보기를 시각적으로 표현합니다 (간단한 스타일 적용).
            st.markdown(f"""
                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; text-align: center; background-color: #f9f9f9; width: 150px; height: 150px;">
                    <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">{opt['char']}</div>
                    <div style="font-size: 14px; color: #555;">({opt['shape']})</div>
                    <div style="border: 2px solid #333; border-radius: 5px; width: 100px; height: 50px; margin: 10px auto; {'border-radius: 25px;' if opt['shape'] == '타원' else ''} {'transform: skew(-20deg);' if opt['shape'] == '평행사변형' else ''}"></div>
                </div>
            """, unsafe_allow_html=True)
            # 각 보기에 대한 라디오 버튼 (간접적인 선택 방식)
            st.radio(label="", options=["선택", ""], index=1, key=f"prob_{p['id']}_opt_{opt['char']}")

    st.write("---")

    # 이동 버튼
    cols_nav = st.columns([1, 1, 3])
    with cols_nav[0]:
        st.button("이전 문제", on_click=prev_problem, disabled=st.session_state.current_problem == 0)
    with cols_nav[1]:
        st.button("다음 문제", on_click=next_problem, disabled=st.session_state.current_problem == len(problems) - 1)
    
    # 마지막 문제인 경우 제출 버튼을 표시합니다.
    if st.session_state.current_problem == len(problems) - 1:
        st.write(" ")
        st.button("퀴즈 제출", on_click=submit_quiz, key="submit_button")

# 퀴즈가 제출된 경우 (결과 페이지)
else:
    st.header("퀴즈 결과")
    st.write("각 문제에 대한 정답을 확인하세요.")

    score = 0
    results_list = []
    # 정답을 확인하고 결과를 생성합니다.
    for idx, p in enumerate(problems):
        # 여기에 실제 사용자 답변을 확인하는 로직이 필요합니다.
        # 이 예시에서는 답변 수집 로직이 빠져 있습니다.
        # 실제 앱에서는 사용자가 각 보기를 선택했을 때 
        # st.session_state.user_answers[idx]에 답변을 저장해야 합니다.
        # 예: user_ans = st.session_state.user_answers.get(idx, "미답변")
        
        # 임시 답변 (사용자 답변 수집 로직 추가 필요)
        # st.session_state.user_answers[0] = "A" 
        # st.session_state.user_answers[1] = "C"

        user_ans = st.session_state.user_answers.get(idx, "미답변")
        correct_ans = p["answer_char"]
        is_correct = (user_ans == correct_ans)
        
        if is_correct:
            score += 1
            result_symbol = "⭕ (정답)"
        else:
            result_symbol = "❌ (오답)"

        # 각 문제에 대한 상세 결과를 구성합니다.
        # 사용자가 선택한 답변의 문자뿐만 아니라 모양도 포함할 수 있습니다.
        # 예: 사용자 답변: A (타원), 정답: A (타원)

        # 예시 결과를 만듭니다.
        # detailed_result = f"**문제 {p['id']}:** {p['title']}\n"
        # detailed_result += f"- 사용자 답변: {user_ans}\n"
        # detailed_result += f"- 정답: {correct_ans}\n"
        # detailed_result += f"- 결과: {result_symbol}\n\n"
        # results_list.append(detailed_result)

        # 사진을 보며 작성한 예시 코드 조각 (결과 처리 로직)
        results_list.append(f"**문제 {p['id']}:** 사용자 답변: `{user_ans}`, 정답: `{correct_ans}` - 결과: {result_symbol}")

    # 최종 점수를 표시합니다.
    st.write(f"### 최종 점수: {score} / {len(problems)}")
    for r in results_list:
        st.markdown(r)

    if st.button("다시 풀기"):
        start_quiz()
