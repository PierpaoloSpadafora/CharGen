import sqlite3
from typing import List, Tuple, Optional
from character import Character
from settings import DB_NAME


class DatabaseManager:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.create_characters_table()

    def create_characters_table(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    openness REAL,
                    conscientiousness REAL,
                    extraversion REAL,
                    agreeableness REAL,
                    neuroticism REAL,
                    backstory TEXT,
                    chat_knowledge TEXT
                )
            ''')

    def insert_character(self, character: Character) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                   INSERT INTO characters 
                   (name, openness, conscientiousness, extraversion, agreeableness, neuroticism, backstory, chat_knowledge)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ''', (character.name, character.openness, character.conscientiousness,
                     character.extraversion, character.agreeableness, character.neuroticism,
                     character.backstory, character.chat_knowledge))

    def get_character(self, character_name: str) -> Optional[Character]:
        with sqlite3.connect(self.db_name) as conn:
            result = conn.execute('SELECT * FROM characters WHERE name = ?', (character_name,)).fetchone()
            if result:
                return Character(*result)
            else:
                return None

    def update_character(self, character: Character) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                      UPDATE characters 
                      SET name = ?, openness = ?, conscientiousness = ?, 
                          extraversion = ?, agreeableness = ?, neuroticism = ?, 
                          backstory = ?, chat_knowledge = ?
                      WHERE id = ?
                  ''', (character.name, character.openness, character.conscientiousness,
                        character.extraversion, character.agreeableness, character.neuroticism,
                        character.backstory, character.chat_knowledge, character.id))

    def edit_character_knowledge(self, character_id: int, chat_knowledge: str) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('UPDATE characters SET chat_knowledge = ? WHERE id = ?', (chat_knowledge, character_id))

    def get_character_knowledge(self, character_id: int) -> str:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute('SELECT chat_knowledge FROM characters WHERE id = ?', (character_id,)).fetchone()[0]

    def get_all_characters(self) -> List[Tuple[int, str]]:
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute('SELECT id, name FROM characters').fetchall()

    def delete_character(self, character_name: str) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('DELETE FROM characters WHERE name = ?', (character_name,))
