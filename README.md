Monopoly Speed Simulator
======
**Monopoly Speed** is a version of Monopoly built around a timer, where there are no turns and all players move at the same time relying on a timer to swap between buying properties, and trading with other players. This software allows the user to set up custom simulations in order to test play styles and tactics.

This is a research project under the math department of Southwestern University

## Set Up

To run the simulator, go into the run_game.py file and configure a game using the variables at the top of the file.

## File Descriptions:

**run_game.py** Dashboard to configure and run simulations

**game.py** This file handles the actual gameplay, creating player threads and playing on a shared board object

**cards.py** Classes for the chance, and community chest card decks

**board.py** board class that stores property ownership data

**player.py** default player class that handles how the player interacted with the board and saves all related information

**conPlayer.py** player that only moves around the board without buying any properties

**strategicPlayer.py** player makes slighly more complex decisions on which properties to buy

