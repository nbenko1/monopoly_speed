#Strategic

import player
import time
import random
import sys

class StrategicPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "strategic"

    def canPurchase(self, b, report, block, quickTiming, randomTime):


        bought = False

        tile = b.getTile(self.tile)
        for card in self.commChest:
       
            for i in range(5,len(card)):
                propSet = card[i]
         
                if tile[0] in propSet and not bought or self.money >= 2000 and not bought: 
                    tile[1] = self.id

                    bought = True
                   
                   
                   
                    self.money -= 1000
                    self.properties.append(tile[0]) # saves property id to player
                    if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n")
                    break

        block.release()
        # sys.stdout.write("--player " + str(self.id) + " released block " + "\n")
        
        self.wait(0.4,0.6,quickTiming, randomTime) #-------------------------------------------------------------    
        if bought: self.wait(2.0, 2.5, quickTiming, randomTime)#-------------------------------------------------------------