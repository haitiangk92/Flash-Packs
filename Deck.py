import pickle
import os
from datetime import datetime

username = os.getlogin()
path = f"/home/{username}/Documents/Flash Packs"

class Deck():
    def __init__(self, name):
        self.deck_name = name
        self.last_studied = "N/A"
        self.cards = []
        self.times_studied = 0

        try:
            with open(f"{path}/Decks/{name}.deck", 'rb') as deck:
                while True:
                    try:    
                        card = pickle.load(deck)
                        self.cards.append(card)
                    except EOFError:
                        break
            with open(f"{path}/Decks/{name}.stat", 'rb') as deck_stats:
                try:
                    stats = pickle.load(deck_stats)
                    self.last_studied = stats["last"]
                    self.times_studied = stats["studied"]
                except Exception:
                    print("error")
        except Exception as ex:
            self.update_time()
            open(f"{path}/Decks/{name}.deck", 'wb')
            with open(f"{path}/Decks/{name}.stat","wb") as deck_stats:
                stats = {
                    "last": self.last_studied,
                    "num": len(self.cards),
                    "studied" : self.times_studied
                }
                pickle.dump(stats,deck_stats)

    def update_time(self):
        self.last_studied = datetime.now().strftime("%m/%d/%y %H:%M")
            
    def add_card(self,card):
        with open(f"{path}/Decks/{self.deck_name}.deck", 'ab') as deck:
            pickle.dump(card,deck)
            self.cards.append(card)

    def save_deck(self):
        with open(f"{path}/Decks/{self.deck_name}.deck", 'wb') as deck:
                for card in self.cards:
                    pickle.dump(card,deck)
        
        with open(f"{path}/Decks/{self.deck_name}.stat","wb") as deck_stats:
                stats = {
                    "last": self.last_studied,
                    "num": len(self.cards),
                    "studied" : self.times_studied
                }
                pickle.dump(stats,deck_stats)
    
    def remove_card(self,removed_card):
        self.cards.remove(removed_card)
        self.save_deck()