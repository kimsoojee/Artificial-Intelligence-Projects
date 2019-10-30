#===============================================
# CS 440 Programming Assignment 3
#
# Aris Vanderpool, Soo Jee Kim
#
# This Atropos AI game utilizes the minimax function using an evaluator to
# choose the best possible move to make in the game. Most of the functions in
# this file are helper functions that take the input string and do something
# with it; such as reading it or deciding if the current move is a loss or not.
# The evaluator scores the move based off of what nodes are around it. It scores
# based off of whether or not there are empty nodes around it, or if they are
# the same color, or if it is located in a corner or edge.
#===============================================

# Import Statements
import sys
import random

# This takes the input string in.
b = sys.argv[1]

# Red = 1
# Blue = 2
# Green = 3

def ReadBoard(board):
    """ This function takes the input string and turns it into a more
        readable version.
    """
    chnBoard = board.replace("[", "")
    newBoard = chnBoard.replace("LastPlay:", "")
    revBoard = newBoard.split("]")
    fullBoard = list(reversed(revBoard))
    boardList = [list(x) for x in fullBoard[1:]]
    board = [list(map(int,x)) for x in boardList]

    lastPlay = fullBoard[0]
    if lastPlay != 'null':
        splitNum = lastPlay[1:-1].split(",")
        lastPlay = [int(x) for x in splitNum]

    return board, lastPlay

# Initial call to read the input string.
Board, LastPlay = ReadBoard(b)

# This asserts positive infinity and negative infinity. Being this large, they
# will in essence be equivalent to positive and negative infinity.
PosInfinity = 1000
NegInfinity = -1000

def neighbor(board, move):
    """ This function takes the location based off of the row from the bottom
        and finds all of the neighbouring nodes around that node. There is no
        need to write in for a special case where there aren't six nodes, as the
        edges are always filled in from the start as part of the predetermined
        board.
    """
    row = move[1]
    left = move[2]

    TopLeft = int(board[row+1][left-1])
    TopRight = int(board[row+1][left])
    MidLeft = int(board[row][left-1])
    MidRight = int(board[row][left+1])
    
    # If the node we are looking around is located on row 1 (1 row up from the
    # bottom), then we have to have a special case for it since there are less
    # nodes in row 0 in relation to what size it should be.
    if row == 1:
        BotLeft = int(board[row-1][left-1])
        BotRight = int(board[row-1][left])
        
    else:
        BotLeft = int(board[row-1][left])
        BotRight = int(board[row-1][left+1])

    return TopRight, MidRight, BotRight, BotLeft, MidLeft, TopLeft  # Clockwise



def PossibleMoves(board, lastPlay):
    """ Creates a list of strings of all possible moves that it could make next.
    """
    # Initializes a variable that is the size of the board; that means it is the
    # number of rows in the board.
    size = len(board) - 1

    # Initializes a list of strings of possible moves that we can return.
    possibleMoves = []
    randomChoice = []

    # If the board just started, then the previous move was null. This is the
    # base case.
    if(lastPlay == 'null'):
        # You are allowed to make moves to go in any empty spaces on the board
        # if you are moving first.
        for i in range(1,size):
            for j in range(1,len(board[i])-1):
                if board[i][j] == 0:
                    for c in range(1,4):  #R,B,G
                        move = (c, i, j, len(board[i]) - 1 - j)
                        # This is here just to make
                        if not isLoss(board, move):
                            possibleMoves.append(move)

    # For every other case we looks at the last played move and decide which
    # move we can possibly make around the node that we chose.
    else:
        row = int(lastPlay[1])
        left = int(lastPlay[2])

        # Make a call to neighbor function to find the circles around.
        adjCircles = neighbor(board, lastPlay)

        # Only choose empty circles
        if 0 in adjCircles:
            for c in range(1,4): #R, B, G
                if board[row+1][left-1] == 0: # Top left
                    move = (c, row+1, left-1, len(board[row+1]) - 1 - (left-1))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

                if board[row+1][left] == 0: # Top right
                    move = (c, row+1, left, len(board[row+1]) - 1 - (left))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

                if board[row][left-1] == 0: # Mid left
                    move = (c, row, left-1, len(board[row]) - 1 - (left-1))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

                if board[row][left+1] == 0: # Mid right
                    move = (c, row, left+1, len(board[row]) - 1 - (left+1))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

                if row > 1 and board[row-1][left] == 0: # Bottom left
                    move = (c, row-1, left, len(board[row-1]) - 1 - (left))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

                if row > 1 and board[row-1][left+1] == 0: # Bottom right
                    move = (c, row-1, left+1, len(board[row-1]) - 1 - (left+1))
                    randomChoice.append(move)
                    if not isLoss(board, move):
                        possibleMoves.append(move)

        # If the last move made is surrounded and there are no other moves
        # possible we can then move anywhere on the board that we want.
        else:
            for c in range(1,4): #R,B,G
                for i in range(1,size):
                    for j in range(1,len(board[i])-1):
                        if board[i][j] == 0:
                            for c in range(1,4): #R,B,G
                                move = (c, i, j, len(board[i]) - 1 - j)
                                randomChoice.append(move)
                                if not isLoss(board, move):
                                    possibleMoves.append(move)
                                    
        if not possibleMoves:
            if randomChoice:
                possibleMoves = [random.choice(randomChoice)]

    return possibleMoves


def isLoss(board, move):
    """ Checks if given the board the give move will results in a loss or not.
    """
    color = move[0]
    # This variable is what we look for when we look for a loss.
    colorSet = [1,2,3]
    TopRight, MidRight, BotRight, BotLeft, MidLeft, TopLeft = neighbor(board,move)

    #check
    # 1. TopLeft, TopRight
    # 2. TopRight, MidRight
    # 3. MidRight, BotRight
    # 4. BotRight, BotLeft
    # 5. BotLeft, MidLeft
    # 6. MidLeft, TopLeft

    # Orders the various sets into increasing order, looking for a [1, 2, 3]
    # which would result in a loss.
    check1 = sorted([TopLeft, TopRight, color])
    check2 = sorted([TopRight, MidRight, color])
    check3 = sorted([MidRight, BotRight, color])
    check4 = sorted([BotRight, BotLeft, color])
    check5 = sorted([BotLeft, MidLeft, color])
    check6 = sorted([MidLeft, TopLeft, color])
    Check = [check1, check2, check3, check4, check5, check6]

    # If the set [1, 2, 3] exists in the set, then it is a loss. 
    if colorSet in Check:
        return True

    # Otherwise it is not a loss, therefore false.
    return False


def evaluator(board, move):
    """ This is the evaluator function that decides whether or not the current
        position where the given move would be on the given board is good or not.
        It scores the given move. We tested based on trial and error what scores
        to assign to the values, and whether or not they would be positive or
        negative values. 
    """
    # If the given move is a loss by default it is assigned the lowest score possible.
    if isLoss(board,move):
        return NegInfinity

    # Score by default is zero.
    score = 0
    
    color, row, left = move[0], move[1], move[2]
    right = len(board[row]) - 1 - left
    R, B, G = 1, 2, 3
    neighborColor = neighbor(board,move)


    if row == 1 and color != G:     # Bottom boundary is not Green -> get score
        score += 2
        if left == 1 and color != B:    # Bottom left corner is not Blue -> get score
            score += 2
        elif right == 1 and color != R:   # Bottom right corner is not Red -> get score
            score += 2
    if left == 1 and color != B:    # Left boundary is not blue -> get score
        score += 2
    if right == 1 and color != R:   # Right boundary is not red -> get score
        score += 2

    # Both positive and negative scores were tested for this section. We ended
    # up deciding on these values from the tests that were conducted. However
    # the results were also random so the score values may not have any good
    # reason why they were chosen or not behind them. So the current scoring
    # system is not necessarily optimal.
    for i, c in enumerate(neighborColor):
        # 1. If it has colored neighbors -> Get score
        if c != 0:
            score += 3
            # 2. If it has thesame colored neighbors with move itself -> Get score
            if c == color:
                score += 5
            # 3. If it has different colored neighbor pairs -> Get score
            checkPair = neighborColor[(i+1) % len(neighborColor)]
            if c != checkPair:
                score += 2

    return score


def minimax(board, lastPlay, depth, alpha, beta, Max):
    """ The minimax function takes the board, the last play and does recursive
        calls on itself as many times as depth is.
    """
    # Calls all of the possible moves that can be made.
    node = PossibleMoves(board, lastPlay)
    
    # If it is the first move we randomly choose a node to play.
    if lastPlay == 'null':
        return (0, random.choice(node))

    # Checks the edge case if depth is 0 or if it is a loss and returns that so
    # the earlier recursive make sure not to choose a loss.
    if depth == 0 or isLoss(board, lastPlay):
        score = evaluator(board, lastPlay)
        return (score, lastPlay)

    # This is the alpha segment of alpha-beta pruning. That means it looks at
    # the maximum of the lower bound of possible solutions. This chooses based
    # off of what the player wants to choose.
    elif Max:
        bestValue = (alpha, [])
        for move in node:
            color, row, left = move[0], move[1], move[2]
            board[row][left] = color
            nodeValue = minimax(board, move, depth-1, bestValue[0], beta, False)
            board[row][left] = 0
            if bestValue[0] < nodeValue[0]:
                bestValue = (nodeValue[0], move)
            if bestValue[0] == nodeValue[0] and not bestValue[1]:
                bestValue = (nodeValue[0], move)
            if beta <= bestValue[0]:
                break
    # The beta segment of alpha-beta pruning. This chooses based off of what the
    # opponent would want to choose for the player.
    else:
        bestValue = (beta, [])
        for move in node:
            color, row, left = move[0], move[1], move[2]
            board[row][left] = color
            nodeValue = minimax(board, move, depth-1, alpha, bestValue[0], True)
            board[row][left] = 0
            if bestValue[0] < nodeValue[0]:
                bestValue = (nodeValue[0], move)
            if bestValue[0] == nodeValue[0] and not bestValue[1]:
                bestValue = (nodeValue[0], move)
            if alpha >= bestValue[0]:
                break

    return bestValue

# This is the initial call of the minimax function. We used the value of ten
# for the depth. Too large of a depth/lookahead makes it slow and not necessarily
# better, since there are paths that can lead to a max amount in the score within
# a depth of ten. 
bestValue = minimax(Board, LastPlay, 10, NegInfinity, PosInfinity, True)
bestMove = str(bestValue[1])


# Print to stdout for AtroposGame
sys.stdout.write(bestMove);

