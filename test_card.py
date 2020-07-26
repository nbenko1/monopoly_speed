
import unittest
import player
import cards


class TestCards(unittest.TestCase):

    def setUp(self):
        self.chestDeck = cards.CommChestDeck()
        self.chanceDeck = cards.ChanceDeck()
        self.player1 = player.Player(1)
    
    def tearDown(self):
        pass

    def test_randomCards(self):

        self.player1.commChest = self.chestDeck.pullChestCards()
        self.assertEqual(len(self.player1.commChest), 3)

        for i in range(10):
            self.assertTrue(self.chestDeck.Cards[i][1] > -1) # card cound not netagive
        
    def test_partGroup(self):
        #1
        self.player1.commChest.append(self.chestDeck.Cards[0])
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[0])

        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)

        self.player1.properties = [1]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [3]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [1,3]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [29]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [13,14,19]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        #--------------------------------------------------------
        #2

        self.player1.commChest = [self.chestDeck.Cards[2]]
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[2])

        self.player1.properties = [9]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [10]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [9,10,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [9,10,11,13]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [25]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [26]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [27]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0
        
        self.player1.properties = [25,26,27]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = []
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [17]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [17,17]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0
        
        self.player1.properties = [29,30]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [0,0,0,0,0,100,99999, -1111111]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0     
    
    def test_group(self):

        self.player1.commChest = [self.chestDeck.Cards[1]]
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[1])

        self.player1.properties = [21,29]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [21,22,23,29,31]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [22,29]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [23,31]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [21,29,31]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = []
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [21]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [22]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0
        
        self.player1.properties = [29]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [29,13,28]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [0,0,0,0,0,100,99999, -1111111]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0   

    def test_set(self):
        self.player1.commChest = [self.chestDeck.Cards[3]]
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[3])

        self.player1.properties = [17,18,19]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 4000)
        self.player1.money = 0

        self.player1.properties = [17,18,19,20,21,1]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 4000)
        self.player1.money = 0

        self.player1.properties = [17,18]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [23,31]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = []
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [0,0,0,0,0,100,99999, -1111111]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0   

        # multiple cards
        self.player1.commChest = [self.chestDeck.Cards[3], self.chestDeck.Cards[6]]

        self.player1.properties = [17,18,19,9,10,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 7000)
        self.player1.money = 0 

        self.player1.properties = [17,18,19,9,10]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 4000)
        self.player1.money = 0 

        self.player1.properties = [17,18,9,10,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 3000)
        self.player1.money = 0 

        self.player1.properties = [17,18,9,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0 

    def test_anySet(self):
        self.player1.commChest = [self.chestDeck.Cards[9]]
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[9])

        self.player1.properties = [1,3]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [5,6,7]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [9,10,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [13,14,15]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [17,18,19,21,22,23]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [17,18,19,21,22,23,25,26,27,29,31]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 4000)
        self.player1.money = 0

        self.player1.properties = [2,30]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [4,12,20,28] #railroads
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [1,5,10] 
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [17,18,20]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [0,0,0,0,0,9999999,-100000000000]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

    def test_rail(self):
        self.player1.commChest = [self.chestDeck.Cards[10]]
        self.assertEqual(self.player1.commChest[0],self.chestDeck.Cards[10])
        
        self.player1.properties = [4]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 1000)
        self.player1.money = 0

        self.player1.properties = [4,12]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 2000)
        self.player1.money = 0

        self.player1.properties = [4,12,20]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 3000)
        self.player1.money = 0

        self.player1.properties = [4,12,20,28]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 4000)
        self.player1.money = 0

        self.player1.properties = [1,3]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [5,6,7]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self.player1.money = 0

        self.player1.properties = [9,10,11]
        self.chestDeck.payout(self.player1)
        self.assertEqual(self.player1.money, 0)
        self. player1.money = 0

if __name__ == '__main__':
    unittest.main()