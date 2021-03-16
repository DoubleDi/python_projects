import random

values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q", "A"]
suites = ["Clubs", "Diamonds", "Hearts", "Spades"]
cards = []

for s in suites:
    for v in values:
        cards.append(v + " of " + s)
print('============')
print(len(cards))
print(cards)

shuffled_cards = []
while cards:
    i = random.randint(0, len(cards) - 1)
    c = cards.pop(i)
    shuffled_cards.append(c)
print('============')
print(len(shuffled_cards))
print(shuffled_cards)
