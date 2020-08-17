#this is a basic player class, holds money, cards, 
#will be superclass for more complex players

import time
import random
import sys
from operator import itemgetter

import cards
import board


chance = cards.ChanceDeck()
chest = cards.CommChestDeck()



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

pSet = [brown,lblue,pink,orange,red,yellow,green,dblue,railroads,utilities]

class Player:
    def __init__(self, player_id):

        
        self.type = "greedy"
        self.id = player_id
        self.tile = 0 #current location
        self.winner = "Loser"
        self.totalWaitTime = 0.0

        #game progress
        self.properties = [] #what properties are owned
        self.chance = [] # chance cards, starts with 3
        self.commChest = [] #community chest cards, starts with 4
        self.bankrupt = False

        #stats for reporting
        self.timesJailed = 0
        self.timesPassedGo = 0
        self.roles = []
        self.startingPos = 0 # starting position - can be changed
        self.path = []
        self.numRoles = 0
        self.spaceCovered = 0

        #money breakdown
        self.mGo = 0 #money from passing GO
        self.mProp = 0 #money from owning properties
        self.mChest = 0 #money from chest cards
        self.money = 0 # total combination of all money source  
        self.commChestPayout = [] #tracks how much money each card earns
    
    def passGO(self, oldPos, newPos, report):
        if newPos >= 32 or oldPos < 16 and newPos >= 16:
            self.timesPassedGo += 1
            self.money += 1000
            self.mGo += 1000
            if report: sys.stdout.write("player " + str(self.id) + " passed GO and received 1000 dollars" + "\n")

    #moves player, adds money if passed go
    def move(self, report, quickTiming, randomTime):
        role = random.randint(1,6) 

        if report: 
            if self.type != "conservative":sys.stdout.write("player " + str(self.id) + " is moving to " + str((self.tile+role)%32) + "\n")
            else: sys.stdout.write("player " + str(self.id) + " is moving to " + str((self.tile+role)%32) + " and is speeding along" "\n")

        self.wait(1.8, 2.3, quickTiming,randomTime)#---------------------------------------

        self.roles.append(role) # adds role to records
        
        self.passGO(self.tile, self.tile+role, report) # if passes either go adds $1000
        self.tile += role

        if self.tile >= 32:
            self.tile = self.tile % 32 # wraps position around board

        self.path.append(self.tile) # keeps track of where the player went
        self.numRoles += 1
        self.spaceCovered += role
    

    #when the player lands on a property this method handles whether or not to buy it
    def canPurchase(self, b, report, block, quickTiming, randomTime):
       
        
      
        tile = b.getTile(self.tile)
        tile[1] = self.id
        

        self.money -= 1000
        self.properties.append(tile[0]) # saves property id to player



        if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n") #TODO move to player
        
        block.release()
        # sys.stdout.write("--player " + str(self.id) + " released block " + "\n")


        self.wait(2,3,quickTiming,randomTime)
        

    # at the end of the game this method will look at the cards and calculate how much money was made
    def calculateMoney(self):

        for prop in pSet: # for each possible set
            fullSet = True
            for tile in prop: # for each property owned
                if tile in self.properties: # each property gets 1000
                    self.money += 1000
                    self.mProp += 1000
                else: fullSet = False 

            if fullSet: 
                if len(prop) == 2: #full set of 2
                    self.money += 2000
                    self.mProp += 2000
                if len(prop) == 3: #full set of 3
                    self.money += 3000
                    self.mProp += 3000
                elif len(prop) == 4: #full set of 4(rail)
                    self.money += 4000
                    self.mProp += 4000

    #utility method to suspend the player
    def wait(self, low, high, quickTiming, randomTime):
        # print("low", low, "high", high)
        # print("random?", randomTime)
        wait = 0
        if randomTime:
            randNumber = random.uniform(low,high) # randomized the number a bit
            number = round(randNumber, 2) # rounds it to avoid overflow
            wait = round(number/quickTiming, 2) # same
            time.sleep(wait) # random wait
        else:
            wait = round(high/quickTiming, 2)
            time.sleep(wait) # static wait


        self.totalWaitTime = self.totalWaitTime + wait


    def playChance(self, players, b, report):
        time.sleep(1)
        print("1")
        numCancel = 0
        for card in self.chance:
            if card[0] == 2:
                numCancel += 1

        if len(self.chance) == 0 or len(self.chance) == numCancel:
            print("no playable cards")
            return
        print("2")       

        card = random.choice(self.chance)

        while card[0] == 2: # this could be getting stuck
            print("yeah we stuck looping")
            card = random.choice(self.chance)
        print("3")
        self.chance.remove(card)
 
        if report: print("\n", "  ---- beginning trading round for player", self.id,"----")
        if report: print("playing card:", card)
        print("4")
        found = False
        if card[0] == 1: #take any unowned property
            # loop through wanted properties
            if report: print("starting card 1 process - take an unowned property")
            wantedCards = self.findWantedProperty()
            for prop in wantedCards: # looped through wanted properties in descending order

                tile = b.getTile(prop) # loops through each property on the board

                if prop == tile[0] and tile[1] == 0: # if the properties match and it is available
                    if report: print("Player", self.id, "chose", prop, "from the board")
                    self.properties.append(prop) #add property to player
                    tile[1] = self.id # remove from board
                    found = True
                    break
            if not found and report: print("player", self.id, "used card", card[0], "but there were no unowned properties")
    

        if card[0] == 2: #cancel a chance card played against you
            print("shouldn't be here")
            pass # cannot be drawn

        if card[0] == 3: #swap with another player
            if report: print("starting card 3 process - swap with another player")
            mostWanted = self.findWantedProperty()
            leastWanted = self.findLeastNeededProp()

            if leastWanted == -1: 
                if report: print("player", self.id, "has no properties to trade")
                return

            #TODO move this to method???
            for prop in self.properties: # removes all properties that are already owned
                if prop in mostWanted:
                    mostWanted.remove(prop)

            if report: print("least wanted card is", leastWanted)
            if report: print("most wanted is", mostWanted)

            for prop in mostWanted:
                for player in players:
                    if prop in player.properties and player.id != self.id:
                        if report: print("player", self.id, "is swapping", leastWanted, "for", prop, "from player", player.id)
                        #checks if the player has a cancel card
                        for card in player.chance:
                            if card[0] == 2: # if the player has a cancel card
                                player.chance.remove(card)
                                if report: print("the card was cancelled!")
                                return

                        #give self wanted property
                        player.properties.remove(prop) # remove from player
                        self.properties.append(prop) # give to self
                        b.getTile(prop)[1] = self.id # change owner on the board
        
                        #give player least wanted
                        self.properties.remove(leastWanted) # remove from player
                        player.properties.append(leastWanted) # give to self
                        b.getTile(leastWanted)[1] = player.id # change owner on the board
                        return
            
            if report: print("player", self.id, "looked for a card but couldn't find one")

        if card[0] == 4: #steal from another player
            if report: print("starting card 4 process - steal from another player")
            mostWanted = self.findWantedProperty()

            for prop in mostWanted:
                for player in players:
                    if prop in player.properties and player.id != self.id:
                        if report: print("player", self.id, "is stealing property", prop, "from player", player.id)

                        for card in player.chance:
                            if card[0] == 2: # if the player has a cancel card
                                player.chance.remove(card)
                                if report: print("the card was canceled")
                                return
                        if report: print(prop, "was stolen")
                        #give self wanted property
                        player.properties.remove(prop) # remove from player
                        self.properties.append(prop) # give to self
                        b.getTile(prop)[1] = self.id # change owner on the board
                        return

            if report: print("player", self.id, "couln't find a card to steal")
    
        if card[0] == 5: #return any property owned by another player to the board
            if report: print("starting card 5 process - return prop from another player")
            #find player with most money
            propCount = -1
            p0 = Player(-1)
            chosenPlayer = p0
            if len(players) >= 2: # makes sure theres more than one player
                for player in players: # finds the player with the most properties
                    if len(player.properties) > propCount:
                        propCount = len(player.properties)
                        chosenPlayer = player
            else: 
                if report: print("Not enough players to choose from")
                return

            if chosenPlayer == p0:
                if report: print("no players had any properties")
            else:
                #do nothing if the player has a cancel card
                cancel = False
                if report: print("player", chosenPlayer.id, "was chosen")
                for card in chosenPlayer.chance:
                    if card[0] == 2: # if the player has a cancel card
                        chosenPlayer.chance.remove(card)
                        if report: print("the card was canceled")
                        cancel = True
                
                #otherwise return their most valuable card to the board
                if not cancel: # the card was not canceled
                    wantedProperties = chosenPlayer.findWantedProperty()

                    for prop in wantedProperties: # for each property
                        if prop in chosenPlayer.properties: # if the player owns the property
                 
                            chosenPlayer.properties.remove(prop) # remove the property from the player 
                            boardPlace = b.getTile(prop) # loop through each board tile
                            boardPlace[1] = 0 # set status to unowned
                            if report: print("returning", prop, "to the board")
                            break






    """
    needs some thought - more balance - god this is kicking my ass
    """
    #assigns a score to each property owned by the player
    #then chooses the property with the lowest score and returns it
    #need to TEST THE HELL out of this method
    #returns -1 if no properties
    #TODO fix group card scoring - mostly done, might be worth a another look
    def findLeastNeededProp(self):
        scoreProp = [] # this will keep track of each property and the score
        for i in range(len(self.properties)):
            #[propID, score]
            scoreProp.append([self.properties[i], 0]) # populated list
        for j in range(len(self.properties)): #O(n^3) ~nice~ should check if prop matches chest card
            for card in self.commChest:
                for i in range(5,len(card)):
                    if self.properties[j] in card[i]: # if the property matches a req on a chest card
                        scoreProp[j][1] = scoreProp[j][1] + 1 # gives that property points
                        if card == [2, 1, "group", 2000, 2, yellow, dblue]:
                            scoreProp[j][1] = scoreProp[j][1] + 2 #group card gets extra boost
        
        # print("after card", scoreProp)

        # print(scoreProp)
        countSets = []
        for i in range(len(pSet)):
            countSets.append([pSet[i],0]) # this will count how many properties per set [player props, total props]        
        for prop in self.properties:
            for countSet in countSets:
                if prop in countSet[0]:
                    countSet[1] = countSet[1] + 1

        # print(countSets, '\n')

        for i in range(len(scoreProp)): # for each score tuple
            for countSet in countSets: # for each set with count
                if scoreProp[i][0] in countSet[0]:
                    if countSet[1] == len(countSet[0]): # if a full set
                        scoreProp[i][1] = scoreProp[i][1] + 5
                    elif countSet[1] == len(countSet[0]) - 1: # if only missing one card
                        scoreProp[i][1] = scoreProp[i][1] + 2 
                    else: # only card in the set
                        pass # no points

                    # scoreProp[i][1] = scoreProp[i][1] - (len(countSet[0]) - countSet[1]) #subtracts a point for each property missing from the set
        worstPropScore = float("inf") # really high number
        worstProp = -1
        for prop in scoreProp:
            if prop[1] < worstPropScore:
                worstPropScore = prop[1]
                worstProp = prop[0]

        # print("after sets", scoreProp, "\n")

        return worstProp


    # ranks each possible property and returns the list as a list of tuples with [prop id, score]
    def findWantedProperty(self):
        propScore = []
        for props in pSet:
            for prop in props:
                propScore.append([prop, 0]) # a list with [prop, score]

        #addes points if property matches reqs on chest cards
        for propSet in propScore:
            for card in self.commChest:
                for i in range(5,len(card)):
                    if propSet[0] in card[i]: # if the property matches a req on a chest card
                        propSet[1] = propSet[1]  + 1 # gives that property points
                        if card == [2, 1, "group", 2000, 2, yellow, dblue]:
                            propSet[1] = propSet[1] + 2 #group card gets extra boost

        # print(propScore)

        # add points for sets
        countSets = []
        for i in range(len(pSet)):
            countSets.append([pSet[i],0]) # this will count how many properties per set [player props, total props]        
        for prop in self.properties:
            for countSet in countSets:
                if prop in countSet[0]:
                    countSet[1] = countSet[1] + 1

        # print(countSets)

        for ownedPropScore in countSets:
            for propSet in propScore:
                if propSet[0] in ownedPropScore[0]:
                    propSet[1] = propSet[1] + ownedPropScore[1]

        # print(propScore)
        sortedScore = sorted(propScore, key = lambda x: x[1], reverse=True)#sorts by score
        # print(sortedScore)

        sortedNoScore = []
        for prop, score in sortedScore:
            sortedNoScore.append(prop) #list of only properties

        # print(sortedNoScore)

        #return sorted list of all possible propreties from best to worst
        return sortedNoScore


        


# in-file testing

# p1 = Player(1)
# p1.commChest.append([8, 1, "set", 3000, 1, orange])
# p1.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
# p1.properties.extend([1,3,5,7,13,14,15])
# # p1.properties.extend([1,2,3,4,5,6,7,9,10,11,12,13,14,18,19,20,21,22,23,25,26,27,28,29,30,31])
# # p1.chance.append([1, 2, "keep", "take any unowned property"])
# p1.chance.append([5 ,5, "use", "choose any property owned by another player and immediately return it to the board"])


# p2 = Player(2)
# p2.commChest.append([4, 1, "set", 4000, 1, red])
# p2.properties.extend([6,17,21])
# # p2.chance.append([1, 2, "keep", "take any unowned property"])
# p2.chance.append([5 ,5, "use", "choose any property owned by another player and immediately return it to the board"])
# players = [p1,p2]

# p2.money = 1

# b = board.Board()

# for key, value in b.tiles.items(): #loops through dictionary
#     for place in value:
#         if place[0] in p1.properties:
#             place[1] = 1
#         if place[0] in p2.properties:
#             place[1] = 2

# b.print()

# p1.playChance(players, b, False)

# b.print()

# p = Player(1)
# p.chance = chance.pullChanceCards()
# p.commChest = chest.pullChestCards()
# p.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
# p.commChest.append([8, 1, "set", 3000, 1, orange])
# p.commChest.append([10, 2, "anySet", 1000, 10, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
# p.commChest.append([11, 1, "rail", 1000, 4, railroads])
# print(p.commChest)
# p.properties.append(1)
# p.properties.append(3)
# p.properties.append(9)
# p.properties.append(15)
# p.properties.append(14)
# print(p.findLeastNeededProp())

# p.properties.append(9)
# p.properties.append(10)
# p.properties.append(11)


# p.calculateMoney()
# print(p.money)