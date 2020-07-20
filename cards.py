
import random
import player

# used by both classes
# chooses a random card depending on frequency
def pullCards(deck, num):
    cards = []
    for _ in range(num):  
        weights = []
        for key, value in deck.items():
            weights.append(value[1])
        card = random.choices(deck, weights = weights, k = 1) #this doesn't take into account when cards run out

        cards.append(card[0])
        id = card[0][0]
        for key, value in deck.items():
            if id == value[0]:
                value[1] -= 1
    return cards

class ChanceDeck:
    def __init__(self):
        self.chanceCards = {
            #  [id, frequency, keep/use, description]
            0: [1, 2, "keep", "take any unowned property"],
            1: [2, 2, "keep", "cancel a chance card that is played against you"],
            2: [3, 3, "keep", "swap any one of your properties with any one of anothers players properties"],
            3: [4, 4, "keep", "steal any one property from another player"],
            4: [5 ,5, "use", "choose any property owned by another player and immediately return it to the board"]
        }

    def pullChanceCards(self):
        return pullCards(self.chanceCards, 4)

# player = player.Player(1)
# deck = ChanceDeck()
# player.chance = deck.pullChanceCards()
# for card in player.chance:
#     print(card[0], card[1])

#theses are used for the card set testing
brown = [1,3]
lblue = [5,6,7]
pink = [9,10,11]
orange = [13,14,15]
red = [17, 18,19]
yellow = [21,22,23]
green = [25,26,27]
dblue = [29,31]

railroads = [4,12,20,28]
utilities = [2,30]


class CommChestDeck:

    def __init__(self):

        self.CommChestCards = {
            #[id, freq, type, reward, number of reqs, reqs]
            0: [1, 1, "group", 2000, 3, brown, lblue, dblue],
            1: [2, 1, "group", 2000, 2, yellow, dblue],
            2: [3, 1, "group", 2000, 3, pink, orange, green],
            3: [4, 1, "set", 4000, 1, red],
            4: [5, 1, "set", 4000, 1, green],
            5: [6, 1, "set", 4000, 1, yellow],
            6: [7, 1, "set", 3000, 1, pink],
            7: [8, 1, "set", 3000, 1, orange],
            8: [9, 1, "set", 2000, 1, utilities],
            9: [10, 2, "anySet", 1000, 10, brown, lblue, pink, orange, red, yellow, green, dblue, railroads, utilities],   
            10: [11, 1, "rail", 1000, 4, railroads]
        }

    def pullChestCards(self):
        return pullCards(self.CommChestCards, 4)


    #calculate payout based on cards 
    #this ones tough, have to check property cards against requirements for each community chest card

    #THIS IS A HOT MESS but i think it works

    def payout(self, player):
        for card in player.commChest:
            print(card)
            if card[2] == "group":
                print("CARD", card[2])
                found = False
                fullSet = True
                for i in range(5,len(card)):
                    print("i = " , i)
                    tempSet = False
                    for prop in card[i]:
                        print("out",prop)
                        for x in player.properties:
                            print("owned",x)
                            if x == prop:
                                found = True
                                print("found")
                                break
                        if found: tempSet = True
                        print("met",tempSet)
                        print("was it found?", found)
                        found = False
                    if not tempSet: fullSet = False
                if fullSet: player.money += card[3]
                print("money:",player.money)

            if card[2] == "set":
                print("CARD", card[2])
                propSet = card[5]
                fullSet = True
                for prop in propSet:
                    if prop not in player.properties: fullSet = False
                if fullSet: player.money += card[3] 
                print("money", player.money)
                    
            if card[2] == "anySet":
                print("CARD", card[2])
                for i in range(5, len(card)):
                    fullSet = True
                    for prop in card[i]:
                        if prop not in player.properties: fullSet = False
                    if fullSet: player.money += card[3] 

            if card[2] == "rail":
                print("CARD", card[2])
                propSet = card[5]
                for prop in propSet:
                    if prop in player.properties: player.money += 1000
                print("money", player.money)

chestDeck = CommChestDeck()
player = player.Player(1)
player.commChest = chestDeck.pullChestCards()
player.properties.append(1)
player.properties.append(28)
player.properties.append(4)
player.properties.append(12)
player.properties.append(20)
player.properties.append(3)
chestDeck.payout(player)


