import customtkinter as ctk
import tkinter as tk
import square_generation as oscar
import logging
import numpy as np
#import cv2 as cv # No need thanks to oscar 
#import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class Frame_display_infill(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.board_canvas = ctk.CTkCanvas(self, width=600, height=600, bg="lightblue")
        self.board_canvas.pack(expand=True, fill='both')
        self.action_to_performe_during_refreshing = []


    def draw_list_of_point(self, l_point, close=False, color_line="grey", color_point="black"):
        for i, point in enumerate(l_point):
            if i == 0:
                last_point = point
            else: 
                self.board_canvas.create_line(last_point[0], last_point[1], point[0], point[1], fill=color_line, width=1)
                last_point = point
            self.board_canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill=color_point)
        if close and i>=2:
            self.board_canvas.create_line(last_point[0], last_point[1], l_point[0][0], l_point[0][1], fill=color_line, width=1)


    def refresh_canvas(self, clear=True):
        if clear:
            self.board_canvas.delete("all")
        for action in self.action_to_performe_during_refreshing:
            action()
            

class teste_interpolation(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.master.master.display_frame.action_to_performe_during_refreshing.append(self.draw_straight_line)

        self.extreme_point_of_line = []
        self.interpolation_square = [] # list of point start : bottom_left, trigo sense, end with center
        self.interpolate_point_line = []
        self.nb_point = 100 # nombre de point calculer dans l'interpolation de la ligne

        self.display_square_bool = ctk.BooleanVar(value=0)
        self.display_interpolate_bool = ctk.BooleanVar(value=0)

        self.select_two_point_button = ctk.CTkButton(self, text="click_two_point", command=self.bind_click_extreme_point)
        self.select_two_point_button.grid(row=0, column=0, pady=2)

        self.display_square_chekebox = ctk.CTkCheckBox(self, text="square", command=self.compute_square, variable=self.display_square_bool, onvalue=1, offvalue=0)
        self.display_square_chekebox.grid(row=1, column=0, pady=2)

        self.display_interpolate_line_chekebox = ctk.CTkCheckBox(self, "lerp line", command=self.compute_interpolation, variable=self.display_interpolate_bool, onvalue=1, offvalue=0)
        self.display_interpolate_line_chekebox.grid(row=2, column=0, pady=2)

    def compute_interpolation(self):
        if len(self.extreme_point_of_line) == 2:
            l_x = np.linspace(self.extreme_point_of_line[0][0], self.extreme_point_of_line[1][0], self.nb_point)
            l_y = np.linspace(self.extreme_point_of_line[0][1], self.extreme_point_of_line[1][1], self.nb_point)
            l_point = np.column_stack((l_x, l_y))

        else:
            logging.warning("impossible de calculer l'interpolation : la ligne ne semble pas complete")

    def compute_square(self):
        if self.master.option_menue["polygone"].polygone_is_close:
            self.interpolation_square = oscar.square(self.master.option_menue["polygone"].polygone_point)
        else: 
            logging.warning("la boounding box n'est pas calculer car le polygone n'est pas fermé")
        
        if self.display_square_bool.get():
            self.master.master.display_frame.action_to_performe_during_refreshing.append(self.display_square)

        elif self.display_square in self.master.master.display_frame.action_to_performe_during_refreshing:
            self.master.master.display_frame.action_to_performe_during_refreshing.remove(self.display_square)

        self.master.master.display_frame.refresh_canvas(clear=True)

    def display_square(self):
        self.master.master.display_frame.draw_list_of_point(self.interpolation_square[:-1], close=True)

    def bind_click_extreme_point(self):
        self.master.master.display_frame.board_canvas.bind("<Button-1>", self.add_extreme_point)

    def add_extreme_point(self, event):
        self.extreme_point_of_line.append([event.x, event.y])
        self.master.master.display_frame.refresh_canvas()
        if len(self.extreme_point_of_line) >= 2:
            self.master.master.display_frame.board_canvas.unbind("<Button-1>")

    def draw_straight_line(self):
        self.master.master.display_frame.draw_list_of_point(self.extreme_point_of_line, color_line="red", color_point="green")

    def exit(self):
        pass
        

class polygone_selection(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.polygone_point = []
        self.polygone_is_close = False

        self.master.master.display_frame.action_to_performe_during_refreshing.append(self.draw_polygone)

        self.add_end_point_button = ctk.CTkButton(self, text="add point at the end", command=self.bind_point_at_the_end)
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
        self.polygone_point = []
        self.polygone_is_close = False
        self.master.master.display_frame.refresh_canvas(clear=True)

    def close_polygone(self):
        self.polygone_is_close = True
        self.master.master.display_frame.refresh_canvas()

    def bind_point_at_the_end(self):
        self.master.master.display_frame.board_canvas.bind("<Button-1>", self.add_end_point)

    def add_end_point(self, event):
        self.polygone_point.append([event.x, event.y])
        self.master.master.display_frame.refresh_canvas()

    def exit(self):
        self.master.master.display_frame.board_canvas.unbind("<Button-1>")

    def draw_polygone(self):
        self.master.master.display_frame.draw_list_of_point(self.polygone_point, self.polygone_is_close)


class Frame_right_pannel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.option_menue = {"polygone":polygone_selection(self), "interpolation":teste_interpolation(self)}
        self.menue = ctk.CTkOptionMenu(self, values=list(self.option_menue.keys()), command=self.switch_frame, fg_color="grey")

        self.menue.grid(row=0, column=0, padx=2, pady=5)
        self.option_menue["polygone"].grid(row=1, column=0)

    def switch_frame(self, selection):
        for frame in list(self.option_menue.values()):
            frame.exit()
            frame.grid_remove()
        self.option_menue[selection].grid(row=1, column=0, padx=0)
    

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("basic interface to teste infill pattern")
        self.minsize(200, 300)

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

