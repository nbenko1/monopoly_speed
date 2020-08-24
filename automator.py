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

#how long the game will go in seconds - only if trading == False
gameLength = 45.0

#number of games to play
numberOfRounds = 2

#real time print statements from the game to the terminal
printStatements = True

#True: separate buying and trading rounds
#False: one long buying round
trading = True

#type of players
playerTypes = ["g","s","c"]

# if == 1.0 then it will play at normal speed
# so == 2 is 2x normal speed, 3 is 3x and so on
# this does not affect the trading round - which will always take a total of 20 seconds per game
timeMultiplier = 3.0

# if True, some randomness will be implemented into the timings
# if False, each action will take the same amount of time each instance
randomTime = True

# timing charts
# buyStage = [30.0,30.0,30.0,30.0]
tradeStage = [5.0,5.0,5.0,5.0] 

#defaults
buyStage = [30.0,20.0,20.0,10.0]
# tradeStage = [40.0,50.0,70.0,70.0] 

#---------------------------------------------#




frames = [] # saves all the data from each game
winnerList = [] # saves a list of the player type of each winner

#tracks path for each player type
greedyPath = []
strategicPath = [] 
conservativePath = []
points = []
for i in range(numberOfPlayers):
    points.append(0)


quickTiming = timeMultiplier # changes the name to avoid confusion - but probably makes it more confusing for everyone else
gameLength = gameLength/quickTiming # speeds up game if indicated
if quickTiming != 1.0:  # this loop speeds up the timing for the trading rounds
    gameLength = round(gameLength/timeMultiplier,2) # adjusts for time drift
    if trading:
        for i in range(len(buyStage)):
            buyStage[i] = buyStage[i]/quickTiming




# runs a game
for gameNumber in range(1,numberOfRounds+1):



    details = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading, quickTiming, randomTime, buyStage, tradeStage, points)
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
    3: Points
    4: total money
    5: money from go
    6: money from chest
    7: money from properties
    8: starting position
    9: number of moves
    10: path
    11: times passed go
    12: times jailed
    13: properties owned
    14: chest cards
    15: chest card payouts
    16: total wait
    '''

    for i in range(numberOfPlayers):
        if details[i][2] == "Winner" or details[i][2] == "Tie": # if the player won
            winnerList.append(details[i][1])
        if details[i][1] == 'greedy': # saves the path for the greedy player
            greedyPath.extend(details[i][10])
        if details[i][1] == 'strategic': # path for the strategic player
            strategicPath.extend(details[i][10])
        if details[i][1] == 'conservative': # path for the conservative player
            conservativePath.extend(details[i][10])

        points[i] = details[i][3] # update master list of points

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