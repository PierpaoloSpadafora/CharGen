import random
import secrets
import threading
from typing import List, Dict, Optional, Tuple
from settings import *
from language import *
from ipip_test import IPIPTest
from character import Character
from chat_manager import ChatManager
from database_manager import DatabaseManager
from prompts import get_backstory_prompt, get_personality_test_prompt


class CharacterModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.chat_manager = ChatManager()
        self.ipip_test = IPIPTest()

    @staticmethod
    def generate_random_name() -> str:
        return f"{secrets.choice(ADJECTIVES)} {secrets.choice(NOUNS)}"

    @staticmethod
    def generate_random_trait() -> float:
        return round(random.random(), 2)

    def save_character(self, character: Character) -> None:
        try:
            self.db_manager.insert_character(character)
            print(f"{CHARACTER_TEXT} '{character.name}' {SAVED_SUCCESSFULLY_TEXT}")
        except Exception as e:
            print(f"{ERROR_SAVING_CHARACTER_TEXT}'{character.name}': {str(e)}")
            print(f"{CHARACTER_DETAILS_TEXT}{vars(character)}")
            raise

    def get_all_characters(self) -> List[Tuple[int, str]]:
        try:
            return self.db_manager.get_all_characters()
        except Exception as e:
            print(ERROR_RETRIEVING_CHARACTERS_TEXT.format(e))
            return []

    def get_character_knowledge(self, character_id: int) -> str:
        try:
            return self.db_manager.get_character_knowledge(character_id)
        except Exception as e:
            print(ERROR_RETRIEVING_CHARACTER_TEXT.format(e))
            return ""

    def edit_character_knowledge(self, character_id: int, chat_knowledge: str) -> None:
        try:
            self.db_manager.edit_character_knowledge(character_id, chat_knowledge)
        except Exception as e:
            print(ERROR_UPDATING_CHARACTER_TEXT.format(e))

    def get_character(self, character_name: str) -> Optional[Character]:
        try:
            return self.db_manager.get_character(character_name)
        except Exception as e:
            print(ERROR_RETRIEVING_CHARACTER_TEXT.format(e))
            return None

    def update_character(self, character: Character) -> None:
        try:
            self.db_manager.update_character(character)
        except Exception as e:
            print(ERROR_UPDATING_CHARACTER_TEXT.format(e))

    def delete_character(self, character_name: str) -> None:
        try:
            self.db_manager.delete_character(character_name)
        except Exception as e:
            print(ERROR_DELETING_CHARACTER_TEXT.format(e))

    def generate_random_character_basics(self) -> Character:
        name = self.generate_random_name()
        traits = {trait: self.generate_random_trait() for trait in
                  [EXTRAVERSION_TEXT,
                   AGREEABLENESS_TEXT,
                   CONSCIENTIOUSNESS_TEXT,
                   NEUROTICISM_TEXT,
                   OPENNESS_TEXT]}
        return Character(0, name, **traits, backstory="")

    def generate_backstory(self, character, chat_manager, callback):
        global backstory
        try:
            traits_description = ", ".join(
                [f"{trait.capitalize()}: {value * 100:.0f}%" for trait, value in vars(character).items()
                 if trait in [OPENNESS_TEXT,
                              CONSCIENTIOUSNESS_TEXT,
                              EXTRAVERSION_TEXT,
                              AGREEABLENESS_TEXT,
                              NEUROTICISM_TEXT]])
            prompt = get_backstory_prompt(character.name, traits_description)
            if prompt.strip():
                backstory = chat_manager.get_backstory(prompt)
            else:
                print(ERROR_EMPTY_PROMPT_TEXT)
                callback(None)
            backstory_lines = backstory.split('\n')[:MAX_BACKSTORY_LINES]
            character.backstory = '\n'.join(backstory_lines)
            callback(character)
        except Exception as e:
            print(ERROR_GENERATING_BACKSTORY_TEXT.format(e))
            callback(None)

    def generate_random_backstory(self, character: Character, callback) -> None:
        threading.Thread(target=self.generate_backstory, args=(character, self.chat_manager, callback), daemon=True).start()

    def create_character(self, character_name: str, traits: Dict[str, float], _backstory: str) -> bool:
        character = Character(0, character_name, **traits, backstory=_backstory,
                              chat_knowledge=THE_PLAYER_AND_CHARACTER_NAME_HAVE_NEVER_MET_TEXT)
        try:
            self.save_character(character)
            return True
        except Exception:
            return False

    def calculate_ipip_scores(self, traits: Dict[str, float]) -> Dict[str, float]:
        return {
            "Intellect": traits[OPENNESS_TEXT] * 100,
            "Conscientiousness": traits[CONSCIENTIOUSNESS_TEXT] * 100,
            "Extraversion": traits[EXTRAVERSION_TEXT] * 100,
            "Agreeableness": traits[AGREEABLENESS_TEXT] * 100,
            "Emotional Stability": (1 - traits[NEUROTICISM_TEXT]) * 100
        }

    def edit_character(self, character_id: int, character_name: str, traits: Dict[str, float], _backstory: str) -> None:
        character = Character(character_id, character_name, **traits, backstory=_backstory)
        self.update_character(character)

    @staticmethod
    def get_predefined_profiles() -> Dict[str, Dict[str, float]]:
        return PREDEFINED_PROFILES

    def get_traits_description(self, character: Character) -> str:
        return ", ".join([
            f"{trait.capitalize()}: {getattr(character, trait) * 100:.0f}%"
            for trait in
            [EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, CONSCIENTIOUSNESS_TEXT, NEUROTICISM_TEXT, OPENNESS_TEXT]
        ])

    def get_backstory_prompt(self, character_name: str, traits_description: str) -> str:
        return get_backstory_prompt(character_name, traits_description)