import game 
"""
inputs(number of players, starting position, length of the game, number of rounds, print statements)
"""

#------CONTROL PANEL - SETUP GAME HERE--------#

#number of players
numberOfPlayers = 3

#starting position for each player
startPosition = [0,0,0]

#how long the game will go
gameLength = 100.0

#number of games to player
numberOfRounds = 1

#real time print statements from the game
printStatements = True

#type of player
playerTypes = ["g","g","c"]


report = game.run(numberOfPlayers, startPosition, gameLength, numberOfRounds, printStatements, playerTypes)



