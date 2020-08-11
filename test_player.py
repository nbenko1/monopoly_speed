
import unittest
import player
import cards

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


    def test_findLeastNeededCard(self):

        # test partgroup with extra
        p = player.Player(1)
        p.commChest.append([1, 1, "partGroup", 2000, 3, brown, lblue, dblue])
        p.properties.extend([1,3,9,14,15])
        self.assertEqual(p.findLeastNeededCard(), 9)

        # multiple cards
        p = player.Player(1)
        p.commChest.append([4, 1, "set", 4000, 1, red])
        p.commChest.append([5, 1, "set", 4000, 1, green])
        p.commChest.append([6, 1, "set", 4000, 1, yellow])
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([1,3,9,14,15])
        self.assertEqual(p.findLeastNeededCard(), 9)

        # two full sets - one matching chest
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([17,18,19,9,10,11])
        self.assertEqual(p.findLeastNeededCard(), 17)

        # one full set - both matching card
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.properties.extend([17,18,19,9,10,11])
        self.assertEqual(p.findLeastNeededCard(), 17)

        # no properties
        p = player.Player(1)
        p.commChest.append([7, 1, "set", 3000, 1, pink])
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        self.assertEqual(p.findLeastNeededCard(), -1)

        # anyset - one not
        p = player.Player(1)
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        p.properties.extend([1,3,25,26,27,30])
        self.assertEqual(p.findLeastNeededCard(), 30)

        # anyset - two full
        p = player.Player(1)
        p.commChest.append([10, 2, "anySet", 1000, 9, brown, lblue, pink, orange, red, yellow, green, dblue, utilities])
        p.properties.extend([1,3,25,26,27])
        self.assertEqual(p.findLeastNeededCard(), 1)

        # rail - half set
        p = player.Player(1)
        p.commChest.append([11, 1, "rail", 1000, 4, railroads])
        p.properties.extend([4,12])
        self.assertEqual(p.findLeastNeededCard(), 4)

        # rail - half set, one extra
        p = player.Player(1)
        p.commChest.append([11, 1, "rail", 1000, 4, railroads])
        p.properties.extend([4,12,21])
        self.assertEqual(p.findLeastNeededCard(), 21)

        # returns 21
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([21,29,5,6])
        self.assertEqual(p.findLeastNeededCard(), 5)

        # group card vs set
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([5,6,21])
        self.assertEqual(p.findLeastNeededCard(), 5)

        #damn - change order of props
        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([29,1,3])
        self.assertEqual(p.findLeastNeededCard(), 29)

        p = player.Player(1)
        p.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        p.properties.extend([3,1,29])
        self.assertEqual(p.findLeastNeededCard(), 3)

    def test_findWantedProperty(self):
        # p1 = Player(1)
        # p1.commChest.append([8, 1, "set", 3000, 1, orange])
        # p1.commChest.append([2, 1, "group", 2000, 2, yellow, dblue])
        # # p1.properties.extend([1,3,5,7,13,14,15])
        # p1.properties.extend([1,2,3,4,5,6,7,9,10,11,12,13,14,18,19,20,21,22,23,25,26,27,28,29,30,31])
        # p1.chance.append([1, 2, "keep", "take any unowned property"])

        # p2 = Player(2)
        # p2.commChest.append([4, 1, "set", 4000, 1, red])
        # p2.properties.extend([6,17,21])
        # p2.chance.append([1, 2, "keep", "take any unowned property"])
        # players = [p1,p2]




        # b = board.Board()

        # for key, value in b.tiles.items(): #loops through dictionary
        #     for place in value:
        #         if place[0] in p1.properties:
        #             place[1] = 1
        #         if place[0] in p2.properties:
        #             place[1] = 2

        # b.print()

        # p1.playChance(players, b, False)


if __name__ == '__main__':
    unittest.main()