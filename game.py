#QUICK RUNDOWN
# this file sets up a global board object and player objects for each game instance,
# it then creates threads for each player and runs the game on the shared board
# the individual player classes handle how long each action takes  --- (so far I only have the one)
# but there is an global timer that controls how long the game lasts

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

# key for todos:
# '-' started
# '--' finished but needs testing
# '---' being tested
# '+' complete

#TODO --- Add mutex lock around global board object
#TODO --- chance card class
#TODO --- community chest card class
#TODO --- Add method in the player class that adds up all money at the end of the game - need cards first
#TODO -- Print data to CSV at end of the game
            # need to save different files instead of writing over the same one
#TODO ---stats for each round - total at end
#TODO - with and without chance cards
#TODO - print board in a readable format

#TODO python logging class ?? i dont know what this is but it sounds promising

#this is where the magic happens, run this file to run the simulation

block = threading.Lock() # mutex for the board
c_lock = threading.Lock() # mutex for the card decks

#initialize game elements

#CONTROL BOARD BABY - obsolete
b = board.Board()
rounds = 10 #for testing
players = []
gameLength = 30.0
#cards
chanceDeck = cards.ChanceDeck()
commDeck = cards.CommChestDeck()

report = True

curTime = time.time() 
endTime = curTime + gameLength

#players
player1 = player.Player("JIMMY")
player2 = player.Player("THERESA")
player1.startingPos = 0
player2.startingPos = 0
players.append(player1)
players.append(player2)

#sets up and runs a game instance
def run(numPlayers, startingPos, length, rounds, post):
    global report
    report = post
    
    for r in range(rounds):
        print("\nSTARTING GAME", r+1)
        global b
        b = board.Board()
        global players
        players = []

        global block 
        block = threading.Lock() # mutex for the board
        global c_lock
        c_lock = threading.Lock() # mutex for the card decks

        for i in range(1,numPlayers+1):
            tempPlayer = player.Player(i)
            tempPlayer.startingPos = startingPos
            players.append(tempPlayer)

        global curTime 
        curTime = time.time() 
        global endTime 
        endTime = curTime + length

        #give players money and cards
        gameSetup()
        #prints greeting
        if report:lezgo() 
        #creates threads and plays game
        start()
        #gives rewards at the end of the game
        payout()
        #prints the stats of the game
        if report: printStats()
        #saves stats to CSV
        stats = printCSV()
        return stats

#sets up players using terminal input
def manualSetup():
    numPlayers = int(input("how many players: ")) #freaks out if you dont pass a1n int
    for count in range(1,numPlayers+1):
        print(numPlayers)
        sys.stdout.write("what would you like player " + str(count))
        playerID = input(" to be called? ")
        player_t = player.Player(playerID)
        startPos = -1
        while(startPos != "1" and startPos != "2"):
            startPos = input("type '1' or '2' to choose your starting position: ")
            int(startPos)
            print(type(startPos))
            if startPos != "1" and startPos != "2":
                print("please type either 'first' or 'second'")
        if startPos == "1": player.startingPos = 0
        elif startPos == "2": player.startingPos = 16
        else: print("something went wrong with your starting position please start over")
        players.append(player_t)

def gameSetup():
    #initialize player(s)
    for player in players:
        player.money += 5000 # starts with 5000
        player.chance = chanceDeck.pullChanceCards()
        player.commChest = commDeck.pullChestCards()
   
#runs the game
def main(player):

    if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id)  + '\n' + '\n')
    time.sleep(0.5)
    global curTime
    player.tile = player.startingPos

    loop = 1
    # for _ in range(0,rounds):
    while curTime <= endTime:
        #print("starting round:", loop)
        #role phase
        
        role = random.randint(1,6) #might move this to the player class
        player.move(role, report)
        player.numRoles += 1 #same with this


        if report: sys.stdout.write("player " + str(player.id) + " moved to " + str(player.tile) + "\n")

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
                if report: sys.stdout.write("player " + str(player.id) + " landed on GO " + "\n")
            else:
                if report: sys.stdout.write("player " + str(player.id) + " is visiting jail " + "\n")

        else: #can purchase tile
            block.acquire() #locks board

            purResult = b.purchase(player) #tried to purchase tile from the board object
            if purResult == 2: # successful
                if report: sys.stdout.write("player " + str(player.id) + " bought " + str(player.tile)  + "\n")
                player.canPurchase(b)
            elif purResult == 0: # not enough money
                if report: sys.stdout.write("player " + str(player.id) + " does not have enough money to buy " + str(player.tile)  + "\n")
            else: # already owned
                if report: sys.stdout.write("property already owned "  + "\n")

            block.release() # locks board
        loop += 1
        curTime = time.time()


#prints out stats from the game <- possible logging class? 
#maybe straight to google drive? messy but dope

def printStats(): 
    print("--------------------------")
    print("          STATS")
    print("--------------------------")

    for player in players:

        print("---- PLAYER", player.id, "----")
        print("winner:", player.winner)
        print("Starting position:", player.startingPos)
        print("Times passed GO:", player.timesPassedGo)
        print("Times jailed:", player.timesJailed)
        print("Money:", player.money)
        print("Money from Properties:", player.mProp)
        print("Money from GO:", player.mGo)
        print("Money from community chest:", player.mChest)
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
    if report: print("\nprinting to CSV\n")
    with open ('output.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output.writerow(['P_ID','winner?','Total_Money','Money_from_GO','Money_from_Chest','Money_from_properties','S_Pos','go','Jail','Props'])
        for player in players:
            output.writerow([player.id, player.winner, player.money, player.mGo, player.mChest, player.mProp, player.startingPos, player.timesPassedGo, player.timesJailed, player.properties])
    
    df = pandas.read_csv('output.csv', index_col='P_ID')
    # df = pandas.read_csv('output.csv')
    if report: print(df)
    return df


def lezgo():
    for i in range(20):
        print("-----------------------------------------------")
        if i == 6: print("------< STARTING >-----------------------------")
        if i == 9: print("----------------< MONOPOLY >-------------------")
        if i == 12: print("--------------------------< SPEED >------------")
    print("")


#start game timer

#multithreading - one for each player running at main()
def start():
    threads = list()
    for player in players: #creates a thread for each player
        playerThread = threading.Thread(target=main, args=(player,))
        threads.append(playerThread) #adds to list
    for playerThread in threads: #starts each thread
        playerThread.start() #starts each player
    for index, thread in enumerate(threads): #waits for each thread to end before moving forward
        thread.join() #shouldn't be necessary but here just in case


def payout():
    if report: print("--------------------------\n          PAYOUT       \n--------------------------")
    winningAmount = 0
    for player in players:
        if report: print("\n --payout for community chest", player.id, "--")
        commDeck.payout(player, report)
        if report: print("\n")

        player.calculateMoney()
    
        if player.money >= winningAmount:
            winningPlayer = player
            winningAmount = winningPlayer.money
        
    winningPlayer.winner = True


# curTime = time.time() 
# endTime = curTime + gameLength

#GAME METHODS
# manualSetup() # set up players through terminal input
# gameSetup(players)
# lezgo() #important
# start(players)
# payout(players)
# printStats(players)
# printCSV(players)

#automates game creation
#inputs(number of players, starting position, length of the game, number of rounds)
# run(3, 0, 10.0, 1, True)
