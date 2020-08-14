#Conservative player


import player
import time
import sys

class ConsPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "conservative"

    def canPurchase(self, b, report, block, quickTiming, randomTime):
        block.release()
        # sys.stdout.write("--player " + str(self.id) + " released block " + "\n")
        self.wait(0.3, 0.6, quickTiming,randomTime) #---------------------------------------------------------------
