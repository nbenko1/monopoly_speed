
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



class CommChestDeck:

    def __init__(self):

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

        self.CommChestCards = {
            #[id, freq, type, reward, number of reqs, reqs]
            0: [1, 10, "group", 2000, 3, brown, lblue, pink]
        }

    def pullChestCards(self):
        return pullCards(self.CommChestCards, 1)


    #calculate payout based on cards 
    #this ones tough, have to check property cards against requirements for each community chest card

    #THIS IS A MESS but i think it works

    def payout(self, player):
        for card in player.commChest:
            print(card)
            if card[2] == "group":
                found = False
                fullSet = True
                for i in range(5,5+card[4]):
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
                pass
            if card[2] == "utility":
                pass
            if card[2] == "railroad":
                pass

chestDeck = CommChestDeck()
player = player.Player(1)
player.commChest = chestDeck.pullChestCards()
player.properties.append(4)
player.properties.append(5)
player.properties.append(10)
player.properties.append(1)
chestDeck.payout(player)


