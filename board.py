
class Board:
    def __init__(self):
        self.tiles = { # i may need to rework this to make printing it out easier

        #          0                  1                2          3
        # [ Place on board | Owner? (ID of player) | placeholder | placeholder ]
        "brown"     : [[ 1, 0, 0, 0], [ 3, 0, 0, 0]],
        "lblue"     : [[ 5, 0, 0, 0], [ 6, 0, 0, 0], [ 7, 0, 0, 0]],
        "pink"      : [[ 9, 0, 0, 0],  [10, 0, 0, 0], [11, 0, 0, 0]],
        "orange"    : [[13, 0, 0, 0], [14, 0, 0, 0], [15, 0, 0, 0]],
        "red"       : [[17, 0, 0, 0], [18, 0, 0, 0], [19, 0, 0, 0]],
        "yellow"    : [[21, 0, 0, 0], [22, 0, 0, 0], [23, 0, 0, 0]],
        "green"     : [[25, 0, 0, 0], [26, 0, 0, 0], [27, 0, 0, 0]],
        "dblue"     : [[29, 0, 0, 0], [31, 0, 0, 0]],
   
        "railroad"  : [[ 4, 0, 0, 0], [12, 0, 0, 0], [20, 0, 0, 0], [28, 0, 0, 0]],
        "utilities" : [[2, 0, 0, 0], [30, 0, 0, 0]],
   
        #          0               1              2
        # [ Place on board | placeholder | placeholder ]
        "GO1"          : [[0, 0, 0]],
        "GO2"          : [[16, 0, 0]],
        
   
        "jail"         : [[8, 0, 0]],
        "go to jail"   : [[24, 0, 0]],
        }

        #self.exclude = [0, 8, 16, 24] # not sure about this one

    # isolates the tile that was landed on

    #this method returns the tile from its ID
    def getTile(self, id):
        for key, value in self.tiles.items(): #loops through dictionary
            for place in value: # loops through the values
                if id == place[0]: #if the ID of the property matches the one passed
                   return place #returns property array

        return -1 # if not found return

    #returns the option for the player 
    def purchase(self, player):
        tile = self.getTile(player.tile) #get tile
        if player.money < 1000: return 0 # return 0 if the player does not have enough money
        elif tile[1] == 0: return 2 #return 2 if purchased successful
        else: return 1 #returns 1 already owned
            

