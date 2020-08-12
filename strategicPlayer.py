#Strategic

import player
import time
import random
import sys

class StrategicPlayer(player.Player):

    def __init__(self, player_id):
        super().__init__(player_id)
        self.type = "strategic"

    def canPurchase(self, b,report, block, quickTiming):

        time.sleep(round(0.5/quickTiming,1))#---------------------------------------check cards for property



        tile = b.getTile(self.tile)
        for card in self.commChest:
       
            for i in range(5,len(card)):
                propSet = card[i]
         
                if tile[0] in propSet or self.money >= 2000: 
                    tile[1] = self.id
     
                   
                    self.wait(2.0, 2.5, quickTiming)
                    # time.sleep(random.randint(2,3)/quickTiming)#--------------------------buys property
                    # time.sleep(random.uniform(2.0,2.5)/quickTiming)#--------------------------buys property
                   
                    self.money -= 1000
                    self.properties.append(tile[0]) # saves property id to player
                    if report: sys.stdout.write("player " + str(self.id) + " bought " + str(self.tile)  + "\n")
                    return
