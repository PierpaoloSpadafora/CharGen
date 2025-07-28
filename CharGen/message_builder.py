from typing import List, Dict


class MessageBuilder:

    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_system_message(self, content: str) -> None:
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def add_role_and_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def clear_all_messages(self) -> None:
        self.messages = []

    def clear_user_messages(self) -> None:
        self.messages = [msg for msg in self.messages if msg['role'] != 'user']

    def clear_assistant_messages(self) -> None:
        self.messages = [msg for msg in self.messages if msg['role'] != 'assistant']

    def clear_chat_messages(self) -> None:
        self.clear_user_messages()
        self.clear_assistant_messages()

    def clear_system_messages(self) -> None:
        self.messages = [msg for msg in self.messages if msg['role'] != 'system']

    def get_messages(self) -> List[Dict[str, str]]:
        messages = []
        for msg in self.messages:
            if msg['content'].strip():
                messages.append(msg)

        return messages

