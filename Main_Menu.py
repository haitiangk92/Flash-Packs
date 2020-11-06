from tkinter import *
from tkinter import ttk
import pickle
import os
import Deck
from tkinter.scrolledtext import ScrolledText
import Manny

app_settings = open(f"/home/{os.getlogin()}/Documents/Flash Packs/settings.bin", 'rb') 
try:
    app_settings = pickle.load(app_settings)
    bg_colors = app_settings['bg_colors']
    app_accent_color = app_settings['app_accent_color']
    app_color = app_settings['app_color']
    txt_color_1 = app_settings['txt_color_1']
    txt_color_2 = app_settings['txt_color_2']
    decks = app_settings['decks']
except Exception as ex:
    print(f"Settings Load Error: {ex}")

class MainMenu():
    def __init__(self, root):
        self.main = Frame(root, bg = app_color)

        deck_label = Label(self.main, text = "Choose A Deck", fg = txt_color_1)
        deck_label.configure(width = 110, font = ("Times", 40), anchor = W, bg = app_color)
        deck_label.pack(padx = 35)

        self.deck_list = ScrolledText(self.main)
        self.deck_list.configure(width = 110, height = 20, border = 1, relief = SUNKEN, state = DISABLED)
        self.deck_list.pack()

        self.load_decks()

        buttons_frame = Frame(self.main, bg = app_color)

        add_btn = ttk.Button(buttons_frame, text = "Add New Deck", command = self.create_deck_pop_up)
        add_btn.grid(row = 0, column = 0, padx = 100)

        remove_btn = ttk.Button(buttons_frame, text = "Remove Deck", state = DISABLED)
        remove_btn.grid( row = 0, column = 1, padx = 100)

        study_btn = ttk.Button(buttons_frame, text = "Study Deck", state = DISABLED)
        study_btn.grid(row = 0, column = 2, padx = 100)

        buttons_frame.pack(pady = 35)
        self.main.pack(pady = 20, padx = 20)

    def load_decks(self):
        self.deck_list.configure(state = NORMAL)
        if len(decks) == 0:
            deck_frame = Frame()

            deck_name = Label(deck_frame, text = "No Decks Available", font = ("Times", 30) , fg = txt_color_2, width = 44, anchor = W, bg = "light grey")
            deck_name.pack(fill = BOTH)
            
            deck_cards = Label(deck_frame, text = "Number of cards: N/A", font = ("Times", 10), anchor = W, bg = "light grey")
            deck_cards.pack(fill = BOTH)

            deck_used = Label(deck_frame, text = "Last Studied: N/A", font = ("Times", 10), anchor = W, bg = "lightgrey")
            deck_used.pack(fill = BOTH)

            self.deck_list.window_create(END, window = deck_frame)
            self.deck_list.insert(END, "\n")
        else:
            for i in range(len(decks)):
                self.add_deck(decks[i])
        
        self.deck_list.configure(state = DISABLED)

    def create_deck_pop_up(self):
        self.name_pop = Toplevel(bg = app_accent_color)
        self.name_pop.title("New Deck")
        self.name_pop.geometry("300x100")
        self.name_pop.update()
        #self.name_pop.bell()
        Manny.center_window(self.name_pop)

        name_label = Label(self.name_pop, text = "Name the deck", anchor = W, bg = app_accent_color)
        name_label.pack(fill = BOTH, pady = 15, padx = 20)

        entry_frame = Frame(self.name_pop, bg = app_accent_color)

        self.name_input = Entry(entry_frame)
        self.name_input.focus_set()
        self.name_input.bind("<Return>", self.pop_up_enter_hit)
        self.name_input.grid(row = 0, column = 0, padx = 20)

        enter_btn = ttk.Button(entry_frame, text = "OK", command = self.pop_up_ok_btn_hit)
        enter_btn.grid(row = 0, column = 1)
        
        entry_frame.pack()

        self.name_pop.mainloop()

    def pop_up_enter_hit(self, event):
        self.pop_up_ok_btn_hit()

    def pop_up_ok_btn_hit(self):
        name = self.name_input.get()
        new_deck = Deck(name)

        
        if len(decks) == 0:
            self.deck_list.configure(state = NORMAL)
            self.deck_list.delete(1.0,END)
            self.deck_list.configure(state = DISABLED)

        duplicate_found = False
        for deck in decks:
            if name == deck.deck_name:
                duplicate_found = True
                error_msg = Toplevel()
                error_msg. title("Error")
                error_msg.resizable(width = False, height = False)
                error_msg.geometry("250x20")
                error_msg.update()
                Manny.center_window(error_msg)

                Label(error_msg, text = f'"{name}" Already Exists').pack()

                error_msg.mainloop()
                break

        if not duplicate_found:
            self.name_pop.destroy()
            self.add_deck(new_deck)            

    def add_deck(self,new_deck):
        bg_color = bg_colors[len(decks)%2]

        deck_frame = Frame()

        deck_name = Label(deck_frame, text = new_deck.deck_name, font = ("Times", 30) , fg = txt_color_2, width = 44, anchor = W, bg = bg_color)
        deck_name.pack(fill = BOTH)
        
        deck_cards = Label(deck_frame, text = f"Number of cards: {len(new_deck.cards)}", font = ("Times", 10), anchor = W, bg = bg_color)
        deck_cards.pack(fill = BOTH)

        deck_used = Label(deck_frame, text = f"Last Studied: {new_deck.last_studied}", font = ("Times", 10), anchor = W, bg = bg_color)
        deck_used.pack(fill = BOTH)

        self.deck_list.configure(state = NORMAL)
        self.deck_list.window_create(END, window = deck_frame)
        self.deck_list.insert(END, "\n")
        self.deck_list.configure(state = DISABLED)
    
        decks.append(new_deck)