import game
import player as p
import unittest
import cards

class TestGame(unittest.TestCase):
    



    def setUp(self):
        self.brown = [1,3]
        self.lblue = [5,6,7]
        self.pink = [9,10,11]
        self.orange = [13,14,15]
        self.red = [17,18,19]
        self.yellow = [21,22,23]
        self.green = [25,26,27]
        self.dblue = [29,31]
        self.railroads = [4,12,20,28]
        self.utilities = [2,30]

        self.players = []
        numPlayers = 4
        for i in range(numPlayers):
            tempPlayer = p.Player(i)
            self.players.append(tempPlayer)
        
        self.chest = cards.CommChestDeck()
        self.chance = cards.ChanceDeck()

    def test_gameSetup(self):
        
        for player in self.players:
            self.assertEqual(player.money, 0)
            self.assertEqual(len(player.chance), 0)
            self.assertEqual(len(player.commChest), 0)

        game.gameSetup(self.players)

        for player in self.players:
            self.assertEqual(player.money, 5000)
            self.assertEqual(len(player.chance), 4)
            self.assertEqual(len(player.commChest), 3)


    def test_payout(self):


        players = []
        tempPlayer = p.Player(1)
        players.append(tempPlayer)

        for player in players:
            self.assertFalse(player.winner)
            self.assertEqual(player.mChest, 0)
            self.assertEqual(player.mProp,0)

        tempPlayer.commChest.append(self.chest.Cards[3]) #three card set
        self.assertEquals(tempPlayer.commChest[0],[4, 1, "set", 4000, 1, self.red])
        tempPlayer.properties.append(17)
        tempPlayer.properties.append(18)
        tempPlayer.properties.append(19)
        game.payout(players)
        self.assertTrue(tempPlayer.winner)
        self.assertEqual(tempPlayer.mChest, 4000)
        self.assertEqual(tempPlayer.mProp, 6000)

        tempPlayer = p.Player(1)
        players = [tempPlayer]

        tempPlayer.commChest.append(self.chest.Cards[0]) #group set
        self.assertEquals(tempPlayer.commChest[0],[1, 1, "partGroup", 2000, 3, self.brown, self.lblue, self.dblue])
        tempPlayer.properties.append(1)
        tempPlayer.properties.append(6)
        tempPlayer.properties.append(31)
        game.payout(players)
        self.assertTrue(tempPlayer.winner)
        self.assertEqual(tempPlayer.mChest, 2000)
        self.assertEqual(tempPlayer.mProp, 3000)
        self.assertEqual(tempPlayer.money, 5000)

        tempPlayer = p.Player(1)
        players = [tempPlayer]     

        tempPlayer.commChest.append(self.chest.Cards[9])
        tempPlayer.commChest.append(self.chest.Cards[10])
        self.assertEquals(tempPlayer.commChest[0],[10, 2, "anySet", 1000, 10, self.brown, self.lblue, self.pink, self.orange, self.red, self.yellow, self.green, self.dblue, self.utilities])
        tempPlayer.properties.append(17)
        tempPlayer.properties.append(18)
        tempPlayer.properties.append(19)
        tempPlayer.properties.append(29)
        tempPlayer.properties.append(3)
        tempPlayer.properties.append(2)
        tempPlayer.properties.append(20)
        game.payout(players)
        self.assertTrue(tempPlayer.winner)
        self.assertEqual(tempPlayer.mChest, 2000) #one set + railroad
        self.assertEqual(tempPlayer.mProp, 10000)





        # tempPlayer = p.Player(2)
        # players.append(tempPlayer)
        # for player in players:
        #     self.assertTrue(player.winner)
        #     self.assertEqual(player.mChest, 4000)
        #     self.assertEqual(player.mProp, 6000)


if __name__ == '__main__':
    unittest.main()