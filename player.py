#this is a basic player class, holds money, cards, 
#will be superclass for more complex players


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.money = 5000
        self.tile = 0 # starting position - can be changed
        self.properties = [] #what properties are owned
        self.chance = [] # chance cards, starts with 3
        self.comChest = [] #community chest cards, starts with 4
        self.bankrupt = False

    def passGO(self, oldPos, newPos):
        if oldPos < 20 and newPos >= 20 or oldPos < 40 and newPos >= 40:
            self.money += 1000

    def move(self, role):
        num = role
        old_tile = self.tile
        self.tile += num

        self.passGO(old_tile, self.tile) # if passes either go adds $1000

        if self.tile >= 40:
            self.tile = self.tile % 40 # wraps position around board

    
    
    #def visitProperty(self, property): 

    #def buyProperty(self, property):
