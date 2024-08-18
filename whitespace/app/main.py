from functools import partial

import streamlit as st
from chat import chat_window
from resources.client import OpenAIModel
from resources.models import ChatParameters
from utils import SYS_PROMPT_HELP
from utils import TEMP_HELP
from utils import add_chat_config
from utils import clear_messages
from utils import delete_chat_config
from utils import get_clean_render
from utils import login_dialog

AVAILABLE_MODELS = [model.value for model in OpenAIModel]

st.set_page_config(
    page_title="RUOK Whitespace",
    page_icon=":chat:",
    layout="wide",
    initial_sidebar_state="auto",
    # menu_items=None
)

if "ai_config" not in st.session_state:
    st.session_state.ai_config = [
        ChatParameters(
            model=OpenAIModel.GPT_4O.value,
            temperature=0.5,
            sys_prompt="You are an empathetic chatbot built by the Are You Ok? (RUOK) team.",
        )
    ]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    with st.sidebar:
        st.title("RUOK Whitespace")

        st.divider()

        st.header("Chat Models")
        st.caption("We only have access to GPT-4o at this point.")
        st.caption("gpt-4o | Latest | 128k Context | \\$2.50 Input / \\$10 Output per million")
        # st.caption("gpt-4o-mini | Latest | 128k Context | \\$0.15 Input / \\$0.60 Output per million")
        # st.caption("gpt-4-turbo | Latest | 128k Context | \\$10 Input / \\$30 Output per million")

        st.divider()

        st.button(
            "Clear Chat",
            key="clear_chat",
            help="Clear all chat messages, without changing model config.",
            on_click=partial(clear_messages),
            use_container_width=True,
        )

        with st.popover(
            "Add Model",
            help="Add a new chat model to the whitespace. Max of 3 models.",
            use_container_width=True,
            disabled=len(st.session_state.ai_config) >= 3,
        ):
            with st.form("add_model", clear_on_submit=True, border=False):
                # model = st.selectbox(
                #     "AI Model",
                #     options=AVAILABLE_MODELS,
                #     index=None
                #     )
                st.caption("All Models use GPT-4o by default.")
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    step=0.1,
                    help=TEMP_HELP,
                )
                sys_prompt = st.text_area("System Prompt", help=SYS_PROMPT_HELP)
                if st.form_submit_button("Add"):
                    add_chat_config(temperature, sys_prompt)
                    st.rerun()
        st.divider()

        for i, config in enumerate(st.session_state.ai_config):
            with st.expander(f"Model {i + 1}"):
                # config.model = st.selectbox(
                #     "AI Model",
                #     options=AVAILABLE_MODELS,
                #     index=[model.value for model in OpenAIModel].index(config.model),
                #     key=f"model_{i}"
                #     )
                st.caption("All Models use GPT-4o by default.")
                config.temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=config.temperature,
                    step=0.1,
                    key=f"temperature_{i}",
                    help=TEMP_HELP,
                )
                config.sys_prompt = st.text_area(
                    "System Prompt",
                    value=config.sys_prompt,
                    key=f"sys_prompt_{i}",
                    help=SYS_PROMPT_HELP,
                )
                st.button(
                    "Delete Model",
                    on_click=partial(delete_chat_config, i),
                    key=f"delete_{i}",
                    help="Delete this model configuration.",
                    disabled=len(st.session_state.ai_config) <= 1,
                )

    st.chat_input(
        placeholder="Type a message...",
        key="user_message",
    )

    display_chat = False
    clean_render = get_clean_render("main")

    with clean_render:
        cols = st.columns(len(st.session_state.ai_config))

        for i, config in enumerate(st.session_state.ai_config):
            with cols[i]:
                if len(config.messages) == 0 and not getattr(st.session_state, "user_message", None):
                    continue
                container = st.container(border=len(st.session_state.ai_config) > 1)
                with container:
                    display_chat = True
                    chat_window(i, config)

        if not display_chat:
            st.write("_No chat messages yet. Start by typing a message in the input box below._")

else:
    login_dialog()
