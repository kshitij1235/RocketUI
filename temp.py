import tkinter as tk
from customtkinter import CTkCheckBox

class RocketUI:
    def __init__(self, window):
        self.window = window
        self.create_module(window)

    def create_module(self, parent):
        # Create a frame to center the content horizontally
        frame = tk.Frame(parent, bg="#E4D5B8")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Configure column weights to center the frame horizontally
        parent.grid_columnconfigure(0, weight=1)

        # Add padding and pack labels
        tk.Label(frame, text="", bg="#E4D5B8").pack(pady=10)

        # Create a container frame for the checkboxes to align them in one line
        checkbox_frame = tk.Frame(frame, bg="#E4D5B8")
        checkbox_frame.pack(pady=10, padx=10, fill="x")

        # Configure grid columns in checkbox_frame
        checkbox_frame.grid_columnconfigure(0, weight=1)
        checkbox_frame.grid_columnconfigure(1, weight=1)
        checkbox_frame.grid_columnconfigure(2, weight=1)
        checkbox_frame.grid_columnconfigure(3, weight=1)

        # Place checkboxes in a single line
        CTkCheckBox(checkbox_frame, text="edit the app/main", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        CTkCheckBox(checkbox_frame, text="under the class component system", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        CTkCheckBox(checkbox_frame, text="edit the sequence of main.py", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        CTkCheckBox(checkbox_frame, text="enjoy rocket ui", text_color="black",
                    hover_color="#C29130", fg_color="#C29130").grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(frame, text="", bg="#E4D5B8").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")  
    app = RocketUI(root)
    root.mainloop()
