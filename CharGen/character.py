from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Character:
    id: int
    name: str
    extraversion: float
    agreeableness: float
    conscientiousness: float
    neuroticism: float
    openness: float
    backstory: str = ""
    chat_knowledge: str = ""
