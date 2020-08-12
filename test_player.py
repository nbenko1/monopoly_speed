
import unittest
import player
import cards
import board

# all chest cards
# p.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
# p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
# p.commChest.append([3, 1, "partGroup", 2000, 3, pink, orange, green])
# p.commChest.append([4, 1, "set", 4000, 1, red])
# p.commChest.append([5, 1, "set", 4000, 1, green])
# p.commChest.append([6, 1, "set", 4000, 1, yellow])
# p.commChest.append([7, 1, "set", 3000, 1, pink])
# p.commChest.append([8, 1, "set", 3000, 1, orange])
# p.commChest.append([9, 1, "set", 2000, 1, utilities])
# p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
# p.commChest.append([11, 1, "rail", 1000, 4, railroads])

brown = [1,3]
lblue = [5,6,7]
pink = [9,10,11]
orange = [13,14,15]
red = [17,18,19]
yellow = [21,22,23]
green = [25,26,27]
dblue = [29,31]
railroads = [4,12,20,28]
utilities = [2,30]


class TestPlayer(unittest.TestCase):


    def test_findLeastNeededProp(self):

        # test partgroup with extra
        p = player.Player(1)
        p.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p.properties.extend([1,3,9,14,15])
        self.assertEqual(p.findLeastNeededProp(), 9)

        # multiple cards
        p = player.Player(1)
        p.commChest.append([4, 1, "set", 4000, 1, red])
        p.commChest.append([5, 1, "set", 4000, 1, green])
        p.commChest.append([6, 1, "set", 4000, 1, yellow])
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([1,3,9,14,15])
        self.assertEqual(p.findLeastNeededProp(), 9)

        # two full sets - one matching chest
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([17,18,19,9,10,11])
        self.assertEqual(p.findLeastNeededProp(), 17)

        # one full set - both matching card
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([17,18,19,9,10,11])
        self.assertEqual(p.findLeastNeededProp(), 17)

        # no properties
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        self.assertEqual(p.findLeastNeededProp(), -1)

        # anyset - one not
        p = player.Player(1)
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        p.properties.extend([1,3,25,26,27,30])
        self.assertEqual(p.findLeastNeededProp(), 30)

        # anyset - two full
        p = player.Player(1)
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        p.properties.extend([1,3,25,26,27])
        self.assertEqual(p.findLeastNeededProp(), 1)

        # rail - half set
        p = player.Player(1)
        p.commChest.append([11, 1, "rail", 1000, 4, railroads])
        p.properties.extend([4,12])
        self.assertEqual(p.findLeastNeededProp(), 4)

        # rail - half set, one extra
        p = player.Player(1)
        p.commChest.append([11, 1, "rail", 1000, 4, railroads])
        p.properties.extend([4,12,21])
        self.assertEqual(p.findLeastNeededProp(), 21)

        # returns 21
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([21,29,5,6])
        self.assertEqual(p.findLeastNeededProp(), 5)

        # group card vs set
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([5,6,21])
        self.assertEqual(p.findLeastNeededProp(), 5)

        #damn - change order of props
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([29,1,3])
        self.assertEqual(p.findLeastNeededProp(), 29)

        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([3,1,29])
        self.assertEqual(p.findLeastNeededProp(), 3)

    def test_playChance(self):
        # p1.properties.extend([1,2,3,4,5,6,7,9,10,11,12,13,14,18,19,20,21,22,23,25,26,27,28,29,30,31])
    
        # p1 = player.Player(1)
        # p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        # p1.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        # p1.commChest.append([3, 1, "partGroup", 2000, 3, pink, orange, green])
        # p1.commChest.append([4, 1, "set", 4000, 1, red])
        # p1.commChest.append([5, 1, "set", 4000, 1, green])
        # p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        # p1.commChest.append([7, 1, "set", 3000, 1, pink])
        # p1.commChest.append([8, 1, "set", 3000, 1, orange])
        # p1.commChest.append([9, 1, "set", 2000, 1, utilities])
        # p1.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        # p1.commChest.append([11, 1, "rail", 1000, 4, railroads])
        # p1.properties.extend([1,2,3,4,5,6,7,9,10,11,12,13,14,18,19,20,21,22,23,25,26,27,28,29,30,31])
        # p1.chance.append([1, 2, "keep", "take any unowned property"])
        # p1.chance.append([2, 2, "keep", "cancel a chance card that is played against you"])
        # p1.chance.append([3, 3, "keep", "swap any one of your properties with any one of anothers players properties"])
        # p1.chance.append([4, 4, "keep", "steal any one property from another player"])
        # p1.chance.append([5 ,5, "use", "choose any property owned by another player and immediately return it to the board"])
    
        # players = [p1,p2]
        # b = board.Board()
        # for key, value in b.tiles.items(): #loops through dictionary
        #     for place in value:
        #         if place[0] in p1.properties:
        #             place[1] = 1
        #         if place[0] in p2.properties:
        #             place[1] = 2
        # p1.playChance(players, b, False)
        # self.assertEquals(b,)
        # self.assertTrue(in p1.properties)


        # card 1 check-----------------------------------------------------------------------------------------------------------------
        # no props owned
        p1 = player.Player(1)
        p2 = player.Player(2)
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([])
        p1.chance.append([1, 2, "keep", "take any unowned property"])
        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

        p1.playChance(players, b, False)
      
        self.assertEquals(b.getTile(1)[1],1) # board shows player 1 owns 11
        self.assertTrue(1 in p1.properties) # player 1 owns 11

        # card 1 check
        # no props available
        p1 = player.Player(1)
        p2 = player.Player(2)
        p2.properties.extend([1,2,3,4,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,22,23,25,26,27,28,29,30,31])
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([])
        p1.chance.append([1, 2, "keep", "take any unowned property"])
        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
 
        p1.playChance(players, b, False)

        self.assertEquals(b.getTile(1)[1],2) # board shows player 2 still owns 1
        self.assertFalse(1 in p1.properties) # player 1 does not own 1
        self.assertTrue(len(p1.properties) == 0) # player 1 did not recieve any properties


        # card 1 check
        p1 = player.Player(1)
        p2 = player.Player(2)
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([1,3,9,10])
        p1.chance.append([1, 2, "keep", "take any unowned property"])
        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
    
        p1.playChance(players, b, False)

        self.assertEquals(b.getTile(1)[1],1) # board shows player 1 owns 11
        self.assertTrue(11 in p1.properties) # player 1 owns 11


        # card 1 check
        # for chest card - chooses closer to a full set than completing the card
        p1 = player.Player(1)
        p2 = player.Player(2)
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([1,3,5])
        p1.chance.append([1, 2, "keep", "take any unowned property"])
        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

        p1.playChance(players, b, False)

        self.assertEquals(b.getTile(6)[1],1) # board shows player 1 owns 11
        self.assertTrue(6 in p1.properties) # player 1 owns 11

        # card 1 check-
        # multiple players
        p1 = player.Player(1)
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([1,3,5])
        p1.chance.append([1, 2, "keep", "take any unowned property"])

        p2 = player.Player(2)
        p2.properties.extend([4,14,27])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

        p1.playChance(players, b, False)
     
        self.assertEquals(b.getTile(6)[1],1) # board shows player 1 owns 11
        self.assertTrue(6 in p1.properties) # player 1 owns 11

        # card 1 check
        # multiple players - player 2 has most wanted prop
        p1 = player.Player(1)
        p1.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p1.properties.extend([1,3,5])
        p1.chance.append([1, 2, "keep", "take any unowned property"])

        p2 = player.Player(2)
        p2.properties.extend([4,6,14,27])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
        
        p1.playChance(players, b, False)

        self.assertEquals(b.getTile(7)[1],1) # board shows player 1 owns 11
        self.assertTrue(7 in p1.properties) # player 1 owns 11

        # card 1 check
        # commmunity chest set
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([5,6,21])
        p1.chance.append([1, 2, "keep", "take any unowned property"])

        p2 = player.Player(2)
        p2.properties.extend([4,9,14,27])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
     
        p1.playChance(players, b, False)
       
        self.assertEquals(b.getTile(7)[1],1) # board shows player 1 owns 11
        self.assertTrue(7 in p1.properties) # player 1 owns 11

        # card 1 check
        # 2 close sets, one is chest
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([5,6,21,22])
        p1.chance.append([1, 2, "keep", "take any unowned property"])

        p2 = player.Player(2)
        p2.properties.extend([4,9,14,27])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
     
        p1.playChance(players, b, False)
        
        self.assertEquals(b.getTile(22)[1],1) # board shows player 1 owns 22
        self.assertTrue(22 in p1.properties) # player 1 owns 22

        # card 3 check-------------------------------------------------------------------------------------------------------
        # one property each
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([5])
        p1.chance.append([3, 3, "keep", "swap any one of your properties with any one of anothers players properties"])

        p2 = player.Player(2)
        p2.properties.extend([4])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

        p1.playChance(players, b, False)

        self.assertEquals(b.getTile(5)[1],2) # board shows player 2 owns 22
        self.assertEquals(b.getTile(4)[1],1) # board shows player 1 owns 22
        self.assertTrue(4 in p1.properties) # player 1 owns 4
        self.assertTrue(5 in p2.properties) # player 2 owns 5
        self.assertTrue(len(p1.properties) == 1) # player 1 does not own anything else
        self.assertTrue(len(p2.properties) == 1) # player 2 does not either


        #card 3
        # complete set
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([1,5,6])
        p1.chance.append([3, 3, "keep", "swap any one of your properties with any one of anothers players properties"])

        p2 = player.Player(2)
        p2.properties.extend([7,10,11,20])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
        b.print()
        p1.playChance(players, b, False)
        b.print()
        self.assertEquals(b.getTile(7)[1],1) # board shows player 1 owns 7
        self.assertEquals(b.getTile(1)[1],2) # board shows player 2 owns 1
        self.assertTrue(7 in p1.properties) # player 1 owns 4
        self.assertTrue(1 in p2.properties) # player 2 owns 5
        self.assertTrue(len(p1.properties) == 3) # player 1 does not own anything else
        self.assertTrue(len(p2.properties) == 4) # player 2 does not either


        #card 3
        # player 1 does not have have any properties
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([])
        p1.chance.append([3, 3, "keep", "swap any one of your properties with any one of anothers players properties"])

        p2 = player.Player(2)
        p2.properties.extend([7,10,11,20])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
        b.print()
        p1.playChance(players, b, False)
        b.print()
        self.assertEquals(b.getTile(7)[1],2) # board shows player 2 owns 7
        self.assertFalse(7 in p1.properties) # player 1 owns 4
        self.assertTrue(7 in p2.properties) # player 2 owns 5
        self.assertTrue(len(p1.properties) == 0) # player 1 does not own anything else
        self.assertTrue(len(p2.properties) == 4) # player 2 does not either


        #card 4-----------------------------------------------------------------------------------------------------------------
        # takes card to complete set
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.properties.extend([])
        p1.chance.append([4, 4, "keep", "steal any one property from another player"])

        p2 = player.Player(2)
        p2.properties.extend([7,10,11,21])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
        
        self.assertEquals(b.getTile(21)[1],2) # board shows player 2 owns 21
     
        p1.playChance(players, b, False)
  
        self.assertEquals(b.getTile(21)[1],1) # board shows player 1 owns 21
        self.assertFalse(21 in p2.properties) # player 2 does not own 21
        self.assertTrue(21 in p1.properties) # player 1 does
        self.assertTrue(len(p1.properties) == 1) # player 1 does not own anything else
        self.assertTrue(len(p2.properties) == 3) # player 2 does not either

        #card 4
        # basic
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.commChest.append([4, 1, "set", 4000, 1, red])
        p1.properties.extend([1,3])
        p1.chance.append([4, 4, "keep", "steal any one property from another player"])

        p2 = player.Player(2)
        p2.properties.extend([7,10,11,20])

        players = [p1,p2]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2
        
        self.assertEquals(b.getTile(20)[1],2) # board shows player 2 owns 21
        self.assertTrue(len(p2.properties) == 4) # player 2 does not either
   
        p1.playChance(players, b, False)
 
        print(p1.properties)
        self.assertEquals(b.getTile(7)[1],1) # board shows player 1 owns 21
        self.assertFalse(7 in p2.properties) # player 2 does not own 21
        self.assertTrue(7 in p1.properties) # player 1 does
        self.assertTrue(len(p1.properties) == 3) # player 1 does not own anything else
        self.assertTrue(len(p2.properties) == 3) # player 2 does not either

        #card 5---------------------------------------------------------------------------------------------------------------
        # basic
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.commChest.append([4, 1, "set", 4000, 1, red])
        p1.properties.extend([1,3])
        p1.chance.append([5 ,5, "use", "choose any property owned by another player and immediately return it to the board"])

        p2 = player.Player(2)
        p2.properties.extend([7,10,11,20])

        p3 = player.Player(3)
        p3.properties.extend([29,3])

        players = [p1,p2,p3]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

       
        p1.playChance(players, b, False)
        
        print(p1.properties)

        self.assertEquals(len(p3.properties), 2) # make sure that the property was taken
        self.assertEquals(b.getTile(10)[1], 0) # no one owns it on the board
        self.assertEquals(len(p2.properties), 3)

        #card 5
        # no properties to take
        p1 = player.Player(1)
        p1.commChest.append([6, 1, "set", 4000, 1, yellow])
        p1.commChest.append([4, 1, "set", 4000, 1, red])
        p1.properties.extend([1,3])
        p1.chance.append([5 ,5, "use", "choose any property owned by another player and immediately return it to the board"])

        p2 = player.Player(2)
        p2.properties.extend([])
        p2.money = 1000

        p3 = player.Player(3)
        p3.properties.extend([])
        p3.money = 5000

        players = [p1,p2,p3]
        b = board.Board()
        for key, value in b.tiles.items(): #loops through dictionary
            for place in value:
                if place[0] in p1.properties:
                    place[1] = 1
                if place[0] in p2.properties:
                    place[1] = 2

        b.print()
        p1.playChance(players, b, False)
        b.print()
        print(p1.properties)

        self.assertEquals(len(p3.properties), 0) # make sure that the property was taken
        self.assertEquals(b.getTile(29)[1], 0) # no one owns it on the board
        self.assertEquals(len(p2.properties), 0)





if __name__ == '__main__':
    unittest.main()