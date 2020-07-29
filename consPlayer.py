#Conservative player


import player
import time
import sys

class ConsPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "conservative"

    def canPurchase(self, b,report,block):
        time.sleep(0.5) #-----------------------lag between roles
        pass #tell the