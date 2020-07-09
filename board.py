
class Board:
    def __init__(self):
        self.tiles = {

        #          0                  1                2          3
        # [ Place on board | Owner? (ID of player) | Owner | Frequency p2 ]
        "brown"     : [[ 1, 0, 0, 0], [ 3, 0, 0, 0]],
        "lblue"     : [[ 6, 0, 0, 0], [ 8, 0, 0, 0], [ 9, 0, 0, 0]],
        "pink"      : [[11, 0, 0, 0], [13, 0, 0, 0], [14, 0, 0, 0]],
        "orange"    : [[16, 0, 0, 0], [18, 0, 0, 0], [19, 0, 0, 0]],
        "red"       : [[21, 0, 0, 0], [23, 0, 0, 0], [24, 0, 0, 0]],
        "yellow"    : [[26, 0, 0, 0], [27, 0, 0, 0], [29, 0, 0, 0]],
        "green"     : [[31, 0, 0, 0], [32, 0, 0, 0], [34, 0, 0, 0]],
        "dblue"     : [[37, 0, 0, 0], [39, 0, 0, 0]],
   
        "railroad"  : [[ 5, 0, 0, 0], [15, 0, 0, 0], [25, 0, 0, 0], [35, 0, 0, 0]],
        "utilities" : [[12, 0, 0, 0], [28, 0, 0, 0]],
   
        #          0               1              2
        # [ Place on board | Freqeuncy p1 | Frequency p2 ]
        "GO"           : [[0, 0, 0]],
        "tax"          : [[4, 0, 0], [38, 0, 0]],
        "free parking" : [[20, 0, 0]],
   
        "jail"         : [[10, 0, 0]],
        "go to jail"   : [[30, 0, 0]],
        "chance"       : [[7, 0, 0], [22, 0, 0], [36, 0, 0]],
        "chest"        : [[2, 0, 0], [17, 0, 0], [33, 0, 0]]
        }
        self.exclude = [0, 4, 10, 30, 38, 20, 7, 22, 36, 2, 17, 33]

    # isolates the tile where that was landed on
    def landed(self, id):
        for key, value in self.tiles.items():
            for place in value:
                if id == place[0]:
                    place[1] += 1 # person is on tile

    def position(self, id):
        for key, value in self.tiles.items():
            for place in value:
                if id == place[0]:
                    #place[1] += 1 # person is on tile
                    return place
        return


# board = {
#     1: ('Brown', 0),
#     3: ('Brown', 1),
#     6: ('Cyan', 0),
#     8: ('Cyan', 1),
#     9: ('Cyan', 2),
#     11: ('Pink', 0),
#     13: ('Pink', 1),
#     14: ('Pink', 2),
#     16: ('Orange', 0),
#     18: ('Orange', 1),
#     19: ('Orange', 2),
#     21: ('Red', 0),
#     23: ('Red', 1),
#     24: ('Red', 2),
#     26: ('Yellow', 0),
#     27: ('Yellow', 1),
#     29: ('Yellow', 2),
#     31: ('Green', 0),
#     32: ('Green', 1),
#     34: ('Green', 2),
#     37: ('Blue', 0),
#     39: ('Blue', 1),
# }

# places = {
#     'Brown': [0, 0],
#     'Cyan': [0, 0, 0],
#     'Pink': [0, 0, 0],
#     'Orange': [0, 0, 0],
#     'Red': [0, 0, 0],
#     'Yellow': [0, 0, 0],
#     'Green': [0, 0, 0],
#     'Blue': [0, 0, 0]
# }

