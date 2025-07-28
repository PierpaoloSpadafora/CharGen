import threading
from typing import List, Dict, Any
from settings import *
from language import *
from character import Character
from openai_client import OpenAIClient
from message_builder import MessageBuilder
from prompts import get_character_answer_prompt, get_summary_prompt, get_character_prompt, get_personality_test_prompt


class ChatManager:
    def __init__(self):
        self.character: Character | None = None
        self.conversation_history: List[Dict[str, str]] = []
        self.client = OpenAIClient(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
        self.message_builder = MessageBuilder()
        self.lock = threading.Lock()

        self.character_prompt = ""
        self.knowledge_prompt = ""

    def set_character_answer_prompt(self, character: Character) -> None:
        self.character = character
        self.conversation_history = []
        self.message_builder = MessageBuilder()
        self._add_character_context()

    def _add_character_context(self) -> None:
        if self.character:
            traits_description = ", ".join([
                f"{trait.capitalize()}: {getattr(self.character, trait) * 100:.0f}%"
                for trait in
                [EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, CONSCIENTIOUSNESS_TEXT, NEUROTICISM_TEXT, OPENNESS_TEXT]
            ])
            character_prompt = get_character_answer_prompt(self.character.name, traits_description,
                                                           self.character.backstory)
            self.character_prompt = character_prompt

    def _get_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        try:
            completion_stream = self.client.chat_completions_create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                stream=True
            )
            full_response = self._process_completion_stream(completion_stream)
            return full_response.strip('"')
        except Exception as e:
            return ""

    @staticmethod
    def _process_completion_stream(completion_stream: Any) -> str:
        full_response = ""
        for completion in completion_stream:
            delta = completion.get('choices', [{}])[0].get('delta', {})
            if 'content' in delta:
                full_response += delta['content']
        return full_response

    def get_response(self, general_knowledge: str, user_message: str) -> str:
        with self.lock:
            self.message_builder.clear_all_messages()
            self.message_builder.add_system_message(self.character_prompt)
            self.message_builder.add_user_message(general_knowledge)
            self.message_builder.add_user_message(user_message)

            messages = self.message_builder.get_messages()
            full_response = self._get_chat_completion(messages)

            self.message_builder.add_assistant_message(full_response)
            return full_response

    def get_backstory(self, user_message: str) -> str:
        with self.lock:
            self.message_builder.clear_all_messages()

            self.message_builder.add_system_message(self.character_prompt)
            self.message_builder.add_user_message(user_message)

            messages = self.message_builder.get_messages()
            full_response = self._get_chat_completion(messages)
            self.message_builder.add_assistant_message(full_response)
            return full_response

    def set_character(self, character: Character) -> None:
        self.character = character
        self.conversation_history = []
        self.message_builder = MessageBuilder()
        self.character_prompt = get_character_prompt(self.character)

    def get_personality_test_answers(self) -> str:
        with self.lock:
            self.message_builder.clear_all_messages()

            test_prompt = get_personality_test_prompt(self.character_prompt)
            print(test_prompt)
            self.message_builder.add_user_message(test_prompt)

            messages = self.message_builder.get_messages()
            print(messages)
            full_response = self._get_chat_completion(messages)
            self.message_builder.add_assistant_message(full_response)
            return full_response

    def generate_and_print_summary(self, present_knowledge: str, user_message: str, ai_response: str) -> str:
        with self.lock:
            self.message_builder.clear_all_messages()

            self.message_builder.add_user_message(get_summary_prompt(present_knowledge, user_message, ai_response))

            messages = self.message_builder.get_messages()
            print(messages)
            full_response = self._get_chat_completion(messages)
            self.message_builder.add_assistant_message(full_response)
            print(full_response)
            return full_response
