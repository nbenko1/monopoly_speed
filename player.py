#this is a basic player class, holds money, cards, 
#will be superclass for more complex players

import time
import random
import sys
from operator import itemgetter

import cards


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
        self.winner = False

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
        if oldPos < 0 and newPos >= oldPos or oldPos < 16 and newPos >= 16:
            self.timesPassedGo += 1
            self.money += 1000
            self.mGo += 1000
            if report: sys.stdout.write("player " + str(self.id) + " passed GO and received 1000 dollars" + "\n")

    #moves player, adds money if passed go
    def move(self, report, quickTiming):
        role = random.randint(1,6) 

        self.wait(1.8, 2.3, quickTiming)
        # time.sleep(random.uniform(1.8,2.3)/quickTiming) #--------------------------------------- time to move
        # time.sleep(random.randint(1,2)/quickTiming) #--------------------------------------- time to move


        self.roles.append(role) # adds role to records
        
        self.passGO(self.tile, self.tile+role, report) # if passes either go adds $1000
        self.tile += role

        if self.tile >= 32:
            self.tile = self.tile % 32 # wraps position around board

        self.path.append(self.tile) # keeps track of where the player went
        self.numRoles += 1
        self.spaceCovered += role
    

    #when the player lands on a property this method handles whether or not to buy it
    def canPurchase(self, b, report, block, quickTiming):
       
        time.sleep(random.randint(2,3)/quickTiming)   #--------------------------------------- time to purchase


        # time.sleep(random.uniform(2.0,2.5)/quickTiming)   #--------------------------------------- time to purchase
        

        block.acquire() #mutex lock around board
        tile = b.getTile(self.tile)
        tile[1] = self.id
        block.release() #release mutex

        self.money -= 1000
        self.properties.append(tile[0]) # saves property id to player
        if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n") #TODO move to player

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
    def wait(self, low, high, divider):

        number = random.uniform(low,high)
        wait = number/divider
        wait = round(wait, 1)
        # print(self.id, "is waiting", wait)


        time.sleep(round(high/divider,1))

        # time.sleep(wait)


    def playChance(self, players, player, b, report):
        card = random.choice(self.chance)
        while card[0] == 2: # cant draw the cancel card 
            card = random.choice(self.chance)
        
        print(card)

        if card[0] == 1: #take any unowned property
            pass
        if card[0] == 2: #cancel a chance card played against you
            pass
        if card[0] == 3: #swap with another player
            pass
        if card[0] == 4: #steal from another player
            pass
        if card[0] == 5: #return any property owned by another player to the board
            pass

        self.chance.remove(card)
        
    """
    needs some thought - more balance - god this is kicking my ass
    """
    #assigns a score to each property owned by the player
    #then chooses the property with the lowest score and returns it
    #need to TEST THE HELL out of this method
    #returns -1 if no properties
    #TODO fix group card scoring - mostly done, might be worth a another look
    def findLeastNeededCard(self):
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
        
        print("after card", scoreProp)

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

        print("after sets", scoreProp, "\n")

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

        print(propScore)
        sortedScore = sorted(propScore, key = lambda x: x[1], reverse=True)#sorts by score
        print(sortedScore)

        sortedNoScore = []
        for prop, score in sortedScore:
            sortedNoScore.append(prop) #list of only properties

        print(sortedNoScore)

        #return sorted list of all possible propreties from best to worst
        return sortedNoScore


        

# in file testing


# p = Player(1)
# p.commChest.append([8, 1, "set", 3000, 1, orange])
# p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
# p.properties.extend([1,3,5,7,13,14])
# p.findWantedProperty()



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
# print(p.findLeastNeededCard())

# p.properties.append(9)
# p.properties.append(10)
# p.properties.append(11)


# p.calculateMoney()
# print(p.money)