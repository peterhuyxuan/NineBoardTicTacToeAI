# NineBoardTicTacToeAI

To compile and run the Bot against the randomly generated oppossing AI:
1) Open three Terminals (ideally on a Unix system)

2) On the first terminal, compile the bot with the following command:
chmod +x agent.py

3) On the first terminal, run the server with the following command:
./servt -p 12345 (or any 5-digit port number)

4) On the second terminal, run the opposing AI with the following command:
./randt -p 12345 (or any 5-digit port number)

5) On the third terminal, run the bot with the following command:
./agent.py -p 12345 (or any 5-digit port number)
