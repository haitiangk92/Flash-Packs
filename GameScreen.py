from tkinter import *
import random
import Card

class IndexCards():
    def __init__(self, root, deck):
        cards = deck.cards

        if len(cards) > 0:
            self.target_card = cards[int(random.random()*len(cards))]
        else:
            self.target_card = ""

        self.deck_frame = Frame(root, bg = "white")
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
        new_card = Card.Card(face,content)
        deck.add_card(new_card)
        self.new_card_pop_up.destroy()
        cards.append(new_card)