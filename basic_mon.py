# Monopoly Simulator
# http://img.thesun.co.uk/aidemitlum/archive/01771/Monopoly2_1771742a.jpg

from random import randint

board = {
    1: ('Brown', 0),
    3: ('Brown', 1),
    6: ('Cyan', 0),
    8: ('Cyan', 1),
    9: ('Cyan', 2),
    11: ('Pink', 0),
    13: ('Pink', 1),
    14: ('Pink', 2),
    16: ('Orange', 0),
    18: ('Orange', 1),
    19: ('Orange', 2),
    21: ('Red', 0),
    23: ('Red', 1),
    24: ('Red', 2),
    26: ('Yellow', 0),
    27: ('Yellow', 1),
    29: ('Yellow', 2),
    31: ('Green', 0),
    32: ('Green', 1),
    34: ('Green', 2),
    37: ('Blue', 0),
    39: ('Blue', 1),
}

places = {
    'Brown': [0, 0],
    'Cyan': [0, 0, 0],
    'Pink': [0, 0, 0],
    'Orange': [0, 0, 0],
    'Red': [0, 0, 0],
    'Yellow': [0, 0, 0],
    'Green': [0, 0, 0],
    'Blue': [0, 0, 0]
}

piece = 0
jail = 0
iteration = 0

num = input("How many rolls do you want to simulate? ")
num = int(float(num))
for h in range(num):
    piece += randint(1, 6) + randint(1, 6)

    if piece > 40:
        piece -= 40
        iteration += 1

    if piece == 30:
        piece = 10
        jail += 1

    house_set, place = board.get(piece, (None, None))
    if house_set is not None:
        places[house_set][place] += 1

totals = {place: sum(house_set) for place, house_set in places.items()}

for place, amount in totals.items():
    print('{} = {}'.format(place, amount))

for place, house_set in places.items():
    for i, amount in enumerate(house_set, 1):
        print('{} {} = {}'.format(place, i, amount))

print("You've been jailed %d times" %(jail))

digit = len(str(max(amount for house_set in places.values() for amount in house_set)))
blank = "-" * digit
space = " " * digit
place_format = '{{:0>{}}}'.format(digit)

formatted = {
    place: [place_format.format(amount) for amount in house_set]
    for place, house_set in places.items()
}

board_line = []
for index in range(40):
    place = board.get(index, None)
    if place is None:
        value = blank
    else:
        value = places[place[0]][place[1]]
    board_line.append(value)
board_line[0] = 'Go'

board = [[space] * 11 for _ in range(11)]
for index in range(40):
    x, y = 0, 0
    if index < 11:
        x = 10 - index
        y = 10
    elif index < 21:
        x = 0
        y = 10 - (index - 10)
    elif index < 31:
        x = index - 20
    else:
        x = 10
        y = index - 30
    board[y][x] = board_line[index]

for line in board:
    print('  {}  '.format('  |  '.join(str(p) for p in line)))