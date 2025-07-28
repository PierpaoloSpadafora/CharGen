import tkinter as tk
from tkinter import ttk
from typing import Union
from language import *


class SimplifiedPersonalityUI:
    def __init__(self, parent):
        self.traits_frame = None
        self.mode_button = None
        self.title_label = None
        self.frame = None
        self.header_frame = None
        self.parent = parent
        self.traits = [EXTRAVERSION_TEXT, AGREEABLENESS_TEXT, CONSCIENTIOUSNESS_TEXT, NEUROTICISM_TEXT, OPENNESS_TEXT]
        self.levels = [
            PERSONALITY_LEVEL_NONE_TEXT, PERSONALITY_LEVEL_VERY_LOW_TEXT, PERSONALITY_LEVEL_LOW_TEXT, PERSONALITY_LEVEL_NEUTRAL_TEXT, PERSONALITY_LEVEL_MODERATE_TEXT, PERSONALITY_LEVEL_HIGH_TEXT, PERSONALITY_LEVEL_VERY_HIGH_TEXT
        ]
        self.level_ranges = {
            PERSONALITY_LEVEL_NONE_TEXT: (0.00, 0.09),
            PERSONALITY_LEVEL_VERY_LOW_TEXT: (0.10, 0.29),
            PERSONALITY_LEVEL_LOW_TEXT: (0.30, 0.41),
            PERSONALITY_LEVEL_NEUTRAL_TEXT: (0.42, 0.58),
            PERSONALITY_LEVEL_MODERATE_TEXT: (0.59, 0.70),
            PERSONALITY_LEVEL_HIGH_TEXT: (0.71, 0.84),
            PERSONALITY_LEVEL_VERY_HIGH_TEXT: (0.85, 1.00)
        }
        self.trait_vars: dict[str, Union[tk.StringVar, tk.DoubleVar]] = {
            trait: tk.StringVar(value=PERSONALITY_LEVEL_NEUTRAL_TEXT) for trait in self.traits
        }
        self.trait_values: dict[str, float] = {trait: 0.5 for trait in self.traits}
        self.trait_entries = {}
        self.trait_scales = {}
        self.advanced_mode = False
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.pack(fill=tk.X)

        self.title_label = ttk.Label(self.header_frame, text=PERSONALITY_TRAITS_TEXT, font=('Helvetica', 12, 'bold'))
        self.title_label.pack(side=tk.LEFT)

        self.mode_button = ttk.Button(self.header_frame, text=ADVANCED_MODE_TEXT, command=self.toggle_mode, width=15)
        self.mode_button.pack(side=tk.RIGHT)

        self.traits_frame = ttk.Frame(self.frame)
        self.traits_frame.pack(fill=tk.BOTH, expand=True)

        self.create_simple_ui()

    def create_simple_ui(self):
        for trait in self.traits:
            trait_frame = ttk.Frame(self.traits_frame)
            trait_frame.pack(fill=tk.X, pady=(0, 2))

            ttk.Label(trait_frame, text=f"{trait.capitalize()}:", width=15, anchor="e").pack(side=tk.LEFT, padx=(0, 5))

            level_frame = ttk.Frame(trait_frame)
            level_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            for level in self.levels:
                rb = ttk.Radiobutton(level_frame, text=level, variable=self.trait_vars[trait], value=level,
                                     command=lambda t=trait, l=level: self.update_trait_value(t, l))
                rb.pack(side=tk.LEFT, padx=2)

    def update_trait_value(self, trait, level):
        self.trait_values[trait] = sum(self.level_ranges[level]) / 2

    def toggle_mode(self):
        self.advanced_mode = not self.advanced_mode
        for widget in self.traits_frame.winfo_children():
            widget.destroy()

        if self.advanced_mode:
            self.create_advanced_ui()
            self.mode_button.config(text=SIMPLE_MODE_TEXT)
        else:
            self.create_simple_ui()
            self.mode_button.config(text=ADVANCED_MODE_TEXT)

        self.update_ui_values()

    def create_advanced_ui(self):
        for trait in self.traits:
            trait_frame = ttk.Frame(self.traits_frame)
            trait_frame.pack(fill=tk.X, pady=2)

            ttk.Label(trait_frame, text=f"{trait.capitalize()}:", width=15, anchor="e").pack(side=tk.LEFT, padx=(0, 5))

            scale = ttk.Scale(trait_frame, from_=0, to=1, orient=tk.HORIZONTAL,
                              length=200, command=lambda v, t=trait: self.update_entry(float(v), t))
            scale.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.trait_scales[trait] = scale

            entry = ttk.Entry(trait_frame, width=5)
            entry.pack(side=tk.RIGHT, padx=(5, 0))
            entry.bind('<FocusOut>', lambda e, t=trait: self.update_scale(t))
            self.trait_entries[trait] = entry

    def update_entry(self, value: float, trait: str):
        rounded_value = round(value, 2)
        self.trait_values[trait] = rounded_value
        self.trait_entries[trait].delete(0, tk.END)
        self.trait_entries[trait].insert(0, f"{rounded_value:.2f}")

    def update_scale(self, trait: str):
        try:
            value = float(self.trait_entries[trait].get())
            if 0 <= value <= 1:
                rounded_value = round(value, 2)
                self.trait_values[trait] = rounded_value
                self.trait_scales[trait].set(rounded_value)
            else:
                raise ValueError
        except ValueError:
            current_value = self.trait_values[trait]
            self.trait_entries[trait].delete(0, tk.END)
            self.trait_entries[trait].insert(0, f"{current_value:.2f}")

    def update_ui_values(self):
        if self.advanced_mode:
            self.update_advanced_ui()
        else:
            self.update_simple_ui()

    def update_advanced_ui(self):
        for trait, value in self.trait_values.items():
            self.trait_scales[trait].set(value)
            self.trait_entries[trait].delete(0, tk.END)
            self.trait_entries[trait].insert(0, f"{value:.2f}")

    def update_simple_ui(self):
        for trait, value in self.trait_values.items():
            level = self.get_closest_level(value)
            self.trait_vars[trait].set(level)

    def get_personality_values(self):
        personality_values = {}
        for trait, value in self.trait_values.items():
            rounded_value = round(value, 2)
            personality_values[trait] = rounded_value

        return personality_values

    def set_trait_values(self, traits):
        for trait, value in traits.items():
            self.trait_values[trait] = value
        self.update_ui_values()

    def get_closest_level(self, value):
        for level, (min_val, max_val) in self.level_ranges.items():
            if min_val <= value <= max_val:
                return level
        return PERSONALITY_LEVEL_NEUTRAL_TEXT

