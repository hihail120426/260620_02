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
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "참"), ("C", "E", "거짓"), ("D", "F"), ("E", "F"), ("F", "B", "아니오")],
        "options": [
            "밝기가 50 미만인가?", # 정답
            "전등을 더 밝게 하기",
            "센서 고장 확인",
            "현재 시각 확인?"
        ],
        "answer": "밝기가 50 미만인가?"
    },
    {
        "title": "2번 미션: 청소년 버스 요금 계산",
        "scenario": "[시나리오] 나이에 따라 요금을 계산합니다.\n"
                    "나이가 13세 이상 18세 이하면 청소년 요금을 차감합니다.\n"
                    "아니라면 일반 요금을 차감합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "나이 입력받기", "box"),
            ("C", "나이가 13세 이상 ~ 18세 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", "일반 요금 차감", "box"),
            ("F", "끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "F"), ("E", "F")],
        "options": [
            "일반 요금 차감",
            "청소년 요금 차감", # 정답
            "무료 통과 처리",
            "카드 잔액 충전"
        ],
        "answer": "청소년 요금 차감"
    },
    {
        "title": "3번 미션: 스마트 온실 자동 급수",
        "scenario": "[시나리오] 습도에 따라 자동으로 물을 줍니다.\n"
                    "습도가 30% 이하면 5초간 물을 줍니다.\n"
                    "계속 반복합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "토양 습도 측정", "box"),
            ("C", "습도가 30% 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", "밸브 닫힘 유지", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": [
            "창문 열기",
            "5초간 물 주기", # 정답
            "히터 켜기",
            "스마트폰 알림 전송"
        ],
        "answer": "5초간 물 주기"
    },
    {
        "title": "4번 미션: 화재 경보 시스템",
        "scenario": "[시나리오] 연기 농도를 감지하여 경보를 울립니다.\n"
                    "연기 농도가 80 이상이면 경보음을 울립니다.\n"
                    "계속 반복합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "연기 농도 감지", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", "경보음 울리기", "box"),
            ("E", "안전 표시등 켜기", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": [
            "연기 농도가 80 이상인가?", # 정답
            "실내 온도가 영상인가?",
            "소방서에 전화가 왔는가?",
            "스프링클러가 켜졌는가?"
        ],
        "answer": "연기 농도가 80 이상인가?"
    },
    {
        "title": "5번 미션: 운동장 돌기 기록원",
        "scenario": "[시나리오] 운동장을 돌며 바퀴 수를 셉니다.\n"
                    "한 바퀴 돌 때마다 Count를 1씩 증가시킵니다.\n"
                    "Count가 10이 되면 종료합니다.",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "Count = 0", "box"),
            ("C", "한 바퀴 돌기 (Count = Count + 1)", "box"),
            ("D", "[ ? ]", "diamond"), # 빈칸
            ("E", "종료음 울리기", "box"),
            ("F", "끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E", "예"), ("D", "C", "아니오"), ("E", "F")],
        "options": [
            "제한 시간이 끝났는가?",
            "Count가 0인가?",
            "Count가 10인가?", # 정답
            "심장 박동수가 120 이상인가?"
        ],
        "answer": "Count가 10인가?"
    }
]

# --- 세션 상태(Session State) 초기화 ---
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 메인 화면 구성 ---
st.title("🧩 중1 프로그래밍: 순서도 맞추기 챌린지")
st.subheader("보기를 보고 빈칸을 채워보세요!")
st.write("---")

# 최종 결과 페이지가 아닐 때 문제 풀이 화면 표시
if not st.session_state.submitted:
    current_problem = PROBLEMS[st.session_state.current_idx]
    st.caption(f"**진행 상황:** 총 5문제 중 {st.session_state.current_idx + 1}번째")

    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.markdown(f"### {current_problem['title']}")
        st.info(current_problem['scenario'])
        st.write("---")
        
        st.write("**[ ? ] 빈칸에 들어갈 올바른 블록 내용을 선택하세요:**")
        
        saved_ans = st.session_state.user_answers.get(st.session_state.current_idx, None)
        
        selected_option = st.radio(
            "보기 문항", 
            current_problem['options'], 
            index=current_problem['options'].index(saved_ans) if saved_ans in current_problem['options'] else 0,
            key=f"prob_{st.session_state.current_idx}_radio"
        )
        
        st.session_state.user_answers[st.session_state.current_idx] = selected_option

        st.write(" ")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            if st.button("⬅️ 이전 문제", disabled=(st.session_state.current_idx == 0)):
                st.session_state.current_idx -= 1
                st.rerun()
        with b_col2:
            if st.button("다음 문제 ➡️", disabled=(st.session_state.current_idx == len(PROBLEMS) - 1)):
                st.session_state.current_idx += 1
                st.rerun()
        with b_col3:
            if st.button("🚀 최종 정답 확인", type="primary"):
                st.session_state.submitted = True
                st.rerun()

    with col2:
        st.markdown("### 📊 현재 순서도 미리보기")
        
        dot = graphviz.Digraph()
        dot.attr(rankdir='TB', size='7,7', fontname='Malgun Gothic') 
        dot.attr('node', fontname='Malgun Gothic') 
        dot.attr('edge', fontname='Malgun Gothic') 
        
        for node_id, label, shape in current_problem['nodes']:
            display_label = label
            current_style = "filled"
            fill_color = "#f5f5f5" 
            
            # 2번 문제 등에서 끝 노드가 사라지지 않도록 명확하게 [ ? ] 라벨일 때만 치환합니다.
            if label == "[ ? ]" and st.session_state.current_idx in st.session_state.user_answers: 
                display_label = st.session_state.user_answers[st.session_state.current_idx]
                fill_color = "#e1f5fe" # 하늘색 채우기 (선택 완료)
            elif label == "[ ? ]":
                fill_color = "#ffe0b2" # 주황색 채우기 (미선택)
                
            dot.node(node_id, display_label, shape=shape, style=current_style, fillcolor=fill_color)
            
        for edge in current_problem['edges']:
            if len(edge) == 3:
                dot.edge(edge[0], edge[1], label=edge[2])
            else:
                dot.edge(edge[0], edge[1])
                
        st.graphviz_chart(dot)

# --- 최종 정답 확인 처리 페이지 ---
else:
    st.markdown("## 🏁 챌린지 최종 결과")
    score = 0
    detailed_results = []
    
    for idx, prob in enumerate(PROBLEMS):
        user_ans = st.session_state.user_answers.get(idx, "미선택")
        is_correct = (user_ans == prob['answer'])
        if is_correct:
            score += 1
            
        detailed_results.append({
            "title": prob['title'],
            "user": user_ans,
            "system": prob['answer'],
            "result": "⭕ 정답" if is_correct else "❌ 오답"
        })
        
    st.metric(label="내 점수", value=f"{score} / {len(PROBLEMS)} 문제 맞춤", delta=f"{score*20}점")
    
    if score == len(PROBLEMS):
        st.balloons()
        st.success("🥇 대단해요! 모든 순서도 문제의 빈칸을 완벽하게 맞췄습니다!")
    else:
        st.warning("틀린 문제의 정답과 내 답을 비교해 보세요.")
        
    st.write("### 📋 문항별 상세 분석")
    for idx, res in enumerate(detailed_results):
        with st.container():
            st.markdown(f"#### {res['title']} → **{res['result']}**")
            st.markdown(f"- **내가 고른 답:** `{res['user']}`")
            st.markdown(f"- **실제 정답:** `{res['system']}`")
            st.divider()
            
    if st.button("🔄 처음부터 다시 풀기"):
        st.session_state.current_idx = 0
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()
