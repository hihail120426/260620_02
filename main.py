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

# --- 유니코드 아이콘 정의 ---
ICON_START = " 💡 " # Oval (Start/End) - 대체 텍스트/유니코드 없음
ICON_PROCESS = " 📝 " # Rectangle (Process)
ICON_DECISION = " ♢ " # Diamond (Decision)
ICON_FLOW = " → " # Arrow (Flow)

# --- 5가지 문제 데이터 정의 (보기에 아이콘 포함) ---
PROBLEMS = [
    {
        "title": "1번 미션: 💡 스마트 가로등 제어",
        "scenario": "[시나리오] 주변 밝기에 따라 가로등을 자동으로 제어합니다.\n"
                    "밝기가 50 미만이면 전등을 켭니다.\n"
                    "종료 버튼을 누를 때까지 반복합니다.",
        "nodes": [
            ("A", f"{ICON_START}시작", "oval"),
            ("B", f"{ICON_PROCESS}밝기 값 읽기", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", f"{ICON_PROCESS}전등 켜기", "box"),
            ("E", f"{ICON_PROCESS}전등 끄기", "box"),
            ("F", f"{ICON_DECISION}종료 버튼 클릭?", "diamond")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "참"), ("C", "E", "거짓"), ("D", "F"), ("E", "F"), ("F", "B", "아니오")],
        "options": [
            f"{ICON_DECISION} 밝기가 50 미만인가?", # 정답
            f"{ICON_PROCESS} 전등을 더 밝게 하기",
            f"{ICON_PROCESS} 센서 고장 확인",
            f"{ICON_DECISION} 현재 시각 확인?"
        ],
        "answer": f"{ICON_DECISION} 밝기가 50 미만인가?"
    },
    {
        "title": "2번 미션: 🚌 청소년 버스 요금 계산",
        "scenario": "[시나리오] 나이에 따라 요금을 계산합니다.\n"
                    "나이가 13세 이상 18세 이하면 청소년 요금을 차감합니다.\n"
                    "아니라면 일반 요금을 차감합니다.",
        "nodes": [
            ("A", f"{ICON_START}시작", "oval"),
            ("B", f"{ICON_PROCESS}나이 입력받기", "box"),
            ("C", f"{ICON_DECISION}나이가 13세 이상 ~ 18세 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", f"{ICON_PROCESS}일반 요금 차감", "box"),
            ("F", f"{ICON_START}끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "F"), ("E", "F")],
        "options": [
            f"{ICON_PROCESS} 일반 요금 차감",
            f"{ICON_PROCESS} 청소년 요금 차감", # 정답
            f"{ICON_PROCESS} 무료 통과 처리",
            f"{ICON_PROCESS} 카드 잔액 충전"
        ],
        "answer": f"{ICON_PROCESS} 청소년 요금 차감"
    },
    {
        "title": "3번 미션: 🌡️ 스마트 온실 자동 급수",
        "scenario": "[시나리오] 습도에 따라 자동으로 물을 줍니다.\n"
                    "습도가 30% 이하면 5초간 물을 줍니다.\n"
                    "계속 반복합니다.",
        "nodes": [
            ("A", f"{ICON_START}시작", "oval"),
            ("B", f"{ICON_PROCESS}토양 습도 측정", "box"),
            ("C", f"{ICON_DECISION}습도가 30% 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", f"{ICON_PROCESS}밸브 닫힘 유지", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": [
            f"{ICON_PROCESS} 창문 열기",
            f"{ICON_PROCESS} 5초간 물 주기", # 정답
            f"{ICON_PROCESS} 히터 켜기",
            f"{ICON_PROCESS} 스마트폰 알림 전송"
        ],
        "answer": f"{ICON_PROCESS} 5초간 물 주기"
    },
    {
        "title": "4번 미션: 🚨 화재 경보 시스템",
        "scenario": "[시나리오] 연기 농도를 감지하여 경보를 울립니다.\n"
                    "연기 농도가 80 이상이면 경보음을 울립니다.\n"
                    "계속 반복합니다.",
        "nodes": [
            ("A", f"{ICON_START}시작", "oval"),
            ("B", f"{ICON_PROCESS}연기 농도 감지", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", f"{ICON_PROCESS}경보음 울리기", "box"),
            ("E", f"{ICON_PROCESS}안전 표시등 켜기", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": [
            f"{ICON_DECISION} 연기 농도가 80 이상인가?", # 정답
            f"{ICON_DECISION} 실내 온도가 영상인가?",
            f"{ICON_DECISION} 소방서에 전화가 왔는가?",
            f"{ICON_PROCESS} 스프링클러가 켜졌는가?"
        ],
        "answer": f"{ICON_DECISION} 연기 농도가 80 이상인가?"
    },
    {
        "title": "5번 미션: 🏃 운동장 돌기 기록원",
        "scenario": "[시나리오] 운동장을 돌며 바퀴 수를 셉니다.\n"
                    "한 바퀴 돌 때마다 Count를 1씩 증가시킵니다.\n"
                    "Count가 10이 되면 종료합니다.",
        "nodes": [
            ("A", f"{ICON_START}시작", "oval"),
            ("B", f"{ICON_PROCESS}Count = 0", "box"),
            ("C", f"{ICON_PROCESS}한 바퀴 돌기 (Count = Count + 1)", "box"),
            ("D", "[ ? ]", "diamond"), # 빈칸
            ("E", f"{ICON_PROCESS}종료음 울리기", "box"),
            ("F", f"{ICON_START}끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E", "예"), ("D", "C", "아니오"), ("E", "F")],
        "options": [
            f"{ICON_DECISION} 제한 시간이 끝났는가?",
            f"{ICON_DECISION} Count가 0인가?",
            f"{ICON_DECISION} Count가 10인가?", # 정답
            f"{ICON_DECISION} 심장 박동수가 120 이상인가?"
        ],
        "answer": f"{ICON_DECISION} Count가 10인가?"
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
st.subheader("모양과 텍스트가 함께 있는 보기를 보고 빈칸을 채워보세요!")
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
        
        # 라디오 버튼을 사용하여 모양 아이콘이 있는 보기 표시
        st.write("**[ ? ] 빈칸에 들어갈 올바른 블록 내용을 모양을 보고 선택하세요:**")
        
        # 이전에 선택한 기록이 있다면 유지
        saved_ans = st.session_state.user_answers.get(st.session_state.current_idx, None)
        # '선택 안 함' 옵션 제외 (라디오 버튼은 필수 선택 유도)
        
        selected_option = st.radio(
            "보기 문항", 
            current_problem['options'], 
            index=current_problem['options'].index(saved_ans) if saved_ans in current_problem['options'] else 0,
            key=f"prob_{st.session_state.current_idx}_radio"
        )
        
        # 선택 값 세션에 실시간 임시저장
        st.session_state.user_answers[st.session_state.current_idx] = selected_option

        # 이동 버튼 묶음
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
            # 최종 제출 버튼
            if st.button("🚀 최종 정답 확인", type="primary"):
                st.session_state.submitted = True
                st.rerun()

    with col2:
        st.markdown("### 📊 현재 순서도 미리보기")
        
        # Graphviz를 이용한 실시간 순서도 드로잉
        dot = graphviz.Digraph()
        dot.attr(rankdir='TB', size='7,7', fontname='Malgun Gothic') # 한글 폰트 설정
        dot.attr('node', fontname='Malgun Gothic') # 노드 폰트 설정
        dot.attr('edge', fontname='Malgun Gothic') # 엣지 폰트 설정
        
        # 노드 배치
        for node_id, label, shape in current_problem['nodes']:
            display_label = label
            current_style = "filled"
            
            # 학생이 정답을 고르면 빈칸 내용 채워서 보여주기
            if label == "[ ? ]" and st.session_state.current_idx in st.session_state.user_answers:
                # 보기에 있는 아이콘을 제거하고 텍스트만 표시
                display_label = st.session_state.user_answers[st.session_state.current_idx]
                fill_color = "#e1f5fe" # 하늘색 채우기
            elif label == "[ ? ]":
                fill_color = "#ffe0b2" # 미선택시 주황색 빈칸
            else:
                fill_color = "#f5f5f5"
                
            dot.node(node_id, display_label, shape=shape, style=current_style, fillcolor=fill_color)
            
        # 연결선 배치
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
        
    # 대시보드 스코어 출력
    st.metric(label="내 점수", value=f"{score} / {len(PROBLEMS)} 문제 맞춤", delta=f"{score*20}점")
    
    if score == len(PROBLEMS):
        st.balloons()
        st.success("🥇 대단해요! 모든 순서도 문제의 빈칸을 완벽하게 맞췄습니다!")
    else:
        st.warning("틀린 문제의 정답과 내 답을 비교해 보세요.")
        
    # 세부 리포트 테이블 출력
    st.write("### 📋 문항별 상세 분석")
    for idx, res in enumerate(detailed_results):
        with st.container():
            st.markdown(f"#### {res['title']} → **{res['result']}**")
            # 아이콘이 포함된 결과를 그대로 표시
            st.markdown(f"- **내가 고른 답:** `{res['user']}`")
            st.markdown(f"- **실제 정답:** `{res['system']}`")
            st.divider()
            
    if st.button("🔄 처음부터 다시 풀기"):
        st.session_state.current_idx = 0
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()
