
import random
# import player

# used by both classes
# chooses a random card from a deck depending on frequency
def pullCards(deck, num):
    cards = []
    for _ in range(num):  #loops once for each card drawn
        weights = []
        for key, value in deck.items():
            weights.append(value[1])
        card = random.choices(deck, weights = weights, k = 1)

        cards.append(card[0])
        id = card[0][0]
        for key, value in deck.items(): #adjust weights
            if id == value[0]:
                value[1] -= 1
    return cards

def pullSpecCards(deck, num, IDS):
    cards = []
    for ID in IDS:
        ID -= 1 # cause im dum
        cards.append(deck[ID]) # add card to player list
        deck[ID][1] -= 1 # take card out of deck
    return cards



class ChanceDeck:
    def __init__(self):
        self.Cards = {
            #  [id, frequency, keep/use, description]
            0: [1, 2, "keep", "take any unowned property"],
            1: [2, 2, "keep", "cancel a chance card that is played against you"],
            2: [3, 3, "keep", "swap any one of your properties with any one of anothers players properties"],
            3: [4, 4, "keep", "steal any one property from another player"],
            4: [5 ,5, "use", "choose any property owned by another player and immediately return it to the board"]
        }

    def pullSpecChanceCards(self, IDS):
        return pullSpecCards(self.Cards, 4, IDS)


    def pullChanceCards(self):
        # print("distributing chance cards")
        return pullCards(self.Cards, 4)

    # def playChanceCard(self, player, players, b, block, report):
    #     time.sleep(random.randint(0.0,0.4)) # slightly randomizes which player gets to go first in each round
    #     #loop through cards

    #     #while the player makes decision the player and board need to be locked
    #     block.acquire()
    #     player.playChance(players,player,b,report)
    #     block.release()




# player = player.Player(1)
# deck = ChanceDeck()
# player.chance = deck.pullChanceCards()
# for card in player.chance:
#     print(card[0], card[1])

#these are used for the card set testing
brown = [1,3]
lblue = [5,6,7]
pink = [9,10,11]
orange = [13,14,15]
red = [17,18,19]
yellow = [21,22,23]
green = [25,26,27]
dblue = [29,31]

railroads = [4,12,20,28]
utilities = [2,30]

class CommChestDeck:

    def __init__(self):

        self.Cards = {
            # [id, freq, type, reward, number of reqs, reqs]
            0: [1, 1, "partGroup", 2000, 3, brown, lblue, dblue], # need to look at card
            1: [2, 1, "group", 2000, 2, yellow, dblue],
            2: [3, 1, "partGroup", 2000, 3, pink, orange, green],
            3: [4, 1, "set", 4000, 1, red],
            4: [5, 1, "set", 4000, 1, green],
            5: [6, 1, "set", 4000, 1, yellow],
            6: [7, 1, "set", 3000, 1, pink],
            7: [8, 1, "set", 3000, 1, orange],
            8: [9, 1, "set", 2000, 1, utilities],
            9: [10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities],   
            10: [11, 1, "rail", 1000, 4, railroads]
        }

    def pullChestCards(self):
        # print("distributing chest cards")
        return pullCards(self.Cards, 3)

    def pullSpecChestCards(self, IDS):
        return pullSpecCards(self.Cards, 3, IDS)

    #calculate payout based on cards 

    def payout(self, player, report):
        for card in player.commChest:
            if report: print("---CARD---:",card)
            if card[2] == "partGroup": # at least one card in group
                meetsReq = False
                for i in range(5, len(card)):
                    for prop in card[i]:
                        if prop in player.properties: meetsReq = True
            
                if meetsReq: 
                    player.money += 2000
                    player.mChest += 2000
                    player.commChestPayout.append([card[0], card[3]])
                    if report: print("\n             + 2000 for partGroup\n")

            if card[2] == "group": # one in each
                #print("CARD", card[2])
                found = False
                fullSet = True
                for i in range(5,len(card)):
                    tempSet = False
                    for prop in card[i]:
                        for x in player.properties:
                            if x == prop:
                                found = True
                                break
                        if found: tempSet = True
                        found = False
                    if not tempSet: fullSet = False
                if fullSet: 
                    player.money += card[3]
                    player.mChest += card[3]
                    player.commChestPayout.append([card[0], card[3]])
                    if report: print("\n             +", card[3], "for group\n")

            if card[2] == "set": #full set
                #print("CARD", card[2])
                fullSet = True
                for i in range(5,len(card)):
                    propSet = card[i]
                    for prop in propSet:
                        if prop not in player.properties: fullSet = False
                    if fullSet: 
                        player.money += card[3] 
                        player.mChest += card[3]
                        player.commChestPayout.append([card[0], card[3]])
                        if report: print("\n             +", card[3], "for set\n")
                    
            if card[2] == "anySet":
                #print("CARD", card[2])
                for i in range(5, len(card)):
                    fullSet = True
                    for prop in card[i]:
                        if prop not in player.properties: fullSet = False
                    if fullSet: 
                        player.money += card[3] 
                        player.mChest += card[3]
                        player.commChestPayout.append([card[0], card[3]])
                        if report: print("             +", card[3], "for anySet\n")

            if card[2] == "rail":
                # print("CARD", card[2])
                propSet = card[5]
                for prop in propSet:
                    if prop in player.properties: 
                        player.money += 1000
                        player.mChest += 1000
                        player.commChestPayout.append([card[0], card[3]])
                        if report: print("             + 1000 for rail\n")
                    


#testing
# chestDeck = CommChestDeck()
# player = player.Player(1)
# player.commChest = chestDeck.pullChestCards()
# player.commChest.append(chestDeck.Cards[0])
# player.properties.append(1)
# player.properties.append(28)
# player.properties.append(4)
# player.properties.append(12)
# player.properties.append(29)
# player.properties.append(3)
# chestDeck.payout(player)
# print(player.money)
# print(player.commChest)
