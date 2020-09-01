Monopoly Speed Simulator
======
**Monopoly Speed** is a version of Monopoly where instead of taking turns, and all players move around the board and buy properties at the same time, relying on a timer to swap between buying properties, and trading with other players. This software was built to allow the user to set up custom simulations in order to test play styles and tactics in order to study the effect of different configurations on outcomes.

This is a research project under the math department of Southwestern University

## Set Up

To run the simulator, go into the run_game.py file and configure a simulation using the variables at the top of the file.
Once the simulation is complete, it will create a number of CSV files that report all the details of the games that were played. And if you want to watch it work, you can enable real-time print statements that explain whats happening in the game.

## File Descriptions:

**run_game.py** Dashboard to configure and run simulations  <--- this is what you want to look at <3

**game.py** This file handles the actual gameplay, creating player threads that all interact with a shared board object

**cards.py** Classes for the chance, and community chest card decks

**board.py** Board class that stores property ownership data

**player.py** Default player class that handles how the player interacts with the board and saves all related information

**conPlayer.py** A player agent that moves around the board collecting money from GO without buying any properties

**strategicPlayer.py** A player agent that makes slighly more complex decisions on which properties to buy

