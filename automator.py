import game
import pandas
import os
from collections import Counter
"""
inputs(number of players, starting position, length of the game, number of rounds, print statements, player types, (length of buy stages), (length of trade stages))
"""

#------CONTROL PANEL - SETUP GAME HERE--------#

#number of players
numberOfPlayers = 3

#starting position for each player
startPosition = [0,0,0]

#how long the game will go in seconds
gameLength = 20.0

#number of games to play
numberOfRounds = 2

#real time print statements from the game
printStatements = False

#True: separate buying and trading rounds
#False: one long buying round
trading = False

#type of players
playerTypes = ["g","s","c"] #TODO long simulations should shuffle this to avoid quirks

#timing charts
#if False will default to regular game timings
#"trading" must be True for this to come into effect
customTimes = False #if this is true the round timing will be overriden with the following times
buyStage = [3.0,2.0,2.0,1.0]
tradeStage = [4.0,5.0,7.0,7.0]

# buyStage = [3.0,2.0,2.0,1.0]
# tradeStage = [4.0,5.0,7.0,7.0]

#---------------------------------------------#




frames = [] # saves all the data from each game
winnerList = [] # saves a list of the player type of each winner
greedyPath = [] # the total path for all greedy players and rounds
strategicPath = [] # same for strategic
conservativePath = [] #^^^ for cons



for gameNumber in range(1,numberOfRounds+1):

    if customTimes: details = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading, buyStage, tradeStage)
    else: details = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading)
    df = pandas.read_csv('output.csv', index_col='ID') # creates a dataframe by reading the output from the previous game
    frames.append(df)

    # this is per game and is over written each time
    # the variables "details" is a 2d array of all the data for each player like this:
        # details[player number(starting at 0)][data from the list below]

    # so if you wanted the total money from the 2nd player youd do --> "details[1][3]"
    # this is the what I'll use for all the analysis before its put into the csv
    
    '''
    list of indices for 'details'
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
        if details[i][2] == True: # if the player won
            winnerList.append(details[i][1])
        if details[i][1] == 'greedy': # saves the path for the greedy player
            greedyPath.extend(details[i][9])
        if details[i][1] == 'strategic': # for the strategic player
            strategicPath.extend(details[i][9])
        if details[i][1] == 'conservative': # for the conservative player
            conservativePath.extend(details[i][9])



consTotalPath =  Counter(conservativePath) # counts the frequency of each property in the list
greedyTotalPath = Counter(greedyPath)
stratTotalPath = Counter(strategicPath)


# outputs frequency for total path for each type of player
df = pandas.DataFrame.from_dict(greedyTotalPath, orient = 'index').reset_index()
df = df.rename(columns={'index':'greedy player path', 0:'frequency'})
df.to_csv(r'reports\greedy_path.csv')

df = pandas.DataFrame.from_dict(stratTotalPath, orient = 'index').reset_index()
df = df.rename(columns={'index':'strategic player path', 0:'frequency'})
df.to_csv(r'reports\strategic_path.csv')

df = pandas.DataFrame.from_dict(consTotalPath, orient = 'index').reset_index()
df = df.rename(columns={'index':'conservative player path', 0:'frequency'})
df.to_csv(r'reports\conservative_path.csv')



player_result = pandas.concat(frames) #combines all the games details
print(winnerList)
player_result.to_csv(r'reports\players_report.csv')


