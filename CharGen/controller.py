import os
import csv
import time
import random
import threading
from typing import Dict
from settings import *
from language import *
import stats
from ipip_test import IPIPTest
from character import Character
from chat_manager import ChatManager
from view import CharacterCreatorView
from prompts import get_character_prompt
from character_model import CharacterModel


class CharacterCreatorController:
    def __init__(self, model: CharacterModel, view: CharacterCreatorView):
        self.model = model
        self.view = view
        self.chat_manager = ChatManager()
        self.ipip_test = IPIPTest()
        self.view.setup_event_handlers(self)
        self.view.setup_keyboard_shortcuts(self)
        self.load_characters()
        self.view.set_predefined_profiles(self.model.get_predefined_profiles())
        self.view.select_random_character.config(command=self.select_random_character)
        self.view.show_test_prompt_button.config(command=self.show_test_prompt)
        self.personality_test_running = False
        self.test_counter = 0
        self.total_expected_tests = 0
        self.is_generating_characters = False
        self.view.make_stats_button.config(command=self.make_stats)

    def make_stats(self):
        self.view.disable_make_stats_button()
        self.view.show_personality_test_loading()
        threading.Thread(target=self._generate_statistics, daemon=True).start()

    def _generate_statistics(self):
        try:
            for progress in stats.generate_statistics():
                self.view.master.after(0, self.view.update_progress_bar, progress)
            self.view.master.after(0, self._handle_stats_result, True)
        except Exception as e:
            self.view.master.after(0, self.view.show_error, f"Error generating statistics: {str(e)}")
        finally:
            self.view.master.after(0, self._finish_stats_generation)

    def _handle_stats_result(self, success):
        if success:
            self.view.show_info(STATISTICS_GENERATED_SUCCESSFULLY_TEXT)
        else:
            self.view.show_error(FAILED_TO_GENERATE_STATISTICS_TEXT)

    def _finish_stats_generation(self):
        self.view.hide_personality_test_loading()
        self.view.enable_make_stats_button()

    def generate_random_characters(self):
        if self.is_generating_characters:
            return

        self.is_generating_characters = True
        self.view.disable_character_generation_buttons()
        self.view.show_loading()

        threading.Thread(target=self.generate_and_save_character, daemon=True).start()

    def generate_and_save_character(self):
        for _ in range(NUMBER_OF_RANDOM_CHARACTERS_TO_GENERATE):
            character = self.model.generate_random_character_basics()
            self.generate_random_backstory_sync(character)
            self.model.save_character(character)
            self.view.master.after(0, self.view.refresh_character_list, self.model.get_all_characters())

        self.view.master.after(0, self.finish_character_generation)

    def select_random_character(self) -> None:
        characters = self.model.get_all_characters()
        if characters:
            random_character = random.choice(characters)
            self.view.character_select.set(random_character[1])
            self.on_chat_character_selected(None)
        else:
            self.view.show_error(NO_CHARACTERS_AVAILABLE_TEXT)

    def generate_random_character_basics(self) -> None:
        profiles = list(self.model.get_predefined_profiles().keys()) + [CUSTOM_TEXT]
        random_profile = random.choice(profiles)

        if random_profile == CUSTOM_TEXT:
            traits = {trait: self.model.generate_random_trait() for trait in
                      [EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, CONSCIENTIOUSNESS_TEXT, NEUROTICISM_TEXT, OPENNESS_TEXT]}
        else:
            traits = self.model.get_predefined_profiles()[random_profile]

        name = self.model.generate_random_name()

        character = Character(0, name, **traits)
        self.view.set_character_basic_traits(character)
        self.view.profile_select.set(random_profile)
        self.view.profile_select.set(CUSTOM_TEXT)
        self.apply_predefined_profile(None)

    def generate_random_backstory_sync(self, character):
        traits_description = self.model.get_traits_description(character)
        prompt = self.model.get_backstory_prompt(character.name, traits_description)
        backstory = self.chat_manager.get_backstory(prompt)
        backstory_lines = backstory.split('\n')[:MAX_BACKSTORY_LINES]
        character.backstory = '\n'.join(backstory_lines)

    def generate_random_backstory(self) -> None:
        character_info = self.view.get_character_info()
        name = self.view.name_entry.get().strip()

        if not name or not all(character_info.values()):
            self.view.show_incomplete_fields_warning()
            return

        character = Character(0, name, **character_info)
        self.view.show_loading()
        self.view.disable_character_generation_buttons()
        self.model.generate_random_backstory(character, self.on_backstory_generated)

    def on_backstory_generated(self, character: Character) -> None:
        def update_ui():
            if character:
                self.view.set_character_backstory(character.backstory)
            else:
                self.view.show_error(ERROR_TEXT)
            self.view.hide_loading()
            self.view.enable_character_generation_buttons()
            self.view.update_copy_button_state()

        self.view.master.after(0, update_ui)

    def apply_predefined_profile(self, event: any) -> None:
        profile_name = self.view.get_selected_profile()
        if profile_name and profile_name != CUSTOM_TEXT:
            profile = self.model.get_predefined_profiles()[profile_name]
            self.view.set_character_basic_traits(profile)
            self.view.profile_select.set(profile_name)
            self.view.update_copy_button_state()

    def save_character(self) -> None:
        name = self.view.name_entry.get().strip()
        if not name:
            self.view.show_error(PLEASE_ENTER_CHARACTER_NAME_TEXT)
            return

        traits = self.view.get_character_info()
        backstory = self.view.backstory_text.get("1.0", "end-1c")
        if self.model.create_character(name, traits, backstory):
            self.view.show_info(CHARACTER_SAVED_SUCCESSFULLY_TEXT.format(name))
            self.view.clear_character_info()
            self.load_characters()
        else:
            self.view.show_error(FAILED_TO_SAVE_CHARACTER_TEXT)

    def edit_character(self):
        full_name = self.view.get_selected_character()
        if not full_name:
            self.view.show_error(SELECT_CHARACTER_TO_CHAT_TEXT)
            return

        character = self.model.get_character(full_name)
        if not character:
            self.view.show_error(CHARACTER_NOT_FOUND_TEXT.format(full_name))
            return

        self.view.create_edit_window(character, self.save_edits)

    def finish_character_generation(self):
        self.view.hide_loading()
        self.view.enable_character_generation_buttons()
        self.view.show_info(
            f"{NUMBER_OF_RANDOM_CHARACTERS_TO_GENERATE} random characters have been generated and saved.")
        self.is_generating_characters = False
        self.load_characters()

    def save_edits(self, character_id: int, new_name: str, traits: Dict[str, float], backstory: str,
                   window: any) -> None:
        if not new_name.strip():
            self.view.show_error(CHARACTER_NAME_EMPTY_TEXT)
            return

        try:
            character = Character(character_id, new_name, **traits, backstory=backstory)
            self.model.update_character(character)
            self.view.show_info(CHANGES_SAVED_SUCCESSFULLY_TEXT.format(new_name))
            window.destroy()
            self.load_characters()
        except Exception as e:
            self.view.show_error(str(e))

    def delete_character(self):
        full_name = self.view.get_selected_character()
        if not full_name:
            self.view.show_error(SELECT_CHARACTER_TO_CHAT_TEXT)
            return

        if self.view.show_confirm(CONFIRM_DELETE_CHARACTER_TEXT.format(full_name)):
            self.model.delete_character(full_name)
            self.load_characters()

    def view_character_info(self):
        full_name = self.view.get_selected_character()
        if not full_name:
            self.view.show_error(PLEASE_SELECT_CHARACTER_TO_VIEW_TEXT)
            return

        character = self.model.get_character(full_name)
        if not character:
            self.view.show_error(CHARACTER_NOT_FOUND_TEXT.format(full_name))
            return

        similarity = self.model.get_similarity(character) if hasattr(self.model, 'get_similarity') else 0.0

        self.view.show_character_info(character, similarity)

    def load_characters(self):
        characters = self.model.get_all_characters()
        self.view.refresh_character_list(characters)

        if characters:
            first_character = characters[0][1]
            self.view.character_select.set(first_character)
            self.on_chat_character_selected(None)

    def on_chat_character_selected(self, event: any) -> None:
        name = self.view.get_selected_chat_character()
        if name:
            character = self.model.get_character(name)
            self.chat_manager.set_character_answer_prompt(character)
            self.view.clear_chat()
            self.view.add_message_to_chat(NOW_CHATTING_WITH_TEXT.format(name), "System")

    def clear_chat(self) -> None:
        self.view.clear_chat()
        if self.chat_manager.character:
            self.view.add_message_to_chat(CHAT_CLEARED_TEXT.format(self.chat_manager.character.name), "System")

    def get_npc_dialog_response(self, user_message: str) -> None:
        general_knowledge = self.model.get_character_knowledge(self.chat_manager.character.id)
        ai_response = self.chat_manager.get_response(general_knowledge, user_message)
        summary = self.generate_and_print_summary(user_message, ai_response)
        self.model.edit_character_knowledge(self.chat_manager.character.id, summary)
        self.view.master.after(0, lambda: self.update_chat_ui(ai_response))

    def update_chat_ui(self, ai_response: str) -> None:
        self.view.add_message_to_chat(ai_response, self.chat_manager.character.name)
        self.view.hide_chat_loading()
        self.view.enable_chat_buttons()

    def generate_and_print_summary(self, user_message: str, ai_response: str) -> str:
        general_knowledge = self.model.get_character_knowledge(self.chat_manager.character.id)
        summary = self.chat_manager.generate_and_print_summary(general_knowledge, user_message, ai_response)
        return summary

    def send_chat_message(self) -> None:
        if not self.chat_manager.character:
            self.view.show_error(SELECT_CHARACTER_TO_CHAT_TEXT)
            return

        user_message = self.view.get_chat_input().strip()
        if not user_message:
            self.view.show_error(ENTER_MESSAGE_BEFORE_SENDING_TEXT)
            return

        self.view.add_message_to_chat(user_message, "You")
        self.view.clear_chat_input()
        self.view.show_chat_loading()
        self.view.disable_chat_buttons()

        threading.Thread(target=self.get_npc_dialog_response, args=(user_message,), daemon=True).start()

    def _get_selected_character(self):
        full_name = self.view.get_selected_character()
        if not full_name:
            self.view.show_error(SELECT_CHARACTER_TO_CHAT_TEXT)
            return None
        character = self.model.get_character(full_name)
        if not character:
            self.view.show_error(CHARACTER_NOT_FOUND_TEXT.format(full_name))
            return None
        return character

    def run_personality_test(self):
        character = self._get_selected_character()
        if not character:
            print("Debug: No character selected")
            return
        if self._start_personality_test(character):
            threading.Thread(target=self._run_single_test_for_character, args=(character,), daemon=True).start()

    def _run_single_test_for_character(self, character):
        start_time = time.time()
        result = self.ipip_test.run_test_for_character(character)
        if result is None:
            self.view.add_message_to_chat("Failed to process personality test results.", "System")
            return

        ipip_scores, raw_responses = result
        print(f"IPIP scores calculated: {ipip_scores}")
        accuracy, trait_accuracies = self._calculate_accuracy(character, ipip_scores)
        end_time = time.time()
        test_duration = round(end_time - start_time, 2)
        print(f"Accuracy calculated: {accuracy}")

        self._save_test_results_to_csv(character, ipip_scores, accuracy, trait_accuracies, test_duration, raw_responses)
        self.view.master.after(0, lambda: self._display_test_result(character.name, ipip_scores, accuracy))
        self.view.master.after(0, self._end_personality_test)

    def _start_personality_test(self, character):
        if hasattr(self, 'personality_test_running') and self.personality_test_running:
            print("Debug: A personality test is already running")
            self.view.show_info("A personality test is already in progress. Please wait.")
            return False
        self.personality_test_running = True
        self.view.show_personality_test_loading()
        self.view.disable_personality_test_buttons()
        self.chat_manager.set_character_answer_prompt(character)
        self.view.clear_chat()
        self.view.add_message_to_chat(f"Starting personality test for {character.name}", "System")
        return True

    def run_multiple_personality_tests(self):
        character = self._get_selected_character()
        if not character:
            return

        self.total_expected_tests = NUMBER_OF_TESTS_FOR_STATISTICS
        self.test_counter = 0
        self.view.show_personality_test_loading()
        self.view.disable_personality_test_buttons()

        threading.Thread(target=self._run_multiple_tests_for_character,
                         args=(character,),
                         daemon=True).start()

    def _run_multiple_tests_for_character(self, character):
        for _ in range(self.total_expected_tests):
            self._run_test_for_character(character)
            self.test_counter += 1
            self.view.master.after(0, self._update_progress)

        self.view.master.after(0, self._end_personality_test)

    def _run_test_for_character(self, character):
        try:
            start_time = time.time()
            ipip_scores, raw_responses = self.ipip_test.run_test_for_character(character)
            if ipip_scores is None:
                print(f"Failed to process personality test results for {character.name}")
                return False

            accuracy, trait_accuracies = self._calculate_accuracy(character, ipip_scores)
            end_time = time.time()
            test_duration = round(end_time - start_time, 2)
            print(f"Accuracy calculated for {character.name}: {accuracy}")

            self._save_test_results_to_csv(character, ipip_scores, accuracy, trait_accuracies, test_duration, raw_responses)

            return True
        except Exception as e:
            print(f"Error during test for {character.name}: {str(e)}")
            return False

    def _update_progress(self):
        progress = (self.test_counter / self.total_expected_tests) * 100
        self.view.update_progress_bar(progress)

    def test_all_characters(self):
        characters = self.model.get_all_characters()
        if not characters:
            self.view.show_info(NO_CHARACTERS_AVAILABLE_TO_TEST_TEXT)
            return

        self.view.show_personality_test_loading()
        self.view.disable_personality_test_buttons()

        completed_tests = {char_id: 0 for char_id, _ in characters}
        total_tests = len(characters) * NUMBER_OF_TESTS_FOR_STATISTICS

        self.test_counter = 0
        self.total_expected_tests = total_tests

        def run_tests():
            while min(completed_tests.values()) < NUMBER_OF_TESTS_FOR_STATISTICS:
                for char_id, char_name in characters:
                    if completed_tests[char_id] < NUMBER_OF_TESTS_FOR_STATISTICS:
                        character = self.model.get_character(char_name)
                        if character:
                            self._run_test_for_character(character) # mettere qua if test succeded counter +1
                            completed_tests[char_id] += 1
                            self.test_counter += 1
                            self.view.master.after(0, self._update_progress)

            self.view.master.after(0, self._end_personality_test)

        threading.Thread(target=run_tests, daemon=True).start()

    def _end_personality_test(self):
        self.view.hide_personality_test_loading()
        self.view.enable_personality_test_buttons()
        self.personality_test_running = False
        self.view.show_info(
            f"Completed {self.test_counter} tests for all characters. Each character has exactly {NUMBER_OF_TESTS_FOR_STATISTICS} tests. Results saved in {OPENAI_MODEL}.csv")

    def _save_test_results_to_csv(self, character, ipip_scores, accuracy, trait_accuracies, test_duration, responses):
        csv_filename = STATISTICS_FILE
        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            if not file_exists:
                writer.writerow(
                    ['Model', 'Character_Name', 'Target_Extraversion', 'Target_Agreeableness',
                     'Target_Conscientiousness', 'Target_Neuroticism', 'Target_Openness',
                     'Test_Extraversion', 'Test_Agreeableness', 'Test_Conscientiousness',
                     'Test_Neuroticism', 'Test_Openness',
                     'Accuracy_Extraversion', 'Accuracy_Agreeableness', 'Accuracy_Conscientiousness',
                     'Accuracy_Neuroticism', 'Accuracy_Openness', 'Total_Accuracy', 'Duration'] +
                    [f'Q{i}' for i in range(1, 51)])

            writer.writerow([
                                OPENAI_MODEL,
                                character.name,
                                f"{character.extraversion:.2f}",
                                f"{character.agreeableness:.2f}",
                                f"{character.conscientiousness:.2f}",
                                f"{character.neuroticism:.2f}",
                                f"{character.openness:.2f}",
                                f"{ipip_scores['Extraversion'] / 100:.2f}",
                                f"{ipip_scores['Agreeableness'] / 100:.2f}",
                                f"{ipip_scores['Conscientiousness'] / 100:.2f}",
                                f"{ipip_scores['Neuroticism'] / 100:.2f}",
                                f"{ipip_scores['Openness'] / 100:.2f}",
                                f"{trait_accuracies['Extraversion']:.2f}",
                                f"{trait_accuracies['Agreeableness']:.2f}",
                                f"{trait_accuracies['Conscientiousness']:.2f}",
                                f"{trait_accuracies['Neuroticism']:.2f}",
                                f"{trait_accuracies['Openness']:.2f}",
                                f"{accuracy:.2f}",
                                f"{test_duration:.2f}".replace('.', ',')
                            ] + responses)

    def _calculate_accuracy(self, character, ipip_scores):
        traits = {
            'Extraversion': character.extraversion,
            'Agreeableness': character.agreeableness,
            'Conscientiousness': character.conscientiousness,
            'Neuroticism': character.neuroticism,
            'Openness': character.openness
        }
        trait_accuracies = {}
        total_accuracy = 0
        for trait, expected in traits.items():
            actual = ipip_scores[trait] / 100
            trait_accuracy = 100 - abs(expected - actual) * 100
            trait_accuracies[trait] = trait_accuracy
            total_accuracy += trait_accuracy

        average_accuracy = total_accuracy / len(traits)
        return average_accuracy, trait_accuracies

    def _display_test_result(self, name, ipip_scores, accuracy):
        result_message = f"Test results for {name}:\n"
        for trait, score in ipip_scores.items():
            result_message += f"{trait}: {score:.2f}\n"
        result_message += f"\nAccuracy: {accuracy:.2f}%"
        self.view.add_message_to_chat(result_message, "System")

    def show_test_prompt(self):
        character = self._get_selected_character()
        if not character:
            print("Errore: Nessun personaggio selezionato.")
            return

        full_prompt = self.ipip_test.get_test_prompt()
        full_prompt += get_character_prompt(character)
        full_prompt += "\n\n    - Answers: \n"

        self.view.show_test_prompt_window(full_prompt)

    def analyze_test_responses(self):
        character = self._get_selected_character()
        if not character:
            print("Errore: Nessun personaggio selezionato.")
            return

        responses = self.view.get_test_responses_from_user()
        if not responses:
            print("Nessuna risposta fornita.")
            return

        print("Risposte ricevute:")
        print(responses)

        scores, raw_responses = self.ipip_test.process_response(responses)
        if scores is None:
            print("Errore nell'analisi delle risposte. Controllare il formato delle risposte.")
            return

        print(f"\nRisultati del test per {character.name}:")
        for trait, score in scores.items():
            print(f"{trait}: {score:.2f}")

        accuracy, trait_accuracies = self._calculate_accuracy(character, scores)
        print(f"\nAccuratezza totale: {accuracy:.2f}%")
        for trait, acc in trait_accuracies.items():
            print(f"Accuratezza {trait}: {acc:.2f}%")

        test_duration = 1.0
        self._save_test_results_to_csv(character, scores, accuracy, trait_accuracies, test_duration, raw_responses)

        self.view.show_info(f"Risultati del test per {character.name} salvati nel file CSV.")
