import game
import pandas
import os
from collections import Counter

# THIS IS WHERE YOU WANT TO BE #


#------CONTROL PANEL - SETUP GAME HERE--------#

#number of players
numberOfPlayers = 3

#starting position for each player
startPosition = [0,0,0]

#how long the game will go in seconds
gameLength = 45.0

#number of games to play
numberOfRounds = 1

#real time print statements from the game
printStatements = True

#True: separate buying and trading rounds
#False: one long buying round
trading = True

#type of players
playerTypes = ["g","s","c"]

# if == 1.0 then it will play at normal speed
# so == 2 is 2x normal speed, 3 is 3x and so on
timeMultiplier = 3.0

# if True, some randomness will be implemented into the timings
# if False, each action will take the same amount of time each instance
randomTime = True


#if False will default to regular game timings
#"trading" must be True for this to come into effect
customTimes = True #if this is true the round timing will be overriden with the following times

# timing charts
# buyStage = [30.0,30.0,30.0,30.0]
tradeStage = [4.0,4.0,4.0,4.0]  # this is currently ignored - once each card is played the game moves on

#defaults
buyStage = [30.0,20.0,20.0,10.0]
# tradeStage = [40.0,50.0,70.0,70.0] # this is currently ignored - once each card is played the game moves on

#---------------------------------------------#




frames = [] # saves all the data from each game
winnerList = [] # saves a list of the player type of each winner

#tracks path for each player type
greedyPath = []
strategicPath = [] 
conservativePath = []


quickTiming = timeMultiplier # changes the name to avoid confusion - but probably makes it more confusing for everyone else
gameLength = gameLength/quickTiming # speeds up game if indicated
if quickTiming != 1.0:  # this loop speeds up the timing for the trading rounds
    gameLength = round(gameLength/timeMultiplier,2) # adjusts for time drift
    if trading:
        for i in range(len(buyStage)):
            buyStage[i] = buyStage[i]/quickTiming




# runs a game
for gameNumber in range(1,numberOfRounds+1):


    details = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading, quickTiming, randomTime, buyStage, tradeStage)
    df = pandas.read_csv('output.csv', index_col='ID') # creates a dataframe by reading the output from the previous game
    frames.append(df)

    # this is per game and is over written each time
    # the variables "details" is a 2d array of all the data for each player like this:
        # details[player number][data from the list below]  # both zero indexed

    # so if you wanted the total money from the 2nd player youd do --> "details[1][3]"
    # this is the what I'll use for all the analysis before its put into the csv
    
    '''
    list of indices for data in 'details'
    0: ID
    1: player type
    2: winner
    3: total money
    4: money from go
    5: money from properties
    6: money from chance
    7: starting position
    8: number of moves
    9: path
    10: times passed go
    11: times jailed
    12: properties owned
    13: chest cards
    '''

    for i in range(numberOfPlayers):
        if details[i][2] == "Winner" or details[i][2] == "Tie": # if the player won
            winnerList.append(details[i][1])
        if details[i][1] == 'greedy': # saves the path for the greedy player
            greedyPath.extend(details[i][9])
        if details[i][1] == 'strategic': # path for the strategic player
            strategicPath.extend(details[i][9])
        if details[i][1] == 'conservative': # path for the conservative player
            conservativePath.extend(details[i][9])


greedyTotalPath = []
stratTotalPath = []
consTotalPath = []

playerPaths = [greedyPath,strategicPath,conservativePath]
totalPaths= [greedyTotalPath, stratTotalPath, consTotalPath]

for path in totalPaths:
    for prop in range(0,32):
        path.append([prop,0])

for i in range(0,3):
    playerPath = playerPaths[i]
    totalPath = totalPaths[i]
    for playerProp in playerPath:
        countProp = totalPath[playerProp]
        countProp[1] += 1 # increase count of the prop

greedyTotalPath = dict(greedyTotalPath)
stratTotalPath = dict(stratTotalPath)
consTotalPath = dict(consTotalPath)


# outputs frequency for total path for each type of player
df = pandas.DataFrame.from_dict(greedyTotalPath, orient = 'index')
df = df.rename(columns={'index':'greedy player path', 0:'frequency'})
df.to_csv(r'reports\greedy_path.csv')

df = pandas.DataFrame.from_dict(stratTotalPath, orient = 'index')
df = df.rename(columns={'index':'strategic player path', 0:'frequency'})
df.to_csv(r'reports\strategic_path.csv')

df = pandas.DataFrame.from_dict(consTotalPath, orient = 'index')
df = df.rename(columns={'index':'conservative player path', 0:'frequency'})
df.to_csv(r'reports\conservative_path.csv')



player_result = pandas.concat(frames) #combines all the games details
print(winnerList)
player_result.to_csv(r'reports\report.csv')





    #------FOR TIMING TESTING-----------#

    # buyStage = [30.0,20.0,20.0,10.0]
    # tradeStage = [40.0,50.0,70.0,70.0]
    # quickTiming = timeMultiplier
    
    # if gameNumber > 2:
    # randomTime = False

    # for time structure testing
    # if gameNumber % 2== 0:
    #     randomTime = True

    # gameLength = 180
    # if gameNumber <= 2: 
    #     quickTiming = 1.0
    # elif gameNumber >= 3 and gameNumber <= 4:
    #     quickTiming = 2.0
    # elif gameNumber >= 5: 
    #     quickTiming = 4.0
    # if quickTiming != 1.0: 
    #     gameLength = round(gameLength/timeMultiplier,2) # adjusts for time drift
    #     if trading:
    #         for i in range(len(buyStage)):
    #             buyStage[i] = round(buyStage[i]/quickTiming,2)

    # if quickTiming != 1.0: gameLength = round(gameLength/quickTiming,2) # adjusts for time drift

    # print("game", gameNumber, "length", gameLength)

    #-----------------------------------#