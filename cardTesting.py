
import unittest
import player
import cards


class TestCards(unittest.TestCase):
    def testMoney(self):
        chestDeck = cards.CommChestDeck()
        player = player.Player(1)
        player.commChest = chestDeck.pullChestCards()
        player.properties.append(1)
        player.properties.append(28)
        player.properties.append(4)
        player.properties.append(12)
        player.properties.append(20)
        player.properties.append(3)
        chestDeck.payout(player)
        # assertTrue(player.money == )



if __name__ == '__main__':
    unittest.main()