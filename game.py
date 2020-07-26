#QUICK RUNDOWN
# this file sets up a global board object and player objects for each game instance,
# it then creates threads for each player and runs the game on the shared board
# the individual player classes handle how long each action takes  --- (so far I only have the one)
# but there is an global timer that controls how long the game lasts


# key for todos:
# '-' started
# '--' finished but needs testing
# '---' being tested
# '+' complete


#TODO -- Add mutex lock around global board object
#TODO --- chance card class
#TODO --- community chest card class
#TODO --- Add method in the player class that adds up all money at the end of the game - need cards first
#TODO -- Print data to CSV at end of the game
            # need to save different files instead of writing over the same one
#TODO ---stats for each round - total at end
#TODO - with and without chance cards
#TODO print board in a readable format


#TODO python logging class ?? i dont know what this is but it sounds promising



#this is where the magic happens, run this file to run the simulation

#custom classes
import player
import board
import cards

#Python libraries
import random
import time
import threading
import sys #for atomic print commands
import csv
import pandas

block = threading.Lock() # mutex for the board
c_lock = threading.Lock() # mutex for the card decks

#initialize game elements

#board
b = board.Board()
rounds = 10 #for testing
players = []
gameLength = 60.0
#cards
chanceDeck = cards.ChanceDeck()
commDeck = cards.CommChestDeck()

#players
player1 = player.Player("JIMMY")
player2 = player.Player("THERESA")
player1.startingPos = 0
player2.startingPos = 16
players.append(player1)
players.append(player2)

# #automates
# numPlayers = 2
# for x in range(numPlayers):
#     playerX = player.Player(x+1)
#     playerX.startingPos = 0
#     players.append(playerX)


def gameSetup(players):
    #initialize player(s)
    for player in players:
        player.money += 5000 # starts with 5000
        for cards in range(4):
            player.chance.append("random chance card") # four chance cards
            if cards < 3:
                player.chance.append("random community chest card") # three community chest cards

   
#runs the game
def main(player):

    c_lock.acquire() #mutex for the cards decks
    player.chance = chanceDeck.pullChanceCards()
    player.commChest = commDeck.pullChestCards()
    c_lock.release()

    # sys.stdout.write("-----------------------------------------------" + '\n')
    sys.stdout.write("STARTING GAME FOR " + str(player.id)  + '\n' + '\n')
    # sys.stdout.write("-----------------------------------------------" + '\n')

    global curTime
    player.tile = player.startingPos

    loop = 1
    # for _ in range(0,rounds):
    while curTime <= endTime:
        #print("starting round:", loop)
        #role phase
        
        role = random.randint(1,6) #might move this to the player class
        player.move(role)
        player.numRoles += 1 #same with this


        sys.stdout.write("player " + str(player.id) + " moved to " + str(player.tile) + "\n")

        #tile action phase
        if player.tile == 24: #on go to jail 
            block.acquire()
            player.tile = 8 #reset player position to jail
            player.path.append(8)
            player.timesJailed += 1 #for player stats
            block.release()

        elif player.tile == 0 or player.tile == 16 or player.tile == 8: # if the player is on GO or Jail do nothing
            t = player.tile
            if t == 0 or t == 16:
                sys.stdout.write("player " + str(player.id) + " landed on GO " + "\n")
            else:
                sys.stdout.write("player " + str(player.id) + " is visiting jail " + "\n")

        else: #can purchase tile
            block.acquire() #locks board

            purResult = b.purchase(player) #tried to purchase tile from the board object
            if purResult == 2: # successful
                sys.stdout.write("player " + str(player.id) + " bought " + str(player.tile)  + "\n")
                player.canPurchase(b)
            elif purResult == 0: # not enough money
                sys.stdout.write("player " + str(player.id) + " does not have enough money to buy " + str(player.tile)  + "\n")
            else: # already owned
                sys.stdout.write("property already owned "  + "\n")

            block.release() # locks board
        loop += 1
        curTime = time.time()

    #after the game ends
    # sys.stdout.write("\n"+ "decks testing - pre payout" +"\n")
    # sys.stdout.write(str(player.id) + "pre money: " + str(player.money))
    # c_lock.acquire()
    # commDeck.payout(player) # does this need a mutex
    # c_lock.release()
    # sys.stdout.write(str(player.id)+ " cards: " + str(player.commChest) + "\n")
    # sys.stdout.write(str(player.id) + " post money: " + str(player.money))
    # sys.stdout.write("\n"+ "decks testing - pre payout" +"\n")


#prints out stats from the game <- possible logging class? 
#maybe straight to google drive? messy but dope

def stats(players): 
    print("---------------------------")
    print("           STATS")
    print("---------------------------")

    for player in players:

        print("---- PLAYER", player.id, "----")
        print("Starting position:", player.startingPos)
        print("Times passed GO:", player.timesPassedGo)
        print("Times jailed:", player.timesJailed)
        print("Money:", player.money)
        print("Number of roles:", player.numRoles)
        print("Roles:", player.roles)
        print("Path:", player.path)
        print("Properties:", player.properties)
        print("------------------")
    b.print()

#prints the output to a csv file
#then reads it back in and prints it all pretty like - just make sure to give it enough room 
#in the terminal window
def printCSV():
    print("printing to CSV", '\n')
    with open ('output.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output.writerow(['P_ID','Money','S_Pos','GO','Jail','Props'])
        for player in players:
            output.writerow([player.id, player.money,player.startingPos, player.timesPassedGo, player.timesJailed, player.properties])
    df = pandas.read_csv('output.csv', index_col='P_ID')
    print(df)

gameSetup(players) #setup players

def lezgo():
    for i in range(20):
        print("-----------------------------------------------")
        if i == 6: print("------< STARTING >-----------------------------")
        if i == 9: print("----------------< MONOPOLY >-------------------")
        if i == 12: print("--------------------------< SPEED >------------")
lezgo()


#start game timer
curTime = time.time() 
endTime = curTime + gameLength

#multithreading - one for each player running at main()
threads = list()
for player in players: #creates a thread for each player
    playerThread = threading.Thread(target=main, args=(player,))
    threads.append(playerThread) #adds to list
for playerThread in threads: #starts each thread
    playerThread.start() #starts each player
for index, thread in enumerate(threads): #waits for each thread to end before moving forward
    thread.join() #shouldn't be necessary but here just in case


print(" ------------------\n       PAYOUT       \n ------------------")
for player in players:
    print("\n --payout for community chest", player.id, "--")
    commDeck.payout(player)

stats(players)
printCSV()









