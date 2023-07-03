"""Class for managing chatbot in UI
"""
import random
from pathlib import Path
import streamlit as st

from streamlit_chat import message
from audio_recorder_streamlit import audio_recorder
from common import convert_stt

from ui.api_handler import PredictAskDoubt, PredictAIExaminer
from common import get_viva_context
from config import (
    API_CONFIG, 
    DATASET_COURSE_BASE_DIR
)

from utils.logging_handler import Logger


class Chatbot:
    """Manages chatbot UI
    """

    def __init__(self, chat_box_label: str = "Ask Doubt:", viva_mode: bool = False, callback=None, **kwargs) -> None:
        """Initializes a chat-bot on UI. In viva mode bot messages will be displayed before user messages.

        Args:
            chat_box_label (_type_, optional): _description_. Defaults to "Ask your queries:".
            viva_mode (bool, optional): _description_. Defaults to False.
            callback (_type_, optional): Function which will be called every time a new bot message is displayed on chat. Defaults to None.
        """
        if 'user_message' not in st.session_state:
            st.session_state['user_message'] = []

        if 'bot_message' not in st.session_state:
            st.session_state['bot_message'] = []

        if 'bot_message_context' not in st.session_state:
            st.session_state['bot_message_context'] = []

        if 'bot_message_meta_data' not in st.session_state:
            st.session_state['bot_message_meta_data'] = []

        if 'chat_input' not in st.session_state:
            st.session_state['chat_input'] = None

        # container for displaying older messages (before the last two conversations)
        self.chat_history_container = st.expander("See history")
        self.chat_container = st.container()

        self.chat_box_label = chat_box_label
        self.viva_mode = viva_mode
        self.callback = callback
        self.kwargs = kwargs
        # self.chat_query = None
        self.speech_input = None

        # sets up the chatbot UI layout
        Logger.info("Initializing the chat-bot UI")
        self._init()

        self.course_name = kwargs.get("selected_course", None)
        Logger.info("Selected course: {}".format(self.course_name))

        # for making API calls
        self.ask_doubt = PredictAskDoubt(server_config=API_CONFIG)
        self.ai_examiner = PredictAIExaminer(server_config=API_CONFIG)

    def listen_for_inputs(self,):
        """Generates a response for the input query and displays it in the chat UI.
        """
        if self.viva_mode:
            # Initial question has to be from bot if in viva mode
            if not st.session_state['bot_message']:
                bot_message = """ 🎉👏 Congrats 🥳 on completing the course! Let's check your understanding around the topic `{}` with few questions. Here is the question:""".format(
                    self.course_name)
                # call /leap/api/v1/ai-examiner/ask-question
                context = get_viva_context(DATASET_COURSE_BASE_DIR, self.course_name)
                question_type = random.choice(API_CONFIG["ai_examiner"]["viva_ask_question_types"])
                payload = {
                    "topic": self.course_name,
                    "context": context,
                    "question_type": question_type
                }
                output = self.ai_examiner.predict_aiexaminer_ask_question(
                    payload)
                ai_question = output["data"]["prediction"]["ai_question"]
                st.session_state["ai_question"] = ai_question
                
                bot_message += "\n\n" + ai_question
                st.session_state['bot_message'].append(bot_message)
                with self.chat_container:
                    self._display_message(message_index=len(
                        st.session_state['bot_message'])-1, is_user=False, more_info=True)

        user_message = st.session_state['chat_input'] if st.session_state['chat_input'] else self.speech_input

        if user_message:
            if self.viva_mode:
                st.session_state['user_message'].append(user_message)
                # call /leap/api/v1/ai-examiner/eval-answer
                ai_question = st.session_state["ai_question"] 
                payload = {
                    "topic": self.course_name,
                    "ai_question": ai_question,
                    "student_solution": user_message
                }
                output = self.ai_examiner.predict_aiexaminer_eval_answer(payload)
                student_grade = output["data"]["prediction"]["student_grade"]

                if student_grade == "Incorrect":
                    bot_message = "Well try, but your answer is ❌ Incorrect 😔\n\n"
                    # call /leap/api/v1/ai-examiner/hint-motivate
                    output = self.ai_examiner.predict_aiexaminer_hint_motivate(payload)
                    hint = output["data"]["prediction"]["hint"]
                    motivation = output["data"]["prediction"]["motivation"]
                    bot_message += "Hint: {}".format(hint) + "\n\n" + "🤛 {}".format(motivation)

                    st.session_state['bot_message'].append(bot_message)

                    st.session_state['chat_input'] = None
                    with self.chat_container:
                        self._display_message(message_index=len(
                            st.session_state['user_message'])-1, is_user=True)
                        self._display_message(message_index=len(
                            st.session_state['bot_message'])-1, is_user=False)
                else:
                    bot_message = "Wow 🥳, That's a ✔️ correct answer. You are doing great! 🚀. Here is the another question:" 

                    # call /leap/api/v1/ai-examiner/ask-question
                    context = get_viva_context(DATASET_COURSE_BASE_DIR, self.course_name)
                    question_type = random.choice(API_CONFIG["ai_examiner"]["viva_ask_question_types"])
                    payload = {
                        "topic": self.course_name,
                        "context": context,
                        "question_type": question_type
                    }
                    output = self.ai_examiner.predict_aiexaminer_ask_question(
                        payload)
                    ai_question = output["data"]["prediction"]["ai_question"]
                    st.session_state["ai_question"] = ai_question

                    bot_message += "\n\n" + ai_question
                    st.session_state['bot_message'].append(bot_message)

                    st.session_state['chat_input'] = None
                    with self.chat_container:
                        self._display_message(message_index=len(
                            st.session_state['bot_message'])-1, is_user=False)
            else:
                payload = {
                    "question": user_message,
                    "max_answer_length": API_CONFIG["ask_doubt"]["max_answer_length"],
                    "max_seq_length": API_CONFIG["ask_doubt"]["max_seq_length"],
                    "top_n": API_CONFIG["ask_doubt"]["top_n"],
                    "top_k": API_CONFIG["ask_doubt"]["top_k"]
                }
                bot_message, context, meta_data = self.ask_doubt.predict_ask_doubt(payload)
                st.session_state['user_message'].append(user_message)
                st.session_state['bot_message'].append(bot_message)
                st.session_state['bot_message_context'].append(context)
                st.session_state['bot_message_meta_data'].append(meta_data)

                st.session_state['chat_input'] = None
                with self.chat_container:
                    self._display_message(message_index=len(
                        st.session_state['user_message'])-1, is_user=True)
                    self._display_message(message_index=len(
                        st.session_state['bot_message'])-1, is_user=False, more_info=True)

    def _display_message(self, message_index: int, is_user: bool, more_info: bool = False):
        """Displays the message on chatbot UI which has the given index. 
        Message will be styled as user message or as bot message depending on is_user value.

        Args:
            message_index (int): _description_
            is_user (bool): whether this is a user message or a bot message
        """
        if is_user:
            if message_index < len(st.session_state['user_message']):
                message(st.session_state['user_message'][message_index],
                        is_user=True, key=str(message_index) + '_user', avatar_style='adventurer-neutral', seed='Loki')
        else:
            if message_index < len(st.session_state['bot_message']):
                message(st.session_state["bot_message"][message_index], key=str(
                    message_index), avatar_style='bottts', seed='Midnight')
                if not self.viva_mode:
                    # TODO: currently tested for normal mode only
                    if more_info:
                        with st.expander("Get More info"):
                            if self.callback:
                                self.callback(
                                    st.session_state['bot_message_meta_data'][message_index], **self.kwargs)
                            st.caption(
                                st.session_state['bot_message_context'][message_index])

    def _display_message_pairs(self, message_pair_index: int, more_info: bool = False):
        """Displays the message pair in the chat box UI

        Args:video_selected
            message_pair_index (int): _description_
        """

        # display user message
        # Refer: https://www.dicebear.com/styles for changing avatar_style
        if not self.viva_mode:
            self._display_message(
                message_index=message_pair_index, is_user=True, more_info=more_info)
            self._display_message(
                message_index=message_pair_index, is_user=False, more_info=more_info)
        else:
            self._display_message(
                message_index=message_pair_index, is_user=False, more_info=more_info)
            self._display_message(
                message_index=message_pair_index, is_user=True, more_info=more_info)

    def _display_chat_history(self):
        """Displays a chat-box on the UI where messages will be displayed.

        Returns:
            _type_: Containers used to display chat messages and chat history
        """

        with self.chat_container:
            if st.session_state['user_message'] or st.session_state['bot_message']:
                total_message_pairs = max(len(st.session_state['user_message']), len(
                    st.session_state['bot_message']))
                for i in range(total_message_pairs):
                    if total_message_pairs > 1 and i < total_message_pairs-1:
                        with self.chat_history_container:
                            self._display_message_pairs(message_pair_index=i)
                    else:
                        self._display_message_pairs(
                            message_pair_index=i, more_info=True)

    def _set_chat_query(self):
        """Sets the chat_query for processing and clears the input box
        """
        st.session_state['chat_input'] = st.session_state.chat_box
        st.session_state.chat_box = ''

    def _init(self):
        """Displays the chat window on the UI.
        """

        with st.container():
            st.markdown(
                """
                <style>
                .chat_container {
                    background-color: green;
                    padding: 5px;
                    border-radius: 5px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # display all the previous chats till now
            self._display_chat_history()

            # query column for typing input and speech column for microphone input
            query_column, speech_column = st.columns([22, 1])

            with query_column:
                st.text_input(label=self.chat_box_label,
                              key='chat_box', on_change=self._set_chat_query)

            with speech_column:
                audio_bytes = audio_recorder(
                    text="",
                    recording_color="#d63f31",
                    neutral_color="#6aa36f",
                    icon_name="microphone",
                    icon_size="2x",
                    sample_rate=16000,
                    key='mic'
                )
                if audio_bytes:
                    self.speech_input = convert_stt(audio_bytes)
