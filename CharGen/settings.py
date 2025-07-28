from language import OPENNESS_TEXT, CONSCIENTIOUSNESS_TEXT, EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, NEUROTICISM_TEXT


# impostazioni database
DB_NAME = 'characters.db'


# impostazioni di OpenAI
OPENAI_BASE_URL = "http://localhost:1234/v1"
OPENAI_API_KEY = "lm-studio"


#OPENAI_MODEL = "LLaMA-3.1-8B-Q5_K_M"
#OPENAI_MODEL = "LLaMA-3.1-8B-Q8_0"

#OPENAI_MODEL = "Gemma-2-9b-Q5_K_M"
#OPENAI_MODEL = "Gemma-2-9b-Q8_0"

OPENAI_MODEL = "Gemma-2-27b-IQ2_M"
#OPENAI_MODEL = "Gemma-2-27b-Q3_K_S"


# nome file per le statistiche
STATISTICS_FILE = f'STATISTICS/csv/{OPENAI_MODEL}.csv'

# Aggiungi questa costante
MAX_TEST_ATTEMPTS = 2000

# Modifica la costante esistente se necessario
NUMBER_OF_TESTS_FOR_STATISTICS = 100
NUMBER_OF_RANDOM_CHARACTERS_TO_GENERATE = 10



# generazione nomi personaggi casuali
ADJECTIVES = [
    "Brave", "Clever", "Mysterious", "Charming", "Fierce",
    "Valiant", "Wise", "Stealthy", "Noble", "Ferocious",
    "Cunning", "Daring", "Loyal", "Gallant", "Vigilant",
    "Bold", "Intrepid", "Crafty", "Fearless", "Eloquent",
    "Resolute", "Magnificent", "Sagacious", "Unyielding", "Witty"
]
NOUNS = [
    "Warrior", "Mage", "Rogue", "Bard", "Paladin",
    "Ranger", "Sorcerer", "Druid", "Knight", "Assassin",
    "Monk", "Cleric", "Barbarian", "Shaman", "Archer",
    "Necromancer", "Alchemist", "Summoner", "Viking", "Templar",
    "Samurai", "Ninja", "Sage", "Hunter", "Priest"
]

# Personalità per un AI con tratti da videogioco
PREDEFINED_PROFILES = {
    "Hero": {EXTRAVERSION_TEXT: 0.3, AGREEABLENESS_TEXT: 0.4, CONSCIENTIOUSNESS_TEXT: 0.9, NEUROTICISM_TEXT: 0.4, OPENNESS_TEXT: 0.8},
    "Villain": {EXTRAVERSION_TEXT: 0.8, AGREEABLENESS_TEXT: 0.2, CONSCIENTIOUSNESS_TEXT: 0.7, NEUROTICISM_TEXT: 0.7, OPENNESS_TEXT: 0.6},
    "Sidekick": {EXTRAVERSION_TEXT: 0.5, AGREEABLENESS_TEXT: 0.8, CONSCIENTIOUSNESS_TEXT: 0.6, NEUROTICISM_TEXT: 0.3, OPENNESS_TEXT: 0.7},
    "Mentor": {EXTRAVERSION_TEXT: 0.4, AGREEABLENESS_TEXT: 0.9, CONSCIENTIOUSNESS_TEXT: 0.8, NEUROTICISM_TEXT: 0.2, OPENNESS_TEXT: 0.9},
    "Antihero": {EXTRAVERSION_TEXT: 0.6, AGREEABLENESS_TEXT: 0.3, CONSCIENTIOUSNESS_TEXT: 0.4, NEUROTICISM_TEXT: 0.6, OPENNESS_TEXT: 0.5},
    "Trickster": {EXTRAVERSION_TEXT: 0.7, AGREEABLENESS_TEXT: 0.5, CONSCIENTIOUSNESS_TEXT: 0.3, NEUROTICISM_TEXT: 0.5, OPENNESS_TEXT: 0.9},
    "Leader": {EXTRAVERSION_TEXT: 0.9, AGREEABLENESS_TEXT: 0.6, CONSCIENTIOUSNESS_TEXT: 0.8, NEUROTICISM_TEXT: 0.3, OPENNESS_TEXT: 0.7},
    "Rebel": {EXTRAVERSION_TEXT: 0.7, AGREEABLENESS_TEXT: 0.3, CONSCIENTIOUSNESS_TEXT: 0.4, NEUROTICISM_TEXT: 0.6, OPENNESS_TEXT: 0.8},
    "Guardian": {EXTRAVERSION_TEXT: 0.4, AGREEABLENESS_TEXT: 0.9, CONSCIENTIOUSNESS_TEXT: 0.8, NEUROTICISM_TEXT: 0.3, OPENNESS_TEXT: 0.5},
}

# impostazioni finestra
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
DIALOG_WIDTH = 300
DIALOG_HEIGHT = 300

# impostazioni ui icona di caricamento
LOADING_INDICATOR_WIDTH = 100
LOADING_INDICATOR_HEIGHT = 20
LOADING_INDICATOR_ANIMATION_SPEED = 500 # ms

# impostazioni chat
MAX_BACKSTORY_LINES = 25
