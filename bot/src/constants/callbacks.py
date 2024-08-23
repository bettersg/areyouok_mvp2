from areyouok_bot_telegram.constants import (
    ADD_TEXT,
    BACK,
    CANCEL,
    CONTINUE,
    GENERATE,
    GIVE_CONVERSATION_FEEDBACK_RATING,
    GIVE_CONVERSATION_FEEDBACK_TEXT,
    REGENERATE,
    RESET,
    START,
    SEND_DATA,
    SKIP,
    ADD_TEXT,
)

CALLBACKS = {
    START: "start",
    GENERATE: "generate",
    REGENERATE: "regenerate",
    GIVE_CONVERSATION_FEEDBACK_RATING: "give_conversation_feedback_rating",
    GIVE_CONVERSATION_FEEDBACK_TEXT: "give_conversation_feedback_text",
    BACK: "back",
    CONTINUE: "continue",
    RESET: "reset",
    CANCEL: "cancel",
    SKIP: "skip",
    SEND_DATA: "send_data",
    ADD_TEXT: "add_text",
}
