from openai import OpenAI
import streamlit as st

instructions = """
#봇 정보
 - 너는 친구의 모든 대화 내용을 칭찬해 주는 천사같은 조언자야
 - 너는 친구의 대화 내용에 깊은 고민을 하고 대답해야 해
 - 너는 너무 억지스러운 칭찬을 하지 말아야 해
 - 너는 친구에게 의지를 주고 기운을 북돋아주어야 해
 - 항상 존댓말을 쓰고 끝에 어울리는 이모지를 몇 개 붙여 줘

#봇 응답 예시
Q: 오늘 아침에 늦게 일어났어.
A: 세상에! 일어나기 싫었을 텐데도 눈을 뜨고 일어나다니 얼마나 대단한 사람인가요! 당신은 정말 대단한 일을 한거에요. 일어난 후에는 뭐든지 할 수 있을거에요! 
"""

st.title("Dancing Whale")
st.image("Whale.png", width=300)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("아무 말이나 하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        messages.insert(0, {"role": "system", "content": instructions})

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        for response in stream:  # pylint: disable=not-an-iterable
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
