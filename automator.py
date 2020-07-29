import game 
import pandas
"""
inputs(number of players, starting position, length of the game, number of rounds, print statements)
"""

#------CONTROL PANEL - SETUP GAME HERE--------#

#number of players
numberOfPlayers = 3

#starting position for each player
startPosition = [0,0,0]

#how long the game will go in seconds 
gameLength = 120.0

#number of games to play
numberOfRounds = 5

#real time print statements from the game
printStatements = False

#type of players
playerTypes = ["g","s","c"] #TODO long simulations should shuffle this to avoid quirks

#---------------------------------------------#

# df = game.run(numberOfPlayers, startPosition, gameLength, numberOfRounds, printStatements, playerTypes)

frames = []
winnerList = []
for gameNumber in range(1,numberOfRounds+1):

    df = game.run(numberOfPlayers, startPosition, gameLength, gameNumber, printStatements, playerTypes)

    frames.append(df)
    for i in range(1,numberOfPlayers+1):
        if df.at[i,'winner?'] == True:
            playerDescription = [i, df.at[i,'player_type']]
            winnerList.append(playerDescription)

result = pandas.concat(frames)
print(winnerList)
result.to_csv(r'C:\Users\Nicholai\Documents\monopoly_speed\monopoly_speed\report.csv')