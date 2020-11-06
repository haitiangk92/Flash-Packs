from tkinter import *
from tkinter import ttk
import os
import pickle
import random
import Manny
import Card
import Deck
import Main_Menu
import GameScreen

username = os.getlogin()
path = f"/home/{username}/Documents/Flash Packs"
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
        Manny.center_window(self.root)

    def start(self):
        print(len(decks[0].cards))
        GameScreen.IndexCards(self.root, decks[0])
        #Main_Menu.MainMenu(self.root)
        self.root.mainloop()

    def read_decks(self):        
        try:
            os.mkdir(path)
        except Exception:
            print(f"App Folder Already Exists")

        try:
            directories = os.listdir(f"{path}/Decks")
            for directory in directories:
                if ".deck" in directory:
                    directory = directory[0:len(directory)-5]
                    decks.append(Deck.Deck(directory))
            
            with open(f"{path}/settings.bin","wb") as app_settings:
                settings = {
                    "bg_colors" : ["light grey", "white"],
                    "app_color" :  "light blue",
                    "app_accent_color" : "cyan",
                    "txt_color_1" : "black",
                    "txt_color_2" : "blue",
                    "decks" : decks
                }
                pickle.dump(settings,app_settings)        
        except Exception as ex:
            print(f"No decks made......ever. Error: {ex}")
            try:
                os.mkdir(f"{path}/Decks")
            except Exception:
                print(f"Decks Folder Already Exists")
    
if __name__ == "__main__":
    with open(f"{path}/settings.bin","wb") as app_settings:
        settings = {
            "bg_colors" : ["light grey", "white"],
            "app_color" :  "light blue",
            "app_accent_color" : "cyan",
            "txt_color_1" : "black",
            "txt_color_2" : "blue",
            "decks" : []
        }
        pickle.dump(settings,app_settings)

    flashpack = FlashPacks()
    flashpack.read_decks()
    flashpack.start()