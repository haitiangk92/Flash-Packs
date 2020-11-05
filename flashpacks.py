from os import error, name, stat
from tkinter import *
from tkinter import ttk
import os
from datetime import datetime
import pickle
from typing import Counter
import subprocess
from tkinter.scrolledtext import ScrolledText
import random

username = os.getlogin()
res = f"/home/{username}/Documents/Flash Packs"
dim = str(subprocess.check_output("xrandr  | grep \* | cut -d' ' -f4", shell = True)).split("\\n")[0].split("\'")[1].split("x")
decks = []

bg_colors = ["light grey", "white"]
app_color = "light blue"
app_accient_color = "cyan"
txt_color_1 = "black"
txt_color_2 = "blue"

class FlashPacks():
    def __init__(self):
        self.root = Tk()
        self.root.title("Flash Packs")
        self.root.configure(bg = app_color)
        self.root.resizable(height = False, width = False)
        self.root.geometry("1000x600")
        self.root.update()
        self.center_widget(self.root)
        
        self.read_decks()
        #self.main_menu_frame()
        self.deck_frame(decks[0])
        self.root.mainloop()

    def read_decks(self):        
        try:
            os.mkdir(res)
        except Exception:
            print(f"App Folder Already Exists")

        try:
            directories = os.listdir(f"{res}/Decks")
            for directory in directories:
                if ".deck" in directory:
                    directory = directory[0:len(directory)-5]
                    decks.append(Deck(directory))
        except Exception:
            print(f"No decks made......ever")
            try:
                os.mkdir(f"{res}/Decks")
            except Exception:
                print(f"Decks Folder Already Exists")

    def center_widget(self, widget):
        mid_width = int(int(dim[0])/2)
        mid_height = int(int(dim[1])/2)
        w_width = widget.winfo_width()
        w_height = widget.winfo_height()

        widget.geometry(f"{w_width}x{w_height}+{int(mid_width-w_width/2)}+{int(mid_height-w_height/2)}")

    def main_menu_frame(self):
        self.main = Frame(self.root, bg = app_color)

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
        self.name_pop = Toplevel(bg = app_accient_color)
        self.name_pop.title("New Deck")
        self.name_pop.geometry("300x100")
        self.name_pop.update()
        #self.name_pop.bell()
        self.center_widget(self.name_pop)

        name_label = Label(self.name_pop, text = "Name the deck", anchor = W, bg = app_accient_color)
        name_label.pack(fill = BOTH, pady = 15, padx = 20)

        entry_frame = Frame(self.name_pop, bg = app_accient_color)

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
                self.center_widget(error_msg)

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

    def deck_frame(self, deck):
        cards = deck.cards

        if len(cards) > 0:
            self.target_card = cards[int(random.random()*len(cards))]
        else:
            self.target_card = ""

        self.deck_frame = Frame(self.root, bg = "white")
        self.deck_frame.configure(width = 600, height = 400)
        
        cards_frame = Frame(self.deck_frame, bg = "white")

        flash_card = Label(cards_frame, text = self.target_card.face if len(cards) > 0 else "No cards in the Deck",bg = "white")
        flash_card.pack(padx = 80, pady = 80)

        buttons_frame = Frame(cards_frame)
        Button(buttons_frame, text = "Flip Card", command = lambda: flash_card.configure(text = self.flip_card(self.target_card, flash_card["text"]))).grid(row = 0, column = 0)

        Button(buttons_frame, text = "Next", command = lambda: flash_card.configure(text = self.next_card(cards))).grid(row = 0, column = 1)

        Button(buttons_frame, text = "Add Card", command = lambda: self.add_card(deck, cards)).grid(row = 0, column = 2)

        buttons_frame.pack()
        cards_frame.pack()
        self.deck_frame.pack(pady = 100)

    def flip_card(self, card, current):
        return card.content if current == card.face else card.face

    def next_card(self, deck):
        self.target_card = deck[int(random.random()*len(deck))]
        return self.target_card.face

    def add_card(self, deck, cards):
        self.new_card_pop_up = Toplevel()
        self.new_card_pop_up.title("New Card")

        Label(self.new_card_pop_up, text = "Front").pack()
        face = Entry(self.new_card_pop_up)
        face.pack()
        Label(self.new_card_pop_up, text = "Back").pack()
        content = Entry(self.new_card_pop_up)
        content.pack()
        Button(self.new_card_pop_up, text = "OK", command = lambda: self.add_card_ok(face.get(), content.get(), deck, cards)).pack()

    def add_card_ok(self, face, content, deck, cards):
        new_card = Card(face,content)
        deck.add_card(new_card)
        self.new_card_pop_up.destroy()
        cards.append(new_card)


class Deck():
    def __init__(self, name):
        self.deck_name = name
        self.last_studied = "N/A"
        self.cards = []
        self.times_studied = 0

        try:
            with open(f"{res}/Decks/{name}.deck", 'rb') as deck:
                while True:
                    try:    
                        card = pickle.load(deck)
                        self.cards.append(card)
                    except EOFError:
                        break
            with open(f"{res}/Decks/{name}.stat", 'rb') as deck_stats:
                try:
                    stats = pickle.load(deck_stats)
                    self.last_studied = stats["last"]
                    self.times_studied = stats["studied"]
                except Exception:
                    print("error")
        except Exception as ex:
            self.update_time()
            open(f"{res}/Decks/{name}.deck", 'wb')
            with open(f"{res}/Decks/{name}.stat","wb") as deck_stats:
                stats = {
                    "last": self.last_studied,
                    "num": len(self.cards),
                    "studied" : self.times_studied
                }
                pickle.dump(stats,deck_stats)

    def update_time(self):
        self.last_studied = datetime.now().strftime("%m/%d/%y %H:%M")
            
    def add_card(self,card):
        with open(f"{res}/Decks/{self.deck_name}.deck", 'ab') as deck:
            pickle.dump(card,deck)
            self.cards.append(card)

    def save_deck(self):
        with open(f"{res}/Decks/{self.deck_name}.deck", 'wb') as deck:
                for card in self.cards:
                    pickle.dump(card,deck)
        
        with open(f"{res}/Decks/{self.deck_name}.stat","wb") as deck_stats:
                stats = {
                    "last": self.last_studied,
                    "num": len(self.cards),
                    "studied" : self.times_studied
                }
                pickle.dump(stats,deck_stats)
    
    def remove_card(self,removed_card):
        self.cards.remove(removed_card)
        self.save_deck()

class Card():
    def __init__(self,face,content):
        self.face = face
        self.content = content
    
if __name__ == "__main__":
    helper = FlashPacks()