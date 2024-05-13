import customtkinter as ctk
import tkinter as tk

import numpy as np
import cv2 as cv
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class Frame_display_infill(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.board_canvas = ctk.CTkCanvas(self, width=600, height=600, bg="lightblue")
        self.board_canvas.pack(expand=True, fill='both')

        self.polygone_point = []
        self.infill_point = []



    def refresh_canvas(self):
        pass

class Frame_right_pannel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.add_point_button = ctk.CTkButton(self, text="add point")
        self.add_point_button.grid(row=0, column=0)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("basic interface to teste infill pattern")
        self.minsize(200, 300)
        #self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)

        
        self.display_frame = Frame_display_infill(self)
        self.display_frame.pack(side="left", expand=True, fill="both", padx=10)


        self.right_frame = Frame_right_pannel(self)
        self.right_frame.pack(side="right")

        

if __name__ == "__main__":
    app = App()
    app.mainloop()

