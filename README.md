# NineBoardTicTacToeAI

This project is an agent that plays the game of Nine-Board Tic-Tac-Toe. 

This game is played on a 3 x 3 array of 3 x 3 Tic-Tac-Toe boards. The first move is made by placing an X in a randomly chosen cell of a randomly chosen board. After that, the two players take turns placing an O or X alternately into an empty cell of the board corresponding to the cell of the previous move. (For example, if the previous move was into the upper right corner of a board, the next move must be made into the upper right board.)

The game is won by getting three-in-a row either horizontally, vertically or diagonally in one of the nine boards. If a player is unable to make their move (because the relevant board is already full) the game ends in a draw.

To compile and run the bot against the randomly generated opposing AI:
1) Open three Terminals (ideally on a Unix system)

2) On the first terminal, compile the bot with the following command:
chmod +x agent.py

3) On the first terminal, run the server with the following command:
./servt -p 12345 (or any 5-digit port number)

4) On the second terminal, run the opposing AI with the following command:
./randt -p 12345 (or any 5-digit port number)

5) On the third terminal, run the bot with the following command:
./agent.py -p 12345 (or any 5-digit port number)

6) Observe the results of the game on the first terminal

7) Repeat Step 2-6 with a different 5-digit port number to play again
