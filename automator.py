import game 
import pandas
"""
inputs(number of players, starting position, length of the game, number of rounds, print statements)
"""

#------CONTROL PANEL - SETUP GAME HERE--------#

#number of players
numberOfPlayers = 2

#starting position for each player
startPosition = [0,0]

#how long the game will go in seconds 
gameLength = 20.0

#number of games to play
numberOfRounds = 1

#real time print statements from the game
printStatements = True

#trading round
trading = True

#type of players
playerTypes = ["g","s"] #TODO long simulations should shuffle this to avoid quirks

#timing charts
#if False will default to regular game timings
customTimes = True #if this is true the round timimg will be overriden with the following times
buyStage = [3.0,2.0,2.0,1.0] 
tradeStage = [4.0,5.0,7.0,7.0]

# buyStage = [3.0,2.0,2.0,1.0] 
# tradeStage = [4.0,5.0,7.0,7.0]

#---------------------------------------------#







# df = game.run(numberOfPlayers, startPosition, gameLength, numberOfRounds, printStatements, playerTypes)

frames = []
winnerList = []
for gameNumber in range(1,numberOfRounds+1):

    if customTimes: df = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading, buyStage, tradeStage)
    else: df = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes, trading)

    frames.append(df)
    for i in range(1,numberOfPlayers+1):
        if df.at[i,'winner?'] == True:
            playerDescription = [i, df.at[i,'player_type']]
            winnerList.append(playerDescription)

result = pandas.concat(frames)
print(winnerList)
result.to_csv(r'C:\Users\Nicholai\Documents\monopoly_speed\monopoly_speed\report.csv')