#!/usr/bin/python3
# Sample starter bot by Zac Partridge
# z.partridge@unsw.edu.au
# 06/04/19

#Main Code Written by Sachin Krishnamoorthy from course COMP9414 (z5232031) and Peter Nguyen from course COMP3411 (z5061984)

'''
We used the minmax algorothim as our main heuristic for choosing which move would result in the best chance of victory.
The function is set up such that the base cases of winning, losing, and drawing are defined. An associated score is given to each of these scenarios.
Further cases are made to stop the program iterating to the lowest depth of the tree (as this would cause an overflow). It was found that the 4th level was the max level that could be done for the allowable play time.
If none of these cases were satisfied, the program would recursively examine each potential move that could be made given the board state. From then on it would build an array of node information.
These nodes are stored as structs of the class Node, giving tile score and location. These are placed in an array that resets after each recursion. The best score is determined and returned to the function towards the end of one recursive cycle.
Once all branches at a given depth are explored, the best move is returned, and played.

We are aware that the program could be improved with alpha-beta pruning, but because of our inital decision to iterate through a for loop, building the array of nodes to evaluate beforehand because more difficult. As such due to time constraints, we were unable to implement it.
If we were to redo the design, it would be with alpha-beta pruning in mind earlier on, and thus focus on building more flexible code.
'''

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in

###############################################################################
class Node:
    def __init__(self, location, score):
        self.location = location
        self.score = score

    def __repr__(self):
        return '{location: ' + str(self.location) + ', score:' + str(self.score) + '}'


# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    print(" "+s[board[a][i]]+" "+s[board[a][j]]+" "+s[board[a][k]]+" | " \
             +s[board[b][i]]+" "+s[board[b][j]]+" "+s[board[b][k]]+" | " \
             +s[board[c][i]]+" "+s[board[c][j]]+" "+s[board[c][k]])
###############################################################################
# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()
###############################################################################
def gamewon(board, player):
    
    if (board[1] == player and board[2] == player and board[3] == player):
        return True

    elif (board[4] == player and board[5] == player and board[6] == player):
        return True
  
    elif (board[7] == player and board[8] == player and board[9] == player):
        return True
    
    elif (board[1] == player and board[4] == player and board[7] == player):
        return True

    elif (board[2] == player and board[5] == player and board[8] == player):
        return True

    elif (board[3] == player and board[6] == player and board[9] == player):
        return True

    elif (board[1] == player and board[5] == player and board[9] == player):
        return True

    elif (board[3] == player and board[5] == player and board[7] == player):
        return True

    else:
        return False
###############################################################################
def full_board(board):
    c = 1
    while c <= 9 and board[c] != 0:
        c += 1
    if c == 10:
        return True
    else:
        return False
##############################################################################
# choose a move to play
def play():

    #Minimax function will return best move to make, needs total board, current board, and player
    best_move = minimax(boards,0,curr,1, 0)
    
    #Place move on board
    place(curr, best_move.location, 1)
    
    #Return move on server
    return best_move.location

def minimax(board, previous_location, location, player, level):
    #Base Cases: Check if game is over

    #If our AI wins in the board, return score of -30
    if gamewon(board[previous_location],1):
        return Node(previous_location,-30)

    #If they win in the board, return score of -30
    elif gamewon(board[previous_location],2):
        return Node(previous_location,30)      

    #If board is full, it results in a draw
    elif full_board(board[previous_location]):
        return Node(previous_location,0)

    #Testing so far shows max limit before timeout is 4

    #Set score as 0 if we hit user-set max level
    elif player == 1 and level > 4:
        return Node(previous_location,20)

    elif player == 2 and level > 4:
        return Node(previous_location,-20)

################################################################################
    #List of Nodes that we get from branch
    nodes = []
    for i in range(1, 10):
        #If space is available in board to play
        if board[location][i] == 0:
            
            #Builds board for i value
            board[location][i] = player

            #We will alternate calling the recursve function between the player and opponent, to either maximize or minimize scores based on player perspective
            if player == 1:
                score = minimax(board, location, i, 2, level+1).score
            else:
                score = minimax(board, location, i, 1, level+1).score
            
            #Append node to list of explored nodes 
            nodes.append(Node(i, score))
            
            #Reset Board for next loop iteration
            board[location][i] = 0

    ## Find and return best scores
    #Our player wants the smallest scores (most negative is a win)
    #Their player wants the biggest scores (most postive is a win for them)
    
    #If our AI
    if player == 1:
        best_score = 100000
        for node in nodes:
            if node.score < best_score:
                best_score = node.score
                best_node = node

    #If opponent AI
    else:
        best_score = -100000
        for node in nodes:
            if node.score > best_score:
                best_score = node.score
                best_node = node

    return best_node

################################################################################
# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

################################################################################
# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    global next
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()