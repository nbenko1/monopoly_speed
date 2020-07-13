# this keeps track of the game state, calls update methods and maintains board
# will this be a class? -heh no

import player
import board

import random
 
# add multithreading
# differintiate between player types  -> superclass?
# how to control timing - player class has 'wait' commands
# board is a global variable
    #info per tile = [id, players on spot, owner], freq player 1, freq player 2]


#initialize board
b = board.Board()
playerOne = player.Player(1)
rounds = 10

def gameSetup():
    #initialize player(s)
    
    playerOne.money += 5000 # starts with 5000
    for cards in range(4):
        playerOne.chance.append("random chance card") # four chance cards
        if cards < 3:
            playerOne.chance.append("random community chest card") # three community chest cards
    playerOne.startingPos = 0 # where to start

   

   
#runs the game
def main():
    print("--------------")
    print("STARTING GAME")
    print("--------------")


    for _ in range(0,rounds):
        #role phase
        role = random.randint(1,6)
        playerOne.move(role)

        #tile action phase
        if playerOne.tile == 24: #on go to jail 
            playerOne.tile = 8 #reset player position to jail
            playerOne.timesJailed += 1

        elif playerOne.tile == 0 or playerOne.tile == 16 or playerOne.tile == 8: # if the player is on GO or Jail do nothing
            t = playerOne.tile
            if t == 0 or t == 16:
                print("player", playerOne.id, "landed on GO")
            else:
                print("player", playerOne.id, "is visiting jail")

        else: #can purchase tile
            purResult = b.purchase(playerOne) #tried to purchase tile from the board object
            if purResult == 2: # successful
                #this section will probably be handled by the player obkect once we add more agents
                tile = b.getTile(playerOne.tile)
                tile[1] = playerOne.id
                playerOne.money -= 1000
                playerOne.properties.append(tile[0]) # saves property id to player
                #
                print("player", playerOne.id, "bought", playerOne.tile)
            elif purResult == 0: # not enough money
                print("player", playerOne.id, "does not have enough money to buy", playerOne.tile)
            else: # already owned
                print("property already owned")





#prints out stats from the game
def stats():
    print("--------------")
    print("STATS")
    print("--------------")

    print("player one starting position:", playerOne.startingPos)
    print("money:", playerOne.money)
    print("number of roles:", rounds)
    print("roles:", playerOne.roles)
    print("path:", playerOne.path)
    print("properties:", playerOne.properties)
    print("--------------")
    #print(b.tiles)



gameSetup()
main()
stats()