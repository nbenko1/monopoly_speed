#this is a basic player class, holds money, cards, 
#will be superclass for more complex players


class Player:
    def __init__(self, player_id):

        #
        self.id = player_id
        self.tile = 0 #current location

        #game progress
        self.properties = [] #what properties are owned
        self.chance = [] # chance cards, starts with 3
        self.comChest = [] #community chest cards, starts with 4
        self.bankrupt = False

        #stats for reporting
        self.timesJailed = 0
        self.timesPassedGo = 0
        self.roles = []
        self.startingPos = 0 # starting position - can be changed
        self.path = []

        #money breakdown
        self.mGo = 0 #money from passing GO
        self.mProp = 0 #money from owning properties
        self.mChance = 0 #money from Chance cards
        self.money = 0 # total combination of all money source   <--------------rethink
    
        #money = 20

    def passGO(self, oldPos, newPos):
        if oldPos < 0 and newPos >= oldPos or oldPos < 16 and newPos >= 16:
            self.timesPassedGo += 1
            self.money += 1000
            print(self.id, "passed GO and received 1000 dollars")

    #moves player, adds money if passed go
    def move(self, role):
        self.roles.append(role) # adds role to record
        num = role
        old_tile = self.tile
        self.tile += num

        self.passGO(old_tile, self.tile) # if passes either go adds $1000

        if self.tile >= 32:
            self.tile = self.tile % 32 # wraps position around board

        self.path.append(self.tile) # keeps track of where the player went
    


    
    
    #def visitProperty(self, property): 

    #def buyProperty(self, property):
