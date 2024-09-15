import tkinter as tk
from settings import *


class LoadingIndicator:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=LOADING_INDICATOR_WIDTH, height=LOADING_INDICATOR_HEIGHT, bg='#2E3440',
                                highlightthickness=0)
        dot_radius = LOADING_INDICATOR_HEIGHT / 2
        dot_color = '#88C0D0'
        dot_spacing = LOADING_INDICATOR_HEIGHT
        self.dots = []
        for i in range(4):
            x0 = LOADING_INDICATOR_HEIGHT / 2 + i * dot_spacing
            y0 = LOADING_INDICATOR_HEIGHT / 2
            x1 = x0 + dot_radius
            y1 = y0 + dot_radius
            dot = self.canvas.create_oval(x0, y0, x1, y1, fill=dot_color)
            self.dots.append(dot)
        self.current_dot = 0
        self.animation_speed = LOADING_INDICATOR_ANIMATION_SPEED
        self.animation_job = None

    def start_animation(self):
        self.canvas.pack()
        self.animate()

    def stop_animation(self):
        if self.animation_job:
            self.master.after_cancel(self.animation_job)
            self.animation_job = None
        self.canvas.pack_forget()

    def animate(self):
        for i, dot in enumerate(self.dots):
            if i == self.current_dot:
                fill_color = '#88C0D0'
            else:
                fill_color = '#4C566A'
            self.canvas.itemconfig(dot, fill=fill_color)
        self.current_dot = (self.current_dot + 1) % len(self.dots)
        self.animation_job = self.master.after(self.animation_speed, self.animate)
