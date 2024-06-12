from tkinter import *
from tkinter.ttk import Combobox
import pandas as pd

class Program:
    def __init__(self, root):
        self.root = root
        self.root.title('Laliga Players Database')
        self.root.geometry('1080x700')  # Set the window geometry to 1080x700
        
        # Read the player data from CSV
        self.players_data = pd.read_csv(r"C:\Users\jjond\OneDrive\Desktop\Laliga Stats\La_liga\La_liga Stats with Nationalities.csv", encoding='cp1252')
        
        # Initialize a StringVar to track entry changes
        self.entry_var = StringVar()
        self.entry_var.trace("w", self.filter_players)
        
        # Create a Frame to contain the Combobox and Scrollbar
        self.dropdown_frame = Frame(self.root)
        self.dropdown_frame.pack(side=TOP, fill=X)

        # Create a Combobox and a Listbox with Scrollbar
        self.combo_box = Combobox(self.dropdown_frame, width=50, textvariable=self.entry_var)
        self.listbox = Listbox(self.dropdown_frame, width=50, height=5)
        self.scrollbar = Scrollbar(self.dropdown_frame, orient=VERTICAL, command=self.listbox.yview)

        # Populate Combobox and Listbox with player names
        self.populate_listbox()

        # Bind Listbox selection to entry
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Place Combobox and Listbox with Scrollbar
        self.combo_box.pack(side=LEFT, fill=X, expand=True)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Create a Submit button
        self.submit_button = Button(self.root, text='Submit', width=25, font=('Arial', 10), command=self.show_stats)
        self.submit_button.pack(side=TOP, padx=10, pady=10)
        
        # Create a Text widget for displaying player stats
        self.window = Text(self.root, width=100, height=30, wrap=NONE)
        self.window.pack(side=TOP, padx=10, pady=10, fill=BOTH, expand=True)
        
        # Create a horizontal scrollbar for the Text widget
        self.horizontal_scrollbar = Scrollbar(self.root, orient=HORIZONTAL, command=self.window.xview)
        self.horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        
        # Configure the text widget to use the horizontal scrollbar
        self.window.configure(xscrollcommand=self.horizontal_scrollbar.set)
        
    # Method to populate the listbox with player names
    def populate_listbox(self):
        self.listbox.delete(0, END)
        search_term = self.entry_var.get().lower()
        for player in self.players_data['Player'].unique():
            if player.lower().startswith(search_term):
                self.listbox.insert(END, player)

    # Method to filter player names based on entry text
    def filter_players(self, *args):
        self.populate_listbox()

    # Method to handle selection of a player in the listbox
    def on_select(self, event):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            selected_value = self.listbox.get(selected_indices[0])
            self.entry_var.set(selected_value)

    # Method to display player stats when the Submit button is clicked
    def show_stats(self):
        selected_player = self.entry_var.get()
        player_stats = self.players_data[self.players_data['Player'] == selected_player]
        
        # Clear previous stats
        self.window.delete(1.0, END)
        
        # Display stats
        stats_text = player_stats.to_string(index=False, justify='left', col_space=10)
        self.window.insert(END, stats_text)


if __name__ == '__main__':
    root = Tk()
    app = Program(root)
    root.mainloop()
