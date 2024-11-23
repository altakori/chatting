import streamlit as st
import time
import random
import base64
from datetime import datetime
import json

# 페이지 설정
st.set_page_config(
    page_title="실시간 채팅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{random.randint(1000, 9999)}"
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'matched_user' not in st.session_state:
    st.session_state.matched_user = None
if 'group_id' not in st.session_state:
    st.session_state.group_id = None
if 'group_members' not in st.session_state:
    st.session_state.group_members = []

# CSS 스타일 적용
st.markdown("""
<style>
    .stButton>button {
        background-color: #D8BFD8;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .sent {
        background-color: #D8BFD8;
        margin-left: 20%;
    }
    .received {
        background-color: #E6E6FA;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("실시간 채팅")
    
    if not st.session_state.matched_user and not st.session_state.group_id:
        show_profile_setup()
    else:
        show_chat_interface()

def show_profile_setup():
    with st.container():
        st.subheader("프로필 설정")
        
        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio("성별", ["남자", "여자"])
        
        with col2:
            topics = ["하드웨어", "소프트웨어", "네트워크", "데이터베이스", "인공지능", "보안"]
            topic = st.selectbox("관심 주제", topics)
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("1:1 매칭 시작하기"):
                start_matching(gender, topic, False)
        
        with col4:
            if st.button("그룹 매칭 시작하기"):
                start_matching(gender, topic, True)

def show_chat_interface():
    st.subheader("채팅방")
    
    # 메시지 표시 영역
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            message_class = "sent" if msg["from"] == st.session_state.user_id else "received"
            with st.container():
                st.markdown(f"""
                    <div class="chat-message {message_class}">
                        <small>{msg['gender']}</small>
                        <p>{msg['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # 메시지 입력
    col1, col2 = st.columns([4, 1])
    with col1:
        message = st.text_input("메시지 입력", key="message_input")
    
    with col2:
        uploaded_file = st.file_uploader("이미지 업로드", type=['png', 'jpg', 'jpeg'])
    
    if st.button("전송") and (message or uploaded_file):
        send_message(message, uploaded_file)

def start_matching(gender, topic, is_group):
    with st.spinner("매칭 중..."):
        time.sleep(2)  # 실제 구현에서는 실시간 매칭 로직 구현
        if is_group:
            st.session_state.group_id = f"group_{random.randint(1000, 9999)}"
            st.session_state.group_members = [st.session_state.user_id]
        else:
            st.session_state.matched_user = f"user_{random.randint(1000, 9999)}"
        st.rerun()

def send_message(content, file=None):
    if file:
        # 이미지 처리 로직
        file_bytes = file.read()
        content = base64.b64encode(file_bytes).decode()
    
    message = {
        "from": st.session_state.user_id,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "gender": "나",
        "is_image": bool(file)
    }
    
    st.session_state.messages.append(message)
    st.rerun()

if __name__ == "__main__":
    main()