#LIBRARIES
import time
import random

#VARIABLES
VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
SUITS = ["Hearts", "Clubs", "Spades", "Diamonds"]
deck = []
hand = []

#FUNCTIONS
def deal(num_of_cards):
    for i in range(0, num_of_cards):
        hand.append([deck[-1][0], deck[-1][1]])
        deck.pop()
    for i in range(len(hand)):
        print(f"Card {i+1} is: {hand[i][0]} of {hand[i][1]}")

#START
for s in SUITS:
    for v in VALUES:
        deck.append([v, s])
        time.sleep(0.1)
        print(f"Card: {v} of {s} added")
    print("Done!")

random.shuffle(deck)


deal(5)