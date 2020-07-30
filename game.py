#QUICK RUNDOWN
# this file sets up a global board object and player objects for each game instance,
# it then creates threads for each player and runs the game on the shared board
# the individual player classes handle how long each action takes  --- (so far I only have the one)
# but there is a global timer that controls how long the game lasts

#multiple games can be simulated in the automator.py file

#custom classes
import player
import consPlayer
import strategicPlayer

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
# '--' in progress
# '---' being tested
# '+' complete

#TODO + Add mutex lock around global board object
#TODO + chance card class
#TODO + community chest card class

#TODO --- Add method in the player class that adds up all money at the end of the game - need cards first
#TODO -- Print data to CSV at end of the game
    # need to save different files instead of writing over the same one
#TODO --- stats for each round - total at end
#TODO - with and without chance cards
    #option trading round or optional chance cards
#TODO - print board in a readable format
    #less important
#TODO add one more layer for the tie check
#TODO -- read in final csv
#TODO -- support for different player types

#non code todos
#TODO get accurate timing for the player actions
    #the way it works right now is the payer finished their turn
    #even after the timer ends - the threads line back up but the rounds last longer than they should
    #I dont know how to fix this without a lot of added complexity - but it varies up to 6 seconds
        # add "playing" boolean thats checked during the buying method
#TODO python logging class ?? i dont know what this is but it sounds promising
#TODO right now it checks for time after the role, so a player can move to a space but not have time to buy it



block = threading.Lock() # mutex for the board
c_lock = threading.Lock() # mutex for the card decks

#initialize game elements

#CONTROL BOARD BABY - these are overridden by the run() method
b = board.Board()
rounds = 10 #for testing
players = []
gameLength = 30.0
chanceDeck = cards.ChanceDeck()
commDeck = cards.CommChestDeck()
report = True
curTime = time.time() 
endTime = curTime + gameLength
startTime =curTime
gameCount = 0
bs = [30.0,2.0,2.0,1.0]
ts = [2.0,2.0,2.0,2.0]
player1 = player.Player("JIMMY")
player2 = player.Player("THERESA")
player1.startingPos = 0
player2.startingPos = 0
players.append(player1)
players.append(player2)


#sets up and runs a game instance
"""
####################################################################################################################
"""
def run(numPlayers, startingPos, length, gameNumber, post, types, trading, buyStage = bs, tradeStage = ts):
    #jesus christ theres got to be a better way than this
    global bs
    bs = buyStage
    global ts
    ts = tradeStage
    
    global chanceDeck
    chanceDeck = cards.ChanceDeck()
    global commDeck
    commDeck = cards.CommChestDeck()
    global report
    report = post
    global gameCount
    gameCount = gameNumber
    global b
    b = board.Board()
    global players
    players = []
    global block 
    block = threading.Lock() # mutex for the board
    global c_lock
    c_lock = threading.Lock() # mutex for the card decks

    for i in range(0,numPlayers):
        tempPlayer = player.Player(i)
        if types[i] == "c": #conservative player
            tempPlayer = consPlayer.ConsPlayer(i+1)
        elif types[i] == "g": #greedy player
            tempPlayer = player.Player(i+1)
        elif types[i] == "s": #strategic player
            tempPlayer = strategicPlayer.StrategicPlayer(i+1)
        tempPlayer.startingPos = startingPos[i]
        players.append(tempPlayer)

    print("\nSTARTING GAME", gameCount)
    if not report:print("playing...")

    #give players money and cards
    gameSetup()
    #prints greeting
    if report:lezgo() 

    global curTime 
    curTime = time.time() 
    global endTime 
    endTime = curTime + length
    global startTime
    startTime = curTime

    #creates threads and plays game
    if trading: start()
    else: noTradeStart()
    #gives rewards at the end of the game
    payout()
    #prints the stats of the game
    if report: printStats()
    #saves stats to CSV
    stats = printCSV()
    return stats #return dataframe




################
# GAME METHODS #
################




def gameSetup():
    #initialize player(s)
    for player in players:
        player.money += 5000 # starts with 5000
        player.chance = chanceDeck.pullChanceCards()
        player.commChest = commDeck.pullChestCards()
   
#runs the game as one long buying round - mainly for testing
def noTradeGame(player):
    global curTime 
    curTime = time.time()
    global endTime 
    player.tile = player.startingPos
    
    while curTime <= endTime:
        buyRound(player, endTime)
        curTime = time.time()

#runs the buying stage of the game for a player for a certain amount of time
def buyStage(player, rEndTime):
    # print("buying")
    curTime = time.time()
    startTime = curTime
    player.tile = player.startingPos
    while curTime <= rEndTime:
        buyRound(player,rEndTime)
        curTime = time.time()
    print("P",player.id,"buying", curTime - startTime)

#runs the trading stage for a player for a certain amount of time
def tradeStage(player, rEndTime):
    curTime = time.time()
    startTime = curTime
    while curTime <= rEndTime:
        tradeRound(player)
        curTime = time.time()
    print("P",player.id,"trading", curTime - startTime)

#this handles each move the player makes - and any purchases made during that turn
def buyRound(player, endTime):
    player.move(report)
    if time.time() >= endTime: return # checks for time after the move - so right now the player can land on a space but not have time to buy it
    if report: 
        if player.type != "conservative":sys.stdout.write("player " + str(player.id) + " moved to " + str(player.tile) + "\n")
        else: sys.stdout.write("player " + str(player.id) + " moved to " + str(player.tile) + " but is speeding along" "\n")
    #tile action phase
    if player.tile == 24: #on go to jail 
        time.sleep(1) #-------------------------------------going to jail penalty
        player.tile = 8 #reset player position to jail
        player.path.append(8)
        player.timesJailed += 1 #record count

    elif player.tile == 0 or player.tile == 16 or player.tile == 8: # if the player is on GO or Jail do nothing
        if player.tile == 0 or player.tile == 16:
            if report: sys.stdout.write("player " + str(player.id) + " landed on GO " + "\n")
        else:
            if report: sys.stdout.write("player " + str(player.id) + " is visiting jail " + "\n")

    elif player.tile > 0 and player.tile < 32: #can purchase tile
        purResult = b.purchase(player)
        if purResult == 2: # successful
            player.canPurchase(b, report, block)
        elif purResult == 0: # not enough money
            if report: sys.stdout.write("player " + str(player.id) + " does not have enough money to buy " + str(player.tile)  + "\n")
        else:
            if report: sys.stdout.write("property " + str(player.tile) +  " already owned "  + "\n")
    else: print("something went very wrong -> player jumped the board") 

#this will handle the trading round but dear god is it daunting
#global variables that indicated when a trade is taking place
#it will lock for only one player at a time can trade
#each player will be checking

#upload to a global list - each player then
def tradeRound(player):
    pass

#this starts a game consisting of one long buy round
def noTradeStart():
    threads = list()
    for player in players: #creates a thread for each player
        if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id)  + '\n' + '\n')
        playerThread = threading.Thread(target=noTradeGame, args=(player,))
        threads.append(playerThread) #adds to list
    for playerThread in threads: #starts each thread
        playerThread.start() #starts each player
    for index, thread in enumerate(threads): #waits for each thread to end before moving forward
        thread.join() #shouldn't be necessary but here just in case

#this runs a game alternating between buying and trading rounds
def start():
    global curTime

    for r in range(4):
        print("Starting Round", r)
        threads = list()
        for player in players: #creates a thread for each player
            # if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id)  + '\n' + '\n')
            endTime = curTime + bs[r]
            playerThread = threading.Thread(target=buyStage, args=(player,endTime))
            threads.append(playerThread) #adds to list
        for playerThread in threads: #starts each thread
            playerThread.start() #starts each player
        for index, thread in enumerate(threads): #waits for each thread to end before moving forward
            thread.join() #shouldn't be necessary but here just in case

        threads.clear()

        curTime = time.time()

        for player in players: #creates a thread for each player
            # if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id)  + '\n' + '\n')
            endTime = curTime + ts[r]
            playerThread = threading.Thread(target=tradeStage, args=(player,endTime))
            threads.append(playerThread) #adds to list
        for playerThread in threads: #starts each thread
            playerThread.start() #starts each player
        for index, thread in enumerate(threads): #waits for each thread to end before moving forward
            thread.join() #shouldn't be necessary but here just in case
        print("")
        curTime = time.time()





###############################
# POST GAME AND PRINT METHODS #
###############################






#runs at end of game
#gives players money at the end of the game for community chest and properties
#also determines the winner
def payout():
    if report: print("--------------------------\n          PAYOUT       \n--------------------------")
    winningAmount = 0
    winners = []
    for player in players:
        if report: print("\n --payout for community chest", player.id, "--")
        commDeck.payout(player, report)
        if report: print("\n")

        player.calculateMoney()
    
        if player.money >= winningAmount:
            winningPlayer = player
            winningAmount = winningPlayer.money

    for player in players:
        if player.money == winningAmount:
            winners.append(player)

    if len(winners) > 1: # if theres a tie on money compare number of properties
        winningPropAmount = 0
        for player in players:
            propAmount = len(player.properties)
            if propAmount >= winningPropAmount:
                winningPropAmount = propAmount
                winningPlayer = player
        
        winners = []
        for player in players: # test for property tie
            if len(player.properties) == winningPropAmount:
                winners.append(player)

        if len(winners) > 1: # if there a tie on money and properties then call it a draw
            for player in winners:
                player.winner = True
    winningPlayer.winner = True


#prints out stats from the game <- possible logging class? 
#maybe straight to google drive? messy but dope
def printStats(): 
    print("--------------------------")
    print("          STATS")
    print("--------------------------")

    for player in players:

        print("------------------")
        print("---- PLAYER", player.id, "----")
        print("winner:", player.winner)
        print("type:", player.type)
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
        
    b.print()

#prints the output to a csv file
#then reads it back in and prints it all pretty like - just make sure to give it enough room in the terminal window
def printCSV():
    if report: print("\nprinting to CSV\n")
    with open ('output.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output.writerow(['ID','player_type','winner?','Total_Money','Money_from_GO','Money_from_Chest','Money_from_properties','Starting_Pos','num_moves','Passed_go','Jail','Properties','Chest_Cards'])
        for player in players:
            playerChestCardsID = []
            for i in range(len(player.commChest)):
                playerChestCardsID.append(player.commChest[i][0])
            output.writerow([player.id,player.type, player.winner, player.money, player.mGo, player.mChest, player.mProp, player.startingPos, player.numRoles, player.timesPassedGo, player.timesJailed, player.properties,playerChestCardsID])
        strCount = str(gameCount)
        output.writerow([''])
    df = pandas.read_csv('output.csv', index_col='ID')
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
