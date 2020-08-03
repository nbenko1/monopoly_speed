import sys

class Board:
    def __init__(self):
        self.tiles = { # i may need to rework this to make printing it out easier

        #          0                  1                2          3
        # [ Place on board | Owner? (ID of player) | frequency | placeholder ]
        "brown"     : [[ 1, 0, "Mediterranean Ave", 0], [ 3, 0, "Baltic Ave", 0]],
        "lblue"     : [[ 5, 0, "Oriental Ave", 0], [ 6, 0, "Vermont Ave", 0], [ 7, 0, "Connecticut Ave", 0]],
        "pink"      : [[ 9, 0, "St. Charles Place", 0], [10, 0, "States Ave", 0], [11, 0, "Virginia Ave", 0]],
        "orange"    : [[13, 0, "St. James Place", 0], [14, 0, "Tennessee Ave", 0], [15, 0, "New York Ave", 0]],
        "red"       : [[17, 0, "Kentucky Ave", 0], [18, 0, "Indiana Ave", 0], [19, 0, "Illinois Ave", 0]],
        "yellow"    : [[21, 0, "Atlantic Ave", 0], [22, 0, "Ventnor Ave", 0], [23, 0, "Marvins Gardens", 0]],
        "green"     : [[25, 0, "Pacific Ave", 0], [26, 0, "North Carolina Ave", 0], [27, 0, "Pennsylvania Ave", 0]],
        "dblue"     : [[29, 0, "Park Place", 0], [31, 0, "Boardwalk", 0]],
   
        "railroad"  : [[ 4, 0, "Reading Rail", 0], [12, 0, "Pennsylvania Rail", 0], [20, 0, "B. & O. Rail", 0], [28, 0, "Short Lane", 0]],
        "utilities" : [[ 2, 0, "Water Works", 0], [30, 0, "Electric Company", 0]],
   
        #          0               1              2
        # [ Place on board | placeholder | placeholder ]
        "GO1"          : [[0, "GO 1", 0]],
        "GO2"          : [[16, "GO 2", 0]],
        
   
        "jail"         : [[8, "Jail", 0]],
        "go to jail"   : [[24, "Go To Jail", 0]],
        }

        self.exclude = [0,16,8,24]


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

            
    def print(self):
        sys.stdout.write("------------------" + "\n")
        sys.stdout.write("-------BOARD------" + "\n")
        sys.stdout.write("------------------" + "\n")
        sys.stdout.write('[place on board][owner]["Title"]["N"]' + "\n")

        for i in range(1,32):
            if i not in self.exclude:
                # print("ID: ",self.getTile(i)[0],"Owner:",self.getTile(i)[1])
                print(self.getTile(i))

    # looks through what the player needs and returns the best card from the board
    # def bestPropForPlayer(self, player):
        


# b = Board()
# b.print()