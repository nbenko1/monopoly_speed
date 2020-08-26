#QUICK RUNDOWN
# this file sets up a global board object and player objects for each game instance,
# it then creates threads for each player and runs the game on the shared board
# the individual player classes handle how long each action takes
# and there is a global timer that controls how long the game lasts

#run games form the automator.py file

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

#-------------------------------------------------------------------------------------------------------------------
# key for todos:
# '-' started
# '--' in progress
# '---' being tested
# '+' complete

#-------------finished
# + Add mutex lock around global board object
# + chance card class
# + community chest card class
# + read in final csv
# + support for different player types
# + Add method in the player class that adds up all money at the end of the game - need cards first
# + Print data to CSV at end of the game
# + stats for each round - total at end
# + with and without chance cards
# + Chance cards
# + test "findWantedProperty()"
# + get accurate timing for the player actions

#------------main goals
#TODO --- which chest cards gave which money - more detailed??


#-------------non code todos and figure outs

#-------------less important
#TODO - print board in a readable format
#TODO - add one more layer to the tie check

#-------------------------------------------------------------------------------------------------------------------


block = threading.Lock() # mutex for the board
# c_lock = threading.Lock() # mutex for the card decks
t_lock = threading.Lock() # mutex for the trading round

#initialize game elements

#TESTING CONTROL BOARD - these are overridden by the run() method
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
bs = [30.0,20.0,20.0,10.0]
# ts = [40.0,50.0,70.0,70.0]
ts = [5.0,5.0,5.0,5.0]
player1 = player.Player("JIMMY")
player2 = player.Player("THERESA")
player1.startingPos = 0
player2.startingPos = 0
players.append(player1)
players.append(player2)
randomTime = False
quickTiming = 1.0
OfficialStartTime = 0.0
OfficialEndTime = 0.0


#sets up and runs a game instance
"""
####################################################################################################################
"""
#this method sets up and runs games depending on the input
def run(numPlayers, startingPos, length, gameNumber, post, types, trading, timing, randomFactor, buyStage, tradeStage, points,
        player1Chest, player2Chest, player3Chest, player4Chest,
        player1Chance, player2Chance, player3Chance, player4Chance):

    chooseChest = [player1Chest, player2Chest, player3Chest, player4Chest]
    chooseChance = [player1Chance, player2Chance, player3Chance, player4Chance]

    global bs # array with lengths for each buying stage
    bs = buyStage
    global ts # array of lengths for each trading stage
    ts = tradeStage

    global quickTiming # mutliplier for the wait command lengths
    quickTiming = timing
    global randomTime
    randomTime = randomFactor
    
    global chanceDeck # chance deck for this particular game 
    chanceDeck = cards.ChanceDeck()
    global commDeck # communty chest deck for this game
    commDeck = cards.CommChestDeck()
    global report # boolean indicating whether to print real time game updates
    report = post
    global gameCount # current game number
    gameCount = gameNumber
    global b # board object
    b = board.Board()
    global players # array of players
    players = []
    global block  #mutex lock for the board object
    block = threading.Lock() # mutex for the board
    # global c_lock # mutex lock for the card decks
    # c_lock = threading.Lock() # mutex for the card decks

    #reads in array of player types and creates each one
    for i in range(0,numPlayers): 
        tempPlayer = player.Player(i)
        if types[i] == "c": #conservative player
            tempPlayer = consPlayer.ConsPlayer(i+1)
        elif types[i] == "g": #greedy player
            tempPlayer = player.Player(i+1)
        elif types[i] == "s": #strategic player
            tempPlayer = strategicPlayer.StrategicPlayer(i+1)
        else: 
            print("bad player type input")
            return
        tempPlayer.startingPos = startingPos[i] # sets starting position for each player
        tempPlayer.points = points[i] # tracks number of points through multiple rounds
        players.append(tempPlayer) # add to total list of players

    print("\nSTARTING GAME", gameCount)
    if not report: print("playing...")

    #give players money and cards
    gameSetup(players, chooseChest, chooseChance)

    #prints greeting
    if report:lezgo() 

    # starts timers
    global curTime 
    curTime = time.time() 
    global endTime 
    endTime = curTime + length
    global startTime
    startTime = curTime
    global OfficialStartTime
    OfficialStartTime = curTime
    

    #creates threads and plays game
    if trading: start()
    else: noTradeStart()

    global OfficialEndTime
    OfficialEndTime = time.time() # records end time

    #gives rewards at the end of the game
    payout(players)

    #prints the stats of the game
    if report: printStats()

    #saves stats to CSV
    stats = printCSV()

    #return dataframe
    return stats 



def gameSetup(players, chooseChest, chooseChance):
    #initialize player(s)
    for i in range(len(players)):
        player = players[i]
        player.money += 5000 # starts with 5000

        if len(chooseChest[i]) == 3: 
            print("choosing specific Chest cards")
            player.commChest = commDeck.pullSpecChestCards(chooseChest[i])
        else: player.commChest = commDeck.pullChestCards()

        if len(chooseChance[i]) == 4: 
            print("choosing specific Chance cards")
            player.chance = chanceDeck.pullSpecChanceCards(chooseChance[i])
        else: player.chance = chanceDeck.pullChanceCards()
        for card in player.chance:
            card[1] == 1 # set status of each card to unused
        




################
# GAME METHODS #
################




   
#runs the game as one long buying round
def noTradeGame(player):
    global curTime 
    curTime = time.time()
    global endTime 
    player.tile = player.startingPos
    
    while curTime <= endTime:
        buyRound(player, endTime)
        curTime = time.time()

#runs the buying stage of the game for a single player for a specified amount of time
def buyStage(player, rEndTime):
    # print("buying")
    curTime = time.time()
    startTime = curTime
    player.tile = player.startingPos
    while curTime <= rEndTime:
        buyRound(player,rEndTime)
        curTime = time.time()
    # print("P",player.id,"buying", curTime - startTime)

#runs the trading stage for a player for a certain amount of time
def tradeStage(player, rEndTime):
    curTime = time.time()
    startTime = curTime
    tradeRound(player)
    while curTime <= rEndTime: # uncomment this to have the trade round take the normal amount of time -> doesn't change the game
        curTime = time.time()
    # print("P",player.id,"trading", curTime - startTime)

#this handles each move the player makes - and any purchases made during that turn
def buyRound(player, endTime):
    global quickTiming
    global randomTime
    if time.time() + 1.5/quickTiming >= endTime: return # makes sure there is 1.5 seconds to move the piece
    player.move(report, quickTiming, randomTime)
    if time.time() + 1.5/quickTiming >= endTime: return # checks for time after the move - makes sure theres at least 1.5 seconds to make the move

    #tile action phase
    if player.tile == 24: #on go to jail 
        
        player.wait(0.5, 0.8, quickTiming, randomTime)#-----------------------------------------------------------------------------

        player.tile = 8 #reset player position to jail
        player.path.append(8)
        player.timesJailed += 1 #record count

    elif player.tile == 0 or player.tile == 16 or player.tile == 8: # if the player is on GO or Jail do nothing
        if player.tile == 0 or player.tile == 16:
            if report: sys.stdout.write("player " + str(player.id) + " landed on GO " + "\n")
        else:
            if report: sys.stdout.write("player " + str(player.id) + " is visiting jail " + "\n")

    elif player.tile > 0 and player.tile < 32: #can purchase tile
        # sys.stdout.write("--player " + str(player.id) + " trying to acquire block " + "\n")
        block.acquire() #mutex lock around board
        # sys.stdout.write("--player " + str(player.id) + " got block " + "\n")
    
        purResult = b.purchase(player)
        if purResult == 2: # successful
            player.canPurchase(b, report, block, quickTiming, randomTime)
        elif purResult == 0: # not enough money
            if report: sys.stdout.write("player " + str(player.id) + " does not have enough money to buy " + str(player.tile)  + "\n")
            block.release() #release mutex
            # sys.stdout.write("--player " + str(player.id) + " released block " + "\n")
        else:
            if report: sys.stdout.write("property " + str(player.tile) +  " already owned "  + "\n")
            block.release() #release mutex
            # sys.stdout.write("--player " + str(player.id) + " released block " + "\n")
        
        
    else: print("something went very wrong -> player jumped the board") 


# handles the trading round for each player individually
# ecah player plays a chance card one at a time, when they're all done the round ends
def tradeRound(player):
    global t_lock
    # sys.stdout.write("\n" + "ENTERING TRADING STAGE" + "\n")

    # each player plays a card - one at a time
    # sys.stdout.write("player " + str(player.id) + " is requesting t_lock" +"\n")
    t_lock.acquire()
    # sys.stdout.write("player " + str(player.id) + " got it" +"\n")

    player.playChance(players,b, report)
    # time.sleep(1) # slight delay so printing doesn't go by too fast
    t_lock.release()
    # sys.stdout.write("player " + str(player.id) + " released it" +"\n")



#this starts a game consisting of one long buy round
def noTradeStart():
    threads = list()
    for player in players: #creates a thread for each player
        if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id) + " type: " + str(player.type) + '\n' + '\n')
        playerThread = threading.Thread(target=noTradeGame, args=(player,))
        threads.append(playerThread) #adds to list
    for playerThread in threads: #starts each thread
        playerThread.start() #starts each player
    for index, thread in enumerate(threads): #waits for each thread to end before moving forward
        thread.join() #shouldn't be necessary but here just in case

#this runs a game alternating between buying and trading rounds
def start():
    global curTime
    global b

    for r in range(0,4): # plays four rounds of buy-trade stages
       
       #buy round
        print("\n","               Buying Round", r+1, "\n", "              ----------------\n")
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
        print("\n","               Trading Round", r+1, "\n", "              -----------------\n")
        curTime = time.time()

        #trade round
        for player in players: #creates a thread for each player
            # if report: sys.stdout.write("STARTING GAME FOR PLAYER " + str(player.id)  + '\n' + '\n')
            endTime = curTime + ts[r] # checks how long this round should take
            playerThread = threading.Thread(target=tradeStage, args=(player,endTime)) # calls method
            threads.append(playerThread) #adds to list
        for playerThread in threads: #starts each thread
            playerThread.start() #starts each player
        for index, thread in enumerate(threads): #waits for each thread to end before moving forward
            thread.join() #shouldn't be necessary but here just in case
        print("")


        if report: b.print()


        curTime = time.time()






###############################
# POST GAME AND PRINT METHODS #
###############################






#runs at end of game
#gives players money at the end of the game for community chest and properties
#also determines the winner
def payout(players):
    # report = False #for testing
    if report: print("--------------------------\n          PAYOUT       \n--------------------------")
    winningAmount = 0
    winners = []
    for player in players:
        if report: print("\n --community chest payout for player", player.id, "--")
        commDeck.payout(player, report)
        if report: print("\n")

        player.calculateMoney()
    
        if player.money >= winningAmount:
            winningAmount = player.money

    for player in players:
        if player.money == winningAmount:
            winners.append(player)

    # if len(winners) > 1: # if theres a tie on money compare number of properties
    #     winningPropAmount = 0
    #     for player in winners: # finds the player with the most properties out of the players who tied for most money
    #         propAmount = len(player.properties)
    #         if propAmount >= winningPropAmount:
    #             winningPropAmount = propAmount
        
    #     propWinners = []
    #     for player in winners: # test for property tie
    #         if len(player.properties) == winningPropAmount:
    #             propWinners.append(player)
    #     winners = propWinners

    if len(winners) > 1:
        for player in winners:
            player.winner = "Tie"
    else: 
        for player in winners:
            player.winner = "Winner"

    for player in players:
        if player.winner == "Winner":
            player.points += 1.0
        elif player.winner == "Tie":
            player.points += 0.5

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
        # print("Roles:", player.roles)
        print("Path:", player.path)
        print("Properties:", player.properties)
        
    b.print()
    print("")



#prints the output to a csv file
#then reads it back in and prints it all pretty like
def printCSV():
    gameTime = OfficialEndTime - OfficialStartTime
    if report: print("\nprinting to CSV\n")
    with open ('output.csv', mode='w') as output:
        output = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


        

########################
#    CHANGE HEADER     #
########################
        output.writerow(['ID',
                        'Player Type',
                        'Winner?',
                        'Points',
                        'Total Money',
                        'Money from GO',
                        'Money from Chest',
                        'Money from properties',
                        'Starting Position',
                        'Number of Moves',
                        'Path','Times Passed Go',
                        'Times in Jail',
                        'Properties',
                        'Chest Cards', 
                        'Chest Card Payout', 
                        'Total Wait',
                        'Chance Card Round 1',
                        'Chance Card Round 2',
                        'Chance Card Round 3',
                        'Chance Card Round 4'])
########################

        output.writerow([''])
        output.writerow(["","game", str(gameCount) ,gameTime, "seconds", quickTiming, "x speed", "randomized time:", randomTime])

        for player in players:
            playerChestCardsID = []
            for i in range(len(player.commChest)):
                playerChestCardsID.append(player.commChest[i][0])
            chanceCardDetails = []
            for detail in player.chanceUsed: chanceCardDetails.append(detail)


########################
#    CHANGE DATA       #
########################
            output.writerow([player.id, 
                            player.type, 
                            player.winner,
                            player.points, 
                            player.money, 
                            player.mGo, 
                            player.mChest, 
                            player.mProp, 
                            player.startingPos, 
                            player.numRoles, 
                            player.path, 
                            player.timesPassedGo, 
                            player.timesJailed, 
                            player.properties,
                            playerChestCardsID, 
                            player.commChestPayout,
                            player.totalWaitTime,
                            chanceCardDetails[0],
                            chanceCardDetails[1],
                            chanceCardDetails[2],
                            chanceCardDetails[3],])
########################

        


        strCount = str(gameCount)
        output.writerow([''])
    # df = pandas.read_csv('output.csv', index_col='ID')
    # df = pandas.read_csv('output.csv')
    # if report: print(df)
    # return df
    details = []
    for player in players:
        details.append([player.id, player.type, player.winner,player.points, player.money, player.mGo, player.mChest, player.mProp, player.startingPos, player.numRoles, player.path, player.timesPassedGo, player.timesJailed, player.properties,playerChestCardsID, player.commChestPayout,player.totalWaitTime])
    return details

def lezgo():
    for i in range(20):
        print("-----------------------------------------------")
        if i == 6: print("------< STARTING >-----------------------------")
        if i == 9: print("----------------< MONOPOLY >-------------------")
        if i == 12: print("--------------------------< SPEED >------------")
    print("")
