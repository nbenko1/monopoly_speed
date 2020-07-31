#this is a basic player class, holds money, cards, 
#will be superclass for more complex players

import time
import random
import sys

import cards


chance = cards.ChanceDeck()


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
        self.money = 0 # total combination of all money source   <--------------rethink
    
        #money = 20

    def passGO(self, oldPos, newPos, report):
        if oldPos < 0 and newPos >= oldPos or oldPos < 16 and newPos >= 16:
            self.timesPassedGo += 1
            self.money += 1000
            self.mGo += 1000
            if report: sys.stdout.write("player " + str(self.id) + " passed GO and received 1000 dollars" + "\n")

    #moves player, adds money if passed go
    def move(self, report):
        role = random.randint(1,6) 
        time.sleep(random.randint(2,3))#--------------------------time to moce

        self.roles.append(role) # adds role to records
        
        self.passGO(self.tile, self.tile+role, report) # if passes either go adds $1000
        self.tile += role

        if self.tile >= 32:
            self.tile = self.tile % 32 # wraps position around board

        self.path.append(self.tile) # keeps track of where the player went
        self.numRoles += 1
        self.spaceCovered += role
    

    #when the player lands on a property this method handles whether or not to buy it
    def canPurchase(self, b, report, block):
        time.sleep(random.randint(3, 4)) #------------------------------------- time to purchase
        
        block.acquire()
        tile = b.getTile(self.tile)
        tile[1] = self.id
        block.release()

        self.money -= 1000
        self.properties.append(tile[0]) # saves property id to player
        if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n") #TODO move to player

    # at the end of the game this method will look at the cards and calculate how much money was made
    def calculateMoney(self):

        for prop in pSet:
            fullSet = True
            for tile in prop:
                if tile in self.properties:
                    self.money += 1000
                    self.mProp += 1000
                else: fullSet = False 

            if fullSet: 
                if len(prop) == 2:
                    self.money += 2000
                    self.mProp += 2000
                if len(prop) == 3:
                    self.money += 3000
                    self.mProp += 3000
                elif len(prop) == 4:
                    self.money += 4000
                    self.mProp += 4000
            
    def wait(self, time):
        time.sleep(time)



    def playChance(self, players, player, b, report):
        card = random.choice(self.chance)
        
        print(card)

        if card[0] == 1: #take an unknowned property
            pass

        
        if card[0] == 2: #cancel a chance card played against you
            pass
        if card[0] == 3: #swap with another player
            pass
        if card[0] == 4: #steal from another player
            pass
        if card[0] == 5: #return any property to the board
            pass

        self.chance.remove(card)
        
    def findUnneededCard(self):
        lonelyProperties = self.properties
        for prop in self.properties: #O(n^3) nice should check is prop matches card
            for card in self.commChest:
                for i in range(5,5+card[4]):
                    if prop in card[i]:
                        lonelyProperties.remove(prop)
        for prop in lonelyProperties:
            





p = Player(1)
p.chance = chance.pullChanceCards()
p.playChance()

# p.properties.append(9)
# p.properties.append(10)
# p.properties.append(11)


# p.calculateMoney()
# print(p.money)