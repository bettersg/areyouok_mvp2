# Callbacks
(
    START,
    BACK,
    SKIP,
    CONTINUE,
    GENERATE,
    SEND_DATA,
    REGENERATE,
    GIVE_CONVERSATION_FEEDBACK_RATING,
    GIVE_CONVERSATION_FEEDBACK_TEXT,
    RESET,
    CANCEL,
    ADD_TEXT, # NOTE: that add test shouldn't increment the generate text function
) = range(12)

# Rpites
(
    START_ROUTES,
    MESSAGE_ROUTES,
    GENERATE_ROUTES,
    CONVERSATION_MESSAGE_FEEDBACK_RECEIVE_TEXT_ROUTES,
    CONVERSATION_MESSAGE_FEEDBACK_ROUTES,
    END_ROUTES,
) = range(6)

# Context: For accessing context user data
USER_ID = "backend_user_id"
CONVERSATION_MESSAGE_FEEDBACK_RATING = "conversation_message_feedback_rating"
GENERATE_COUNT = "generate_count"
CONVERSATION_DB_ID = "conversation_db_id"
CONVERSATION_MESSAGE_DB_ID = "conversation_message_db_id"
# Stores a list of messages that the user sends at once before sending all these messages to the API at once
MESSAGE_CONTEXT = "message_context"
# Stores a mapping of names to anonymized names which are taken from message forwards
MESSAGE_PERSONAS = "message_personas"
MESSAGE_IN_PROGRESS = "message_in_progress"
SEND_MESSAGES_IN_PROGRESS = "send_messages_in_progress"
# Causes state resets to not result in spamming users
SEND_MESSAGES_REMINDER_NONCE = "send_messages_reminder_nonce"

GENERATE_MESSAGE_ID = "generate_message_id"
ORIGINAL_MESSAGE_ID = "original_message_id"
INITIAL_MESSAGE_ID = "initial_message_id"  # Initially used to edit the original message sent so as to keep it to only 1 message, but may not be relevant now
LAST_CONVERSATION_MESSAGE_ID = "last_conversation_message_id"

CONVERSATION_LIMIT=3