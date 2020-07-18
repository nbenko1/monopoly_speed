
import random
import player

#used by both classes
# chooses a random card depending on frequency
def pullCards(deck, num):
    weights = []
    for key, value in deck.items():
        weights.append(value[0])
    cards = random.choices(deck, weights = weights, k = num)
    for card in cards:
        id = card[0]
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
        pullCards(self.chanceCards, 4)


deck = ChanceDeck()
deck.pullChanceCards()





class CommChestDeck:
    def __init__(self):
        self.CommChestCards = {
            #[type, reward, number of reqs, reqs]
            0: [1, "group", 2000, 3, [1,3],[5,6,7],[29,31]]
        }

    def pullChestCards(self):
        pullCards(self.CommChestCards, 3)


    #caculate payout based on cards 
    #this ones tough, have to check property cards against requirements for each community chest cards
    def payout(player):
        for card in player.commChest:
            if card[0] == "group":
                print("worked")


# chestDeck = CommChestDeck()
# player = player.Player(1)
# player.commChest.append(chestDeck.pullChestCards())
# payout(player)


