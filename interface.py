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

    def add_end_point(self, event):
        self.master.polygone_point.append([event.x, event.y])
        self.refresh_canvas()


    def refresh_canvas(self, clear=False):
        if clear == True:
            self.board_canvas.delete("all")
        for i, point in enumerate(self.master.polygone_point):
            if i == 0:
                last_point = point
            else: 
                self.board_canvas.create_line(last_point[0], last_point[1], point[0], point[1], fill="grey", width=1)
                last_point = point
            self.board_canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill="black")
        if self.master.polygone_is_close and i>=2:
            self.board_canvas.create_line(last_point[0], last_point[1], self.master.polygone_point[0][0], self.master.polygone_point[0][1], fill="grey", width=1)

class Frame_right_pannel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.add_end_point_button = ctk.CTkButton(self, text="add point at the end", command=self.add_point_at_the_end)
        self.add_end_point_button.grid(row=0, column=0, pady=4)

        self.supress_point_button = ctk.CTkButton(self, text="supress point")
        self.supress_point_button.grid(row=1, column=0, pady=4)

        self.insert_point_button = ctk.CTkButton(self, text="insert point")
        self.insert_point_button.grid(row=2, column=0, pady=4)

        self.clear_infill_button = ctk.CTkButton(self, text="clear infill")
        self.clear_infill_button.grid(row=3, column=0, pady=4)

        self.clear_polygone_button = ctk.CTkButton(self, text="clear polygone", command=self.clear_polygone)
        self.clear_polygone_button.grid(row=4, column=0, pady=4)

        self.close_polygone_button = ctk.CTkButton(self, text="close polygone", command=self.close_polygone)
        self.close_polygone_button.grid(row=5, column=0, pady=4)

        self.compute_infill_button = ctk.CTkButton(self, text="compute infill")
        self.compute_infill_button.grid(row=6, column=0, pady=4)

    def clear_polygone(self):
        self.master.polygone_point = []
        self.master.polygone_is_close = False
        self.master.display_frame.refresh_canvas(clear=True)

    def close_polygone(self):
        self.master.polygone_is_close = True
        self.master.display_frame.refresh_canvas()

    def add_point_at_the_end(self):
        self.master.display_frame.board_canvas.bind("<Button-1>", self.master.display_frame.add_end_point)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("basic interface to teste infill pattern")
        self.minsize(200, 300)

        self.polygone_is_close = False 
        
        self.polygone_point = []
        self.infill_point = []

        #self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)

        
        self.display_frame = Frame_display_infill(self)
        self.display_frame.pack(side="left", expand=True, fill="both", padx=10)


        self.right_frame = Frame_right_pannel(self)
        self.right_frame.pack(side="right")

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
