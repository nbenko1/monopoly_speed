# this keeps track of the game state, calls update methods and maintains board
# will this be a class? -heh no

import player
import board

import random
import time

# add multithreading
# differintiate between player types  -> superclass?
# how to control timing - player class has 'wait' commands
# board is a global variable
    #info per tile = [id, players on spot, owner], freq player 1, freq player 2]

print(time.time())



#initialize board
b = board.Board()
rounds = 10
players = []


player = player.Player(1)
players.append(player)

def gameSetup():
    #initialize player(s)
    for player in players:
        player.money += 5000 # starts with 5000
        for cards in range(4):
            player.chance.append("random chance card") # four chance cards
            if cards < 3:
                player.chance.append("random community chest card") # three community chest cards
        player.startingPos = 16 # where to start

 
curTime = time.time() #start time
endTime = curTime + 30.0 # end time
   
#runs the game
def main():
    print("--------------")
    print("STARTING GAME")
    print("--------------")

    global curTime
    player.tile = player.startingPos


    loop = 1
    # for _ in range(0,rounds):
    while curTime <= endTime:    #this is a little flawed as it lets each turn finish before ending the game, but its only a few extra seconds
        print("starting round:", loop)
        #role phase
        role = random.randint(1,6)
        player.move(role)
        print("player moved to", player.tile)

        #tile action phase
        if player.tile == 24: #on go to jail 
            player.tile = 8 #reset player position to jail
            player.timesJailed += 1 #for player stats

        elif player.tile == 0 or player.tile == 16 or player.tile == 8: # if the player is on GO or Jail do nothing
            t = player.tile
            if t == 0 or t == 16:
                print("player", player.id, "landed on GO")
            else:
                print("player", player.id, "is visiting jail")

        else: #can purchase tile
            purResult = b.purchase(player) #tried to purchase tile from the board object
            if purResult == 2: # successful

                player.canPurchase(b) # purchasing decision is based on the player agent

                print("player", player.id, "bought", player.tile)
            elif purResult == 0: # not enough money
                print("player", player.id, "does not have enough money to buy", player.tile)
            else: # already owned
                print("property already owned")
        loop += 1
        curTime = time.time()




#prints out stats from the game
def stats():
    print("--------------")
    print("STATS")
    print("--------------")

    print("player one starting position:", player.startingPos)
    print("money:", player.money)
    print("number of roles:", rounds)
    print("roles:", player.roles)
    print("path:", player.path)
    print("properties:", player.properties)
    print("--------------")
    #print(b.tiles)





gameSetup()
main()
stats()