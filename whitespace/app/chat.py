import streamlit as st
from resources.client import get_openai_client
from resources.models import ChatMessage
from resources.models import ChatParameters
from utils import get_clean_render


@st.fragment
def chat_window(enum: int, config: ChatParameters):
    st.subheader(f"Model {enum + 1}")

    clean_render = get_clean_render(config.id)
    with clean_render:
        for message in config.messages:
            with st.chat_message(message.role):
                st.write(message.content)
                if message.role == "assistant":
                    st.caption(message.model.upper())

    if getattr(st.session_state, "user_message", None):
        llm = get_openai_client(config.model, config.temperature)

        with st.chat_message("user"):
            new_message = ChatMessage(role="user", content=st.session_state.user_message)
            config.messages.append(new_message)
            st.write(new_message.content)

        with st.chat_message("assistant"):
            completion_messages = [
                {
                    "role": "system",
                    "content": config.sys_prompt,
                }
            ]
            completion_messages.extend([m.to_openai_dict() for m in config.messages])

            with st.spinner("Thinking..."):
                response = st.write_stream(llm.stream(completion_messages))

            st.caption(config.model.upper())
            config.messages.append(ChatMessage(role="assistant", content=response, model=config.model))
