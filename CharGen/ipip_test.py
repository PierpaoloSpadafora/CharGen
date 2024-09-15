from chat_manager import ChatManager
from prompts import get_personality_test_prompt
import re


class IPIPTest:
    def __init__(self):
        self.chat_manager = ChatManager()
        self.question_mapping = self._create_question_mapping()

    def _create_question_mapping(self):
        mapping = {}
        lista_di_eccezioni_negative = [29, 39, 49]
        lista_di_eccezioni_positive = [40, 42, 48, 50]

        for i in range(1, 51):
            trait = (i - 1) % 5 + 1
            direction = '-' if i % 2 == 0 else '+'

            if i in lista_di_eccezioni_negative:
                direction = '-'
            elif i in lista_di_eccezioni_positive:
                direction = '+'

            mapping[i] = (trait, direction)

        return mapping

    def get_test_prompt(self):
        return get_personality_test_prompt()

    def run_test_for_character(self, character):
        print(f"Debug: Running IPIP test for {character.name}")
        chat_manager = ChatManager()
        chat_manager.set_character(character)
        response = chat_manager.get_personality_test_answers()
        print(f"Debug: Received response from LLM")
        scores, raw_responses = self.process_response(response)
        print(f"Debug: Processed scores: {scores}")
        return scores, raw_responses

    def process_response(self, response):
        response = response.strip()
        lines = response.split('\n')

        answers = {}
        for line in lines:
            match = re.match(r'(\d+)-(\d+)', line)
            if match:
                question_num = int(match.group(1))
                score = int(match.group(2))
                if 1 <= score <= 5:
                    answers[question_num] = score
                else:
                    print(f"Invalid score {score} for question {question_num}")
            else:
                pass

        if len(answers) != 50:
            print(f"Warning: Number of valid answers is {len(answers)}, not 50")
            return None, None

        trait_scores = {i: 0 for i in range(1, 6)}
        for question, score in answers.items():
            trait, direction = self.question_mapping[question]
            if direction == '+':
                trait_scores[trait] += score
            else:
                trait_scores[trait] += (6 - score)


        max_score = 50
        normalized_scores = {
            'Extraversion': (trait_scores[1] / max_score) * 100,
            'Agreeableness': (trait_scores[2] / max_score) * 100,
            'Conscientiousness': (trait_scores[3] / max_score) * 100,
            'Emotional Stability': (trait_scores[4] / max_score) * 100,
            'Openness': (trait_scores[5] / max_score) * 100
        }

        raw_responses = [answers.get(i, '') for i in range(1, 51)]

        normalized_scores['Neuroticism'] = 100 - normalized_scores['Emotional Stability'] # il test valuta la stabilità emotiva, l'inverso di neuroticism
        del normalized_scores['Emotional Stability']

        return normalized_scores, raw_responses
