#QUICK RUNDOWN
# this file sets up a global board object and player objects for each game instance,
# it then creates threads for each player and runs the game on the shared board
# the individual player classes handle how long each action takes  --- (so far I only have the one)
# but there is an global timer that controls how long the game lasts
# each player gets its own thread so they all run at their own speed, this is cool but causes a MESS of the print statements 
#       so for testing should probably look at one agent at a time

#TODO chance card class
#TODO community chest card class
#TODO Add mutex lock around global board object
#TODO Add method in the player class that adds up all money at the end of the game - needs cards first
#TODO Print data to CSV at end of the game

#TODO python logging class ?? i dont know what this is but it sounds promising

#this is where the magic happens, run this file to run the simulation

#custom classes
import player
import board

#Python libraries
import random
import time
import threading



#initialize board
b = board.Board()
rounds = 10 #for testing
players = []


#this is gross
#initialize players
# player1 = player.Player(1)
# player2 = player.Player(2)
# player1.startingPos = 0
# player2.startingPos = 16
# players.append(player1)
# players.append(player2)

#automates
numPlayers = 2
for x in range(numPlayers):
    playerX = player.Player(x+1)
    playerX.startingPos = 0
    players.append(playerX)




def gameSetup(players):
    #initialize player(s)
    for player in players:
        player.money += 5000 # starts with 5000
        for cards in range(4):
            player.chance.append("random chance card") # four chance cards
            if cards < 3:
                player.chance.append("random community chest card") # three community chest cards
        #player.startingPos = 16 # where to start


   
#runs the game
def main(player):
    print("--------------")
    print("STARTING GAME FOR PLAYER", player.id)
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
        print("player", player.id, "moved to", player.tile)

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
#TODO save to CSV at some point
def stats(players): 

    print("--------------")
    print("STATS")
    print("--------------")

    for player in players:

        print("PLAYER", player.id)
        print("player one starting position:", player.startingPos)
        print("money:", player.money)
        print("number of roles:", rounds)
        print("roles:", player.roles)
        print("path:", player.path)
        print("properties:", player.properties)
        print("--------------")
    #print(b.tiles)




gameSetup(players) #setup players

#start game timer
curTime = time.time() 
endTime = curTime + 30.0 

#jenky multithreading but it kinda works.. just ignore the print statement mess
threads = list()
for player in players: #runs once for each player
    playerThread = threading.Thread(target=main, args=(player,)) #creates thread at main()
    threads.append(playerThread) #adds to list
    playerThread.start() #starts

for index, thread in enumerate(threads):
    thread.join() #rejoin threads



stats(players)