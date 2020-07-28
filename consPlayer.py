#Conservative player


import player
import time

class ConsPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "conservative"

    def canPurchase(self, b):
        time.sleep(2)
        pass #tell the