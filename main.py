import streamlit as st
import graphviz

# --- 페이지 설정 ---
st.set_page_config(page_title="중1 프로그래밍: 순서도 빈칸 채우기 챌린지", layout="wide")

# --- 5가지 문제 데이터 정의 ---
PROBLEMS = [
    {
        "title": "1번 미션: 💡 스마트 가로등 제어",
        "scenario": """[시나리오] 주변이 어두워지면 자동으로 켜지는 시스템입니다.
1. 시스템을 시작합니다.
2. 조도 센서로부터 주변의 [밝기 값]을 읽어옵니다.
3. 만약 [밝기가 50 미만]이라면 [전등을 켜고], 그렇지 않다면 [전등을 끕니다].
4. 이 과정은 종료 버튼을 누를 때까지 무한히 반복됩니다.""",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "밝기 값 읽기", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", "전등 켜기", "box"),
            ("E", "전등 끄기", "box"),
            ("F", "종료 버튼 클릭?", "diamond")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "참"), ("C", "E", "거짓"), ("D", "F"), ("E", "F"), ("F", "B", "아니오")],
        "options": ["밝기가 50 미만인가?", "전등을 더 밝게 하기", "센서 고장 확인", "현재 시각 확인?"],
        "answer": "밝기가 50 미만인가?"
    },
    {
        "title": "2번 미션: 🚌 청소년 버스 요금 계산",
        "scenario": """[시나리오] 나이에 따라 요금을 다르게 정산하는 단말기입니다.
1. 승객이 카드를 대면 작동을 시작합니다.
2. 승객의 [나이]를 입력받습니다.
3. 만약 [나이가 13세 이상이고 18세 이하]라면 [청소년 요금]을 차감하고, 아니라면 [일반 요금]을 차감합니다.
4. 요금 정산이 끝나면 프로세스가 종료됩니다.""",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "나이 입력받기", "box"),
            ("C", "나이가 13세 이상 ~ 18세 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", "일반 요금 차감", "box"),
            ("F", "끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "F"), ("E", "F")],
        "options": ["청소년 요금 차감", "무료 통과 처리", "어린이 요금 차감", "카드 잔액 충전"],
        "answer": "청소년 요금 차감"
    },
    {
        "title": "3번 미션: 🌡️ 스마트 온실 자동 급수",
        "scenario": """[시나리오] 화분의 습도를 체크하여 자동으로 물을 주는 시스템입니다.
1. 시스템이 시작되면 화분의 [토양 습도]를 측정합니다.
2. 습도가 [30% 이하]로 떨어지면 부족한 수분을 채우기 위해 [5초간 밸브를 열어 물을 줍니다].
3. 습도가 충분하면 [밸브를 닫힌 상태로 유지]합니다.
4. 이 작업을 계속 반복합니다.""",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "토양 습도 측정", "box"),
            ("C", "습도가 30% 이하인가?", "diamond"),
            ("D", "[ ? ]", "box"), # 빈칸
            ("E", "밸브 닫힘 유지", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": ["5초간 물 주기", "히터 켜기", "창문 열기", "스마트폰 알림 전송"],
        "answer": "5초간 물 주기"
    },
    {
        "title": "4번 미션: 🚨 화재 경보 시스템",
        "scenario": """[시나리오] 안전을 위해 열과 연기를 감지하는 경보기 알고리즘입니다.
1. 센서가 실시간으로 실내 [연기 농도]를 감지합니다.
2. 연기 농도가 기준치인 [80 이상]이 되면 대피를 위해 [경보음을 울립니다].
3. 80 미만인 평상시에는 [안전 상태 표시등]만 켜둡니다.
4. 건물 전원이 켜져 있는 한 상시 반복 동작합니다.""",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "연기 농도 감지", "box"),
            ("C", "[ ? ]", "diamond"), # 빈칸
            ("D", "경보음 울리기", "box"),
            ("E", "안전 표시등 켜기", "box")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D", "예"), ("C", "E", "아니오"), ("D", "B"), ("E", "B")],
        "options": ["연기 농도가 80 이상인가?", "소방서에 전화가 왔는가?", "스프링클러가 켜졌는가?", "실내 온도가 영상인가?"],
        "answer": "연기 농도가 80 이상인가?"
    },
    {
        "title": "5번 미션: 🏃 10바퀴 운동장 돌기 기록원",
        "scenario": """[시나리오] 체육 시간에 운동장을 정확히 10바퀴 돌았는지 세어주는 스마트 워치 알고리즘입니다.
1. 달리기를 시작할 때 바퀴 수를 저장할 변수 [Count를 0으로 초기화]합니다.
2. 운동장을 한 바퀴 돌 때마다 [Count 변수를 1씩 증가]시킵니다.
3. 변수 [Count가 10이 되었는지 확인]하여, 10이 되었다면 [종료음]을 울리고 종료합니다.
4. 10바퀴 미만이라면 다시 한 바퀴 더 도는 단계로 이동합니다.""",
        "nodes": [
            ("A", "시작", "oval"),
            ("B", "Count = 0", "box"),
            ("C", "한 바퀴 돌기 (Count = Count + 1)", "box"),
            ("D", "[ ? ]", "diamond"), # 빈칸
            ("E", "종료음 울리기", "box"),
            ("F", "끝", "oval")
        ],
        "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E", "예"), ("D", "C", "아니오"), ("E", "F")],
        "options": ["Count가 10인가?", "제한 시간이 끝났는가?", "심장 박동수가 120 이상인가?", "Count가 0인가?"],
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
st.title("🧩 중1 프로그래밍 문제해결과 순서도 맞추기 대화방")
st.subheader("순서도 빈칸을 채워 알고리즘을 완성해 보세요!")
st.write("---")

current_problem = PROBLEMS[st.session_state.current_idx]

# 최종 결과 페이지가 아닐 때 점수판 요약 표시
if not st.session_state.submitted:
    st.caption(f"**진행 상황:** 총 5문제 중 {st.session_state.current_idx + 1}번째 문제를 푸는 중")

# --- 메인 레이아웃 (좌: 문제창, 우: 순서도 창) ---
if not st.session_state.submitted:
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown(f"### {current_problem['title']}")
        st.info(current_problem['scenario'])
        st.write("---")
        
        # 객관식 보기 라디오 버튼 혹은 클릭형 선택
        st.write("**[ ? ] 빈칸에 들어갈 올바른 블록 내용을 선택하세요:**")
        
        # 이전에 선택한 기록이 있다면 유지
        saved_ans = st.session_state.user_answers.get(st.session_state.current_idx, None)
        options_list = ["선택 안 함"] + current_problem['options']
        index_to_set = options_list.index(saved_ans) if saved_ans in options_list else 0
        
        selected_option = st.radio(
            "보기 문항", 
            options_list, 
            index=index_to_set,
            label_visibility="collapsed"
        )
        
        # 선택 값 세션에 실시간 임시저장
        if selected_option != "선택 안 함":
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
            # 5문제를 다 돌았거나 도중이라도 최종 제출 가능하게 유도
            if st.button("🚀 최종 정답 확인", type="primary"):
                st.session_state.submitted = True
                st.rerun()

    with col2:
        st.markdown("### 📊 현재 순서도 미리보기")
        
        # Graphviz를 이용한 실시간 순서도 드로잉
        dot = graphviz.Digraph()
        dot.attr(rankdir='TB', size='6,6')
        
        # 노드 배치
        for node_id, label, shape in current_problem['nodes']:
            display_label = label
            current_style = "filled"
            
            # 학생이 정답을 고르면 빈칸 내용 채워서 보여주기
            if label == "[ ? ]" and st.session_state.current_idx in st.session_state.user_answers:
                display_label = st.session_state.user_answers[st.session_state.current_idx]
                fill_color = "#e1f5fe" # 하늘색 채우기
            elif label == "[ ? ]":
                fill_color = "#ffe0b2" # 미선택시 주황색 경고 느낌 빈칸
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
    st.markdown("## 🏁 채점 결과 리포트")
    score = 0
    detailed_results = []
    
    for idx, prob in enumerate(PROBLEMS):
        user_ans = st.session_state.quiz_answers
