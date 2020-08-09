#Conservative player


import player
import time
import sys

class ConsPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "conservative"

    def canPurchase(self, b,report,block, quickTiming):
        self.wait(0.2, 0.3, quickTiming)
        # time.sleep(0.2/quickTiming) #-----------------------lag between roles
        pass #tell the