# this keeps track of the game state, calls update methods and maintains board
# will this be a class?

import player
import board

import random
 
# add multithreading
# differintiate between player types  -> superclass?
# how to control timing - player class has 'wait' commands
# board is a global variable
    #info per tile = [id, players on spot, owner]

b = board.Board()

# print(b.tiles["brown"][0])

# b.tiles["brown"][0][0] = 6

# print(b.tiles.get("brown")[0])

place = b.position(3)
print(place)
place[2] = 4
print(place)

def main():
    playerOne = player.Player(1)
    
    rounds = 3
    for _ in range(0,rounds):
        role = random.randint(1,6)
        playerOne.move(role)
        print(playerOne.tile)
    print(board)

# main()
