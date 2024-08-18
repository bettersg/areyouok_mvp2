import os

import streamlit as st
from resources.models import ChatParameters
from streamlit.delta_generator import DeltaGenerator

TEMP_HELP = "Higher temperatures result in more creative responses. \
    Set lower for more deterministic responses."

SYS_PROMPT_HELP = "The system prompt is never displayed to the user, but guides the model's output without \
    actually changing the model itself."


@st.dialog("Log In", width="small")
def login_dialog():
    status_container = st.container()
    form_container = st.container()

    with form_container.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Log In"):
            if username == os.environ.get("USERNAME") and password == os.environ.get("PASSWORD"):
                st.session_state.authenticated = True
                st.rerun()
            else:
                status_container.error("Invalid username or password.")


def get_clean_render(key: str) -> DeltaGenerator:
    render_slots = st.session_state.render_slots = st.session_state.get("render_slots", dict())

    slot_in_use = render_slots[key] = render_slots.get(key, "a")

    if slot_in_use == "a":
        slot_in_use = st.session_state.render_slots[key] = "b"
    else:
        slot_in_use = st.session_state.render_slots[key] = "a"

    slot = {
        "a": st.empty(),
        "b": st.empty(),
    }[slot_in_use]
    return slot.container()


def add_chat_config(temperature: float, sys_prompt: str):
    st.session_state.ai_config.append(ChatParameters(model="gpt-4o", temperature=temperature, sys_prompt=sys_prompt))


def delete_chat_config(index: int):
    del st.session_state.ai_config[index]


def clear_messages():
    for config in st.session_state.ai_config:
        config.messages = []
