import pyperclip
import tkinter as tk
from typing import Dict, Callable
from tkinter import ttk, messagebox, scrolledtext
from settings import *
from language import *
from loading_indicator import LoadingIndicator
from simplified_personality_ui import SimplifiedPersonalityUI


class CharacterCreatorView:
    def __init__(self, master: tk.Tk):
        self.listbox = None
        self.notebook = None
        self.chat_text = None
        self.chat_entry = None
        self.chat_frame = None
        self.send_button = None
        self.edit_button = None
        self.progress_bar = None
        self.info_windows = None
        self.edit_windows = None
        self.delete_button = None
        self.backstory_text = None
        self.view_info_button = None
        self.character_select = None
        self.make_stats_button = None
        self.chat_spacer_frame = None
        self.list_spacer_frame = None
        self.clear_chat_button = None
        self.character_list_frame = None
        self.copy_backstory_button = None
        self.multiple_tests_button = None
        self.save_character_button = None
        self.character_spacer_frame = None
        self.chat_loading_indicator = None
        self.create_character_frame = None
        self.show_test_prompt_button = None
        self.select_random_character = None
        self.personality_test_button = None
        self.simplified_personality_ui = None
        self.test_all_characters_button = None
        self.generate_random_traits_button = None
        self.analyze_test_responses_button = None
        self.generate_random_backstory_button = None
        self.generate_random_characters_button = None
        self.create_character_loading_indicator = None
        self.personality_test_loading_indicator = None
        self.master = master
        self.info_windows = {}
        self.setup_main_window()
        self.create_widgets()
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        styles = {
            'TFrame': {'background': '#2E3440'},
            'TNotebook': {'background': '#2E3440'},
            'TNotebook.Tab': {'background': '#3B4252', 'foreground': '#ECEFF4', 'padding': [15, 5]},
            'TButton': {'background': '#5E81AC', 'foreground': '#ECEFF4', 'padding': 10, 'font': ('Helvetica', 12)},
            'TLabel': {'background': '#2E3440', 'foreground': '#ECEFF4', 'font': ('Helvetica', 12)},
            'TEntry': {'fieldbackground': '#3B4252', 'foreground': '#ECEFF4', 'font': ('Helvetica', 12)},
            'Horizontal.TScale': {'background': '#2E3440', 'troughcolor': '#4C566A'},
            'TCombobox': {'fieldbackground': '#3B4252', 'background': '#4C566A', 'foreground': '#ECEFF4',
                          'arrowcolor': '#ECEFF4'},
            'Vertical.TScrollbar': {'background': '#4C566A', 'troughcolor': '#3B4252', 'width': 16},
        }

        for widget, options in styles.items():
            style.configure(widget, **options)

        style.map('TNotebook.Tab', background=[('selected', '#4C566A')], foreground=[('selected', '#88C0D0')])
        style.map('TButton', background=[('active', '#81A1C1')])
        style.map('TCombobox', fieldbackground=[('readonly', '#3B4252')], selectbackground=[('readonly', '#4C566A')])
        style.map('Vertical.TScrollbar', background=[('active', '#5E81AC')])

    def setup_main_window(self):
        self.master.title(CHARACTER_CREATOR_TITLE_TEXT)
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.center_window(self.master, WINDOW_WIDTH, WINDOW_HEIGHT)

    def create_widgets(self):
        self.create_notebook()
        self.chat_tab()
        self.create_character_tab()
        self.character_list_tab()
        self.create_loading_indicators()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.chat_frame = ttk.Frame(self.notebook)
        self.create_character_frame = ttk.Frame(self.notebook)
        self.character_list_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.chat_frame, text=CHAT_TEXT)
        self.notebook.add(self.create_character_frame, text=CREATE_CHARACTER_TEXT)
        self.notebook.add(self.character_list_frame, text=CHARACTER_LIST_TEXT)

    def chat_tab(self):
        chat_container = ttk.Frame(self.chat_frame)
        chat_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.chat_text = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD, bg='#3B4252', fg='#ECEFF4',
                                                   font=('Helvetica', 12))
        self.chat_text.pack(expand=True, fill=tk.BOTH)
        self.chat_text.config(state=tk.DISABLED)

        self.chat_spacer_frame = ttk.Frame(chat_container, height=30)
        self.chat_spacer_frame.pack(fill=tk.X)

        self.create_chat_controls()

    def create_chat_controls(self):
        select_frame = ttk.Frame(self.chat_frame)
        select_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(select_frame, text=SELECT_CHARACTER_TEXT).pack(side=tk.LEFT)
        self.character_select = ttk.Combobox(select_frame, state="readonly", width=30)
        self.character_select.pack(side=tk.LEFT, padx=(10, 0))

        self.select_random_character = ttk.Button(select_frame, text=RANDOM_CHARACTER_TEXT, width=10)
        self.select_random_character.pack(side=tk.LEFT, padx=(10, 0))

        self.clear_chat_button = ttk.Button(select_frame, text=CLEAR_CHAT_TEXT, width=15)
        self.clear_chat_button.pack(side=tk.RIGHT)

        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        self.chat_entry = ttk.Entry(input_frame)
        self.chat_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.send_button = ttk.Button(input_frame, text=SEND_TEXT, width=15)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def create_character_tab(self):
        character_container = ttk.Frame(self.create_character_frame)
        character_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        self.create_name_and_profile_container(character_container)
        self.create_personality_traits_section(character_container)
        self.create_character_backstory_section(character_container)

        self.character_spacer_frame = ttk.Frame(character_container, height=30)
        self.character_spacer_frame.pack(fill=tk.X, pady=10)

        self.create_character_buttons(character_container)

    def create_name_and_profile_container(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        self.create_name_textfield(top_frame)
        self.create_profile_combobox(top_frame)

    def create_name_textfield(self, parent):
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(name_frame, text=CHARACTER_NAME_TEXT, font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def create_profile_combobox(self, parent):
        profile_frame = ttk.Frame(parent)
        profile_frame.pack(fill=tk.X, pady=5)
        ttk.Label(profile_frame, text=PREDEFINED_PROFILE_TEXT, font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        self.profile_select = ttk.Combobox(profile_frame, state="readonly")
        self.profile_select.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def create_personality_traits_section(self, parent):
        middle_frame = ttk.Frame(parent)
        middle_frame.pack(fill=tk.X, pady=(0, 10))
        self.simplified_personality_ui = SimplifiedPersonalityUI(middle_frame)

    def create_character_backstory_section(self, parent):
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(expand=True, fill=tk.X)

        backstory_frame = ttk.Frame(bottom_frame)
        backstory_frame.pack(fill=tk.X, pady=(0, 5))

        label_frame = ttk.Frame(backstory_frame)
        label_frame.pack(fill=tk.X)

        ttk.Label(label_frame, text=CHARACTER_BACKSTORY_TEXT, font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT)
        self.copy_backstory_button = ttk.Button(label_frame, text=COPY_TEXT, width=10, command=self.copy_backstory)
        self.copy_backstory_button.pack(side=tk.RIGHT)

        self.backstory_text = scrolledtext.ScrolledText(backstory_frame, wrap=tk.WORD, height=10)
        self.backstory_text.pack(fill=tk.X, expand=False, pady=(10, 0))

        self.update_copy_button_state()
        self.backstory_text.bind("<<Modified>>", lambda e: self.update_copy_button_state())

    def update_copy_button_state(self):
        text_content = self.backstory_text.get("1.0", tk.END).strip()
        if text_content:
            state = tk.NORMAL
        else:
            state = tk.DISABLED
        self.copy_backstory_button.config(state=state)

    def create_character_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.BOTH, pady=(5, 0))

        self.generate_random_traits_button = ttk.Button(button_frame, text=GENERATE_RANDOM_TRAITS_TEXT)
        self.generate_random_traits_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.generate_random_backstory_button = ttk.Button(button_frame, text=GENERATE_RANDOM_BACKSTORY_TEXT)
        self.generate_random_backstory_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        self.save_character_button = ttk.Button(button_frame, text=SAVE_CHARACTER_TEXT)
        self.save_character_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        self.generate_random_characters_button = ttk.Button(button_frame, text=GENERATE_RANDOM_CHARACTERS_TEXT)
        self.generate_random_characters_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def character_list_tab(self):
        list_frame = ttk.Frame(self.character_list_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox = tk.Listbox(list_frame, bg='#3B4252', fg='#ECEFF4',
                                  selectbackground='#5E81AC', font=('Helvetica', 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.create_character_list_buttons()

    def create_character_list_buttons(self):
        button_frame = ttk.Frame(self.character_list_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        buttons = [
            (DELETE_CHARACTER_TEXT, 'delete_button'),
            (EDIT_CHARACTER_TEXT, 'edit_button'),
            (VIEW_INFO_TEXT, 'view_info_button'),
            (PERSONALITY_TEST_TEXT, 'personality_test_button'),
            (RUN_MULTIPLE_TESTS_TEXT, 'multiple_tests_button'),
            (TEST_ALL_CHARACTERS_TEXT, 'test_all_characters_button'),
            (SHOW_TEST_PROMPT_TEXT, 'show_test_prompt_button'),
            (ANALYZE_TEST_RESPONSES_TEXT, 'analyze_test_responses_button'),
            (MAKE_STATS_TEXT, 'make_stats_button')
        ]

        for text, attr_name in buttons:
            button = ttk.Button(button_frame, text=text)
            button.pack(pady=5, fill=tk.X)
            setattr(self, attr_name, button)

        self.list_spacer_frame = ttk.Frame(button_frame, height=30)
        self.list_spacer_frame.pack(fill=tk.X, pady=10)

        self.create_progress_bar(button_frame)

    def create_progress_bar(self, parent):
        self.progress_bar = ttk.Progressbar(parent, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)
        self.progress_bar.pack_forget()

    def create_loading_indicators(self):
        self.chat_loading_indicator = LoadingIndicator(self.chat_spacer_frame)
        self.create_character_loading_indicator = LoadingIndicator(self.character_spacer_frame)
        self.personality_test_loading_indicator = LoadingIndicator(self.list_spacer_frame)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def copy_backstory(self):
        backstory = self.backstory_text.get("1.0", tk.END).strip()
        pyperclip.copy(backstory)
        messagebox.showinfo(COPIED_TEXT, BACKSTORY_COPIED_TEXT)

    def disable_chat_buttons(self):
        buttons = [self.select_random_character,
                   self.clear_chat_button,
                   self.send_button]
        for button in buttons:
            button.config(state=tk.DISABLED)

    def enable_chat_buttons(self):
        buttons = [self.select_random_character,
                   self.clear_chat_button,
                   self.send_button]
        for button in buttons:
            button.config(state=tk.NORMAL)

    def disable_character_generation_buttons(self):
        buttons = [self.generate_random_traits_button,
                   self.generate_random_backstory_button,
                   self.save_character_button,
                   self.generate_random_characters_button]
        for button in buttons:
            button.config(state=tk.DISABLED)

    def enable_character_generation_buttons(self):
        buttons = [self.generate_random_traits_button,
                   self.generate_random_backstory_button,
                   self.save_character_button,
                   self.generate_random_characters_button]
        for button in buttons:
            button.config(state=tk.NORMAL)

    def disable_personality_test_buttons(self):
        buttons = [self.delete_button,
                   self.edit_button,
                   self.view_info_button,
                   self.personality_test_button,
                   self.multiple_tests_button,
                   self.test_all_characters_button]
        for button in buttons:
            button.config(state=tk.DISABLED)

    def enable_personality_test_buttons(self):
        buttons = [self.delete_button,
                   self.edit_button,
                   self.view_info_button,
                   self.personality_test_button,
                   self.multiple_tests_button,
                   self.test_all_characters_button]
        for button in buttons:
            button.config(state=tk.NORMAL)

    def disable_make_stats_button(self):
        buttons = [self.delete_button,
                   self.edit_button,
                   self.view_info_button,
                   self.personality_test_button,
                   self.multiple_tests_button,
                   self.test_all_characters_button,
                   self.make_stats_button]
        for button in buttons:
            button.config(state=tk.DISABLED)

    def enable_make_stats_button(self):
        buttons = [self.delete_button,
                   self.edit_button,
                   self.view_info_button,
                   self.personality_test_button,
                   self.multiple_tests_button,
                   self.test_all_characters_button,
                   self.make_stats_button]
        for button in buttons:
            button.config(state=tk.NORMAL)

    def set_character_basic_traits(self, character_or_profile):
        if isinstance(character_or_profile, dict):
            self.name_entry.delete(0, tk.END)

            traits = character_or_profile
        else:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, character_or_profile.name)

            traits = {
                EXTRAVERSION_TEXT: character_or_profile.extraversion,
                AGREEABLENESS_TEXT: character_or_profile.agreeableness,
                CONSCIENTIOUSNESS_TEXT: character_or_profile.conscientiousness,
                NEUROTICISM_TEXT: character_or_profile.neuroticism,
                OPENNESS_TEXT: character_or_profile.openness
            }

        self.simplified_personality_ui.set_trait_values(traits)

        # Clear the backstory for both cases
        self.backstory_text.delete("1.0", tk.END)
        if not isinstance(character_or_profile, dict):
            self.backstory_text.insert(tk.END, character_or_profile.backstory)

    def set_character_backstory(self, backstory: str):
        self.backstory_text.delete("1.0", tk.END)
        self.backstory_text.insert(tk.END, backstory)

    def clear_character_info(self):
        self.name_entry.delete(0, tk.END)
        self.simplified_personality_ui.set_trait_values({trait: 0.5 for trait in self.simplified_personality_ui.traits})
        self.backstory_text.delete("1.0", tk.END)
        self.profile_select.set(CUSTOM_TEXT)

    def get_character_info(self):
        return self.simplified_personality_ui.get_personality_values()

    def refresh_character_list(self, characters):
        self.listbox.delete(0, tk.END)
        for _, name in characters:
            self.listbox.insert(tk.END, name)
        self.character_select['values'] = [name for _, name in characters]
        self.preselect_first_character()

    def get_selected_character(self):
        selection = self.listbox.curselection()
        return self.listbox.get(selection[0]) if selection else ""

    def get_selected_chat_character(self):
        return self.character_select.get()

    def preselect_first_character(self):
        if self.listbox.size() > 0:
            self.listbox.select_set(0)
            self.listbox.event_generate("<<ListboxSelect>>")

    def get_chat_input(self):
        return self.chat_entry.get()

    def clear_chat_input(self):
        self.chat_entry.delete(0, tk.END)

    def add_message_to_chat(self, message: str, sender: str):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def clear_chat(self):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def show_loading(self):
        self.create_character_loading_indicator.start_animation()

    def hide_loading(self):
        self.create_character_loading_indicator.stop_animation()

    def show_chat_loading(self):
        self.chat_loading_indicator.canvas.pack(in_=self.chat_spacer_frame, pady=5)
        self.chat_loading_indicator.start_animation()

    def hide_chat_loading(self):
        self.chat_loading_indicator.stop_animation()
        self.chat_loading_indicator.canvas.pack_forget()

    def show_personality_test_loading(self):
        self.progress_bar['value'] = 0
        self.progress_bar.pack(pady=5, fill=tk.X)
        self.personality_test_loading_indicator.canvas.pack(pady=5)
        self.personality_test_loading_indicator.start_animation()

    def hide_personality_test_loading(self):
        self.personality_test_loading_indicator.stop_animation()
        self.personality_test_loading_indicator.canvas.pack_forget()
        self.progress_bar.pack_forget()

    def update_progress_bar(self, value):
        self.progress_bar['value'] = value
        if value >= 100:
            self.progress_bar.pack_forget()
        else:
            self.progress_bar.pack(pady=5, fill=tk.X)

    def create_edit_window(self, character, save_callback: Callable):
        if not hasattr(self, 'edit_windows') or self.edit_windows is None:
            self.edit_windows = {}

        if character and character.id is not None:
            if character.id in self.edit_windows:
                existing_window = self.edit_windows[character.id]
                if existing_window.winfo_exists():
                    existing_window.lift()
                    return
                else:
                    del self.edit_windows[character.id]

        self.close_all_windows()

        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"{EDIT_TEXT} {character.name if character else 'Unknown'}")
        edit_window.configure(bg='#2E3440')
        self.center_window(edit_window, 500, 600)

        self.create_edit_fields(edit_window, character, save_callback)
        if character and character.id is not None:
            self.edit_windows[character.id] = edit_window

        close_func = lambda: self.close_edit_window(character.id if character and character.id is not None else None)
        self.set_esc_handler(edit_window, close_func)
        edit_window.protocol("WM_DELETE_WINDOW", close_func)

        edit_window.focus_set()

    def set_trait_values(self, traits):
        self.simplified_personality_ui.set_trait_values(traits)

    def create_edit_fields(self, edit_window, character, save_callback):
        main_frame = ttk.Frame(edit_window, padding=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Name:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        name_entry = ttk.Entry(main_frame, font=('Helvetica', 12))
        name_entry.insert(0, character.name)
        name_entry.pack(fill=tk.X, pady=(0, 10))

        traits_frame = ttk.Frame(main_frame)
        traits_frame.pack(fill=tk.X, pady=(0, 10))
        simplified_personality_ui = SimplifiedPersonalityUI(traits_frame)

        traits = {
            OPENNESS_TEXT: character.openness,
            CONSCIENTIOUSNESS_TEXT: character.conscientiousness,
            EXTRAVERSION_TEXT: character.extraversion,
            AGREEABLENESS_TEXT: character.agreeableness,
            NEUROTICISM_TEXT: character.neuroticism
        }
        self.simplified_personality_ui.set_trait_values(traits)

        ttk.Label(main_frame, text="Backstory:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        backstory_text = scrolledtext.ScrolledText(main_frame, height=10, font=('Helvetica', 11))
        backstory_text.insert(tk.END, character.backstory)
        backstory_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        def save_changes():
            new_name = name_entry.get()
            new_traits = simplified_personality_ui.get_personality_values()
            new_backstory = backstory_text.get("1.0", tk.END).strip()
            save_callback(character.id, new_name, new_traits, new_backstory, edit_window)

        ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT)

    def show_character_info(self, character, similarity):
        if not hasattr(self, 'info_windows'):
            self.info_windows = {}

        self.close_all_windows()

        info_window = tk.Toplevel(self.master)
        info_window.title(f"{CHARACTER_INFO_TEXT} {character.name if character else 'Unknown'}")
        info_window.configure(bg='#2E3440')
        self.center_window(info_window, 400, 450)

        self.create_character_info_widgets(info_window, character, similarity)
        if character and character.id is not None:
            self.info_windows[character.id] = info_window

        close_func = lambda: self.close_info_window(character.id if character else None)
        self.set_esc_handler(info_window, close_func)
        info_window.protocol("WM_DELETE_WINDOW", close_func)

        info_window.focus_set()

    def get_selected_profile(self):
        return self.profile_select.get()

    def create_character_info_widgets(self, info_window, character, similarity):
        ttk.Label(info_window, text=f"Name: {character.name}", font=('Helvetica', 14, 'bold')).pack(pady=10)

        for trait in [EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, CONSCIENTIOUSNESS_TEXT, NEUROTICISM_TEXT, OPENNESS_TEXT]:
            value = getattr(character, trait.lower())
            ttk.Label(info_window, text=f"{trait.capitalize()}: {value:.2f}").pack(pady=5)

        self.create_character_info_backstory(info_window, character)

        ttk.Button(info_window, text=CLOSE_TEXT, command=info_window.destroy).pack(pady=20)

    def create_character_info_backstory(self, info_window, character):
        backstory_frame = ttk.Frame(info_window)
        backstory_frame.pack(pady=10, padx=20, fill=tk.X)

        ttk.Label(backstory_frame, text=CHARACTER_BACKSTORY_TEXT).pack(side=tk.TOP, anchor=tk.W)

        backstory_text = scrolledtext.ScrolledText(backstory_frame, height=5, wrap=tk.WORD, bg='#3B4252', fg='#ECEFF4')
        backstory_text.insert(tk.END, character.backstory)
        backstory_text.config(state=tk.DISABLED)
        backstory_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        copy_backstory_button = ttk.Button(backstory_frame, text=COPY_TEXT, width=10,
                                           command=lambda: self.copy_edit_backstory(backstory_text))
        copy_backstory_button.pack(side=tk.RIGHT, padx=(5, 0), anchor=tk.N)

    def copy_edit_backstory(self, backstory_text):
        backstory = backstory_text.get("1.0", tk.END).strip()
        pyperclip.copy(backstory)
        messagebox.showinfo(COPIED_TEXT, BACKSTORY_COPIED_TEXT)

    def close_all_windows(self):
        if hasattr(self, 'edit_windows') and self.edit_windows is not None:
            for window in list(self.edit_windows.values()):
                if window and window.winfo_exists():
                    window.destroy()
            self.edit_windows.clear()
        if hasattr(self, 'info_windows') and self.info_windows is not None:
            for window in list(self.info_windows.values()):
                if window and window.winfo_exists():
                    window.destroy()
            self.info_windows.clear()

    def close_edit_window(self, char_id):
        if char_id is not None and hasattr(self, 'edit_windows') and char_id in self.edit_windows:
            if self.edit_windows[char_id].winfo_exists():
                self.edit_windows[char_id].destroy()
            del self.edit_windows[char_id]

    def close_info_window(self, char_id):
        if hasattr(self, 'info_windows') and char_id in self.info_windows:
            self.info_windows[char_id].destroy()
            del self.info_windows[char_id]

    def set_esc_handler(self, window, close_function):
        window.bind('<Escape>', lambda event: close_function())

    def show_custom_dialog(self, title: str, message: str, dialog_type: str) -> bool:
        dialog = tk.Toplevel(self.master)
        dialog.title(title)
        dialog.geometry(f"{DIALOG_WIDTH}x{DIALOG_HEIGHT}")
        dialog.resizable(False, False)
        self.center_window(dialog, DIALOG_WIDTH, DIALOG_HEIGHT)
        dialog.configure(bg='#2E3440')

        content_frame = ttk.Frame(dialog, style='Dialog.TFrame')
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        label = ttk.Label(content_frame, text=message, wraplength=260,
                          justify=tk.CENTER, style='Dialog.TLabel')
        label.pack(expand=True, fill=tk.BOTH)

        button_frame = ttk.Frame(content_frame, style='Dialog.TFrame')
        button_frame.pack(side=tk.BOTTOM, pady=(10, 0))

        result = tk.BooleanVar(value=False)

        if dialog_type == "yesno":
            yes_button = ttk.Button(button_frame, text="Yes",
                                    command=lambda: self._set_dialog_result(dialog, result, True),
                                    style='Dialog.TButton', width=8)
            yes_button.pack(side=tk.LEFT, padx=(0, 5))

            no_button = ttk.Button(button_frame, text="No",
                                   command=lambda: self._set_dialog_result(dialog, result, False),
                                   style='Dialog.TButton', width=8)
            no_button.pack(side=tk.LEFT, padx=(5, 0))

            dialog.bind('<Return>', lambda e: self._set_dialog_result(dialog, result, True))
        else:
            ok_button = ttk.Button(button_frame, text="OK",
                                   command=lambda: self._set_dialog_result(dialog, result, True),
                                   style='Dialog.TButton', width=8)
            ok_button.pack(side=tk.LEFT)

            dialog.bind('<Return>', lambda e: self._set_dialog_result(dialog, result, True))

        self._setup_dialog_styles()

        dialog.protocol("WM_DELETE_WINDOW", lambda: self._set_dialog_result(dialog, result, False))
        dialog.bind('<Escape>', lambda e: self._set_dialog_result(dialog, result, False))

        dialog.transient(self.master)
        dialog.grab_set()
        dialog.focus_set()
        self.master.wait_window(dialog)

        return result.get()

    def _set_dialog_result(self, dialog: tk.Toplevel, result_var: tk.BooleanVar, value: bool):
        result_var.set(value)
        dialog.destroy()

    def _setup_dialog_styles(self):
        style = ttk.Style()
        style.configure('Dialog.TFrame', background='#2E3440')
        style.configure('Dialog.TLabel', background='#2E3440', foreground='#ECEFF4',
                        font=('Helvetica', 12), wraplength=260)
        style.configure('Dialog.TButton', background='#5E81AC', foreground='#ECEFF4',
                        padding=(10, 5), font=('Helvetica', 10))
        style.map('Dialog.TButton', background=[('active', '#81A1C1')])

    def show_error(self, message: str):
        self.show_custom_dialog(ERROR_TEXT, message, "ok")

    def show_info(self, message: str):
        self.show_custom_dialog(INFORMATION_TEXT, message, "ok")

    def show_confirm(self, message: str) -> bool:
        return self.show_custom_dialog(CONFIRM_TEXT, message, "yesno")

    def show_incomplete_fields_warning(self):
        messagebox.showwarning(INCOMPLETE_FIELDS_TEXT, ASK_TO_COMPLETE_FIELDS_TEXT)

    def set_predefined_profiles(self, profiles: Dict[str, Dict[str, float]]):
        self.profile_select['values'] = list(profiles.keys()) + [CUSTOM_TEXT]
        self.profile_select.set(CUSTOM_TEXT)

    def setup_event_handlers(self, controller):
        self.generate_random_traits_button.config(command=controller.generate_random_character_basics)
        self.generate_random_backstory_button.config(command=controller.generate_random_backstory)
        self.save_character_button.config(command=controller.save_character)
        self.delete_button.config(command=controller.delete_character)
        self.edit_button.config(command=controller.edit_character)
        self.clear_chat_button.config(command=controller.clear_chat)
        self.personality_test_button.config(command=controller.run_personality_test)
        self.multiple_tests_button.config(command=controller.run_multiple_personality_tests)
        self.generate_random_characters_button.config(command=controller.generate_random_characters)
        self.test_all_characters_button.config(command=controller.test_all_characters)
        self.view_info_button.config(command=controller.view_character_info)
        self.send_button.config(command=controller.send_chat_message)
        self.show_test_prompt_button.config(command=controller.show_test_prompt)
        self.analyze_test_responses_button.config(command=controller.analyze_test_responses)
        self.make_stats_button.config(command=controller.make_stats)
        self.chat_entry.bind('<Return>', lambda event: controller.send_chat_message())
        self.character_select.bind("<<ComboboxSelected>>", controller.on_chat_character_selected)
        self.profile_select.bind("<<ComboboxSelected>>", controller.apply_predefined_profile)

    def setup_keyboard_shortcuts(self, controller):
        self.master.bind('<Control-Key-1>', lambda e: self.notebook.select(0))
        self.master.bind('<Control-Key-2>', lambda e: self.notebook.select(1))
        self.master.bind('<Control-Key-3>', lambda e: self.notebook.select(2))

        def execute_if_character_list_selected(func):
            def wrapper(e):
                if self.notebook.index(self.notebook.select()) == 2:
                    func()
            return wrapper

        self.master.bind('<Delete>', execute_if_character_list_selected(controller.delete_character))
        self.master.bind('<Control-i>', execute_if_character_list_selected(controller.view_character_info))
        self.master.bind('<Control-e>', execute_if_character_list_selected(controller.edit_character))
        self.master.bind('<Control-t>', execute_if_character_list_selected(controller.run_personality_test))

    def show_results_window(self, result_message: str):
        results_window = tk.Toplevel(self.master)
        results_window.title(DIVERSE_CHARACTERS_TEST_RESULTS_TEXT)
        results_window.geometry(f"{DIALOG_WIDTH*2}x{DIALOG_HEIGHT*1.3}")
        self.center_window(results_window, DIALOG_WIDTH*2, DIALOG_HEIGHT*1.3)

        text_widget = scrolledtext.ScrolledText(results_window, wrap=tk.WORD, width=80, height=20)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        text_widget.insert(tk.END, result_message)
        text_widget.config(state=tk.DISABLED)

        close_button = ttk.Button(results_window, text=CLOSE_TEXT, command=results_window.destroy)
        close_button.pack(pady=10)

    def get_test_responses_from_user(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Enter your test answers")
        dialog.geometry("500x500")

        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=50, height=15)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        result = tk.StringVar()

        def on_submit():
            result.set(text_widget.get("1.0", tk.END).strip())
            dialog.destroy()

        submit_button = ttk.Button(dialog, text="Analyze", command=on_submit)
        submit_button.pack(pady=10)

        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)

        return result.get()

    def show_test_prompt_window(self, prompt):
        prompt_window = tk.Toplevel(self.master)
        prompt_window.title("Test Prompt")
        prompt_window.geometry("800x700")
        self.center_window(prompt_window, 800, 700)

        text_widget = scrolledtext.ScrolledText(prompt_window, wrap=tk.WORD, width=80, height=30)
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        text_widget.insert(tk.END, prompt)
        text_widget.config(state=tk.DISABLED)

        close_button = ttk.Button(prompt_window, text=CLOSE_TEXT, command=prompt_window.destroy)
        close_button.pack(pady=10)

        def copy_and_close():
            self.copy_to_clipboard(prompt)
            prompt_window.destroy()

        copy_button = ttk.Button(prompt_window, text=COPY_TEXT, command=copy_and_close)
        copy_button.pack(pady=10)

        prompt_window.bind('<Escape>', lambda e: prompt_window.destroy())

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        self.show_info("Prompt copied to clipboard!")
