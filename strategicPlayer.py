#Strategic

import player
import time
import random
import sys

class StrategicPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "strategic"

    def canPurchase(self, b,report, block):

        time.sleep(2)#---------------------------------------check cards for property

        block.acquire()
        tile = b.getTile(self.tile)
        for card in self.commChest:
            for i in range(5,5+card[4]):
                propSet = card[i]
                if tile[0] in propSet or self.money >= 2000: 
                    tile[1] = self.id
                    block.release()
                    time.sleep(random.randint(2,3))#--------------------------------------- get property
                    self.money -= 1000
                    self.properties.append(tile[0]) # saves property id to player
                    if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n")
                return
        block.release()