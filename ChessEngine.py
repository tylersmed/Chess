"""
Stores all the information about the current state of the game, is responsible for for 
determining valid moves at the current state of the game, and keeps a move log.
"""

class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.white_to_move = True
        self.move_log = []

    #does not work for castling, pawn promotion, and en passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        if (move.endRow == 0 or move.endRow == 7) and self.board[move.endRow][move.endCol][1] == 'P':
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
            # handles pawn promotion
        self.move_log.append(move) #log moves to undo later/ display history
        self.white_to_move = not self.white_to_move # swap players

    def undoMove(self):
        if len(self.move_log) != 0: #there must be a move to undo
            move = self.move_log.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.white_to_move = not self.white_to_move

    # Legal moves while considering check
    def getValidMoves(self, r=-1, c=-1):
        allMoves = []
        if r == -1:
            allMoves = self.getAllPossibleMoves()
        else:
            piece = self.board[r][c][1]
            allMoves = self.moveFunctions[piece](r, c, allMoves)
            return allMoves

    # Legal moves without considering check
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):                
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.white_to_move:
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': # there's and enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        if not self.white_to_move:
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': # there's and enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

        return moves

    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        for d in directions: # for loop runs the while loop 4 times, in every possible dir the rook can move
            dist = 1
            while abs(r+dist*d[0]) <= 7 and abs(r+dist*d[0] >= 0 and
                abs(c+dist*d[1]) <= 7 and abs(c+dist*d[1]) >= 0): # keep the movement within the board dimensions
                sq = self.board[r+d[0]*dist][c+d[1]*dist]
                if sq[0] == '-':
                    moves.append(Move((r, c), (r+d[0]*dist, c+d[1]*dist), self.board))
                    dist += 1
                elif (sq[0] == 'b' and self.white_to_move) or (sq[0] == 'w' and not self.white_to_move):
                    moves.append(Move((r, c), (r+d[0]*dist, c+d[1]*dist), self.board))
                    break
                else:
                    break

        return moves

    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), 
                        (1, 2), (-1, 2), (1, -2), (-1, -2)] # every possible move from current square for a knight in +row, +col
        for d in directions:
            if abs(r+d[0]) <= 7 and abs(r+d[0]) >= 0 and abs(c+d[1] <= 7 and abs(c+d[1] >= 0)): # check move is on the board
                sq = self.board[r+d[0]][c+d[1]]
                if sq[0] == '-':
                    moves.append(Move((r, c), (r+d[0], c+d[1]), self.board)) # move to blank space
                elif (sq[0] == 'b' and self.white_to_move) or (sq[0] == 'w' and not self.white_to_move):
                    moves.append(Move((r, c), (r+d[0], c+d[1]), self.board)) # capture enemy piece

        return moves

    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # all the possible directions to move in +row and +col
        for d in directions:
            dist = 1
            while abs(r+dist*d[0]) <= 7 and abs(r+dist*d[0] >= 0 and
                abs(c+dist*d[1]) <= 7 and abs(c+dist*d[1]) >= 0): # keep the movement within the board dimensions
                sq = self.board[r+d[0]*dist][c+d[1]*dist]
                if sq[0] == '-':
                    moves.append(Move((r, c), (r+d[0]*dist, c+d[1]*dist), self.board))
                    dist += 1
                elif (sq[0] == 'b' and self.white_to_move) or (sq[0] == 'w' and not self.white_to_move):
                    moves.append(Move((r, c), (r+d[0]*dist, c+d[1]*dist), self.board))
                    break
                else:
                    break
        
        return moves

    def getKingMoves(self, r, c, moves):
        directions = [(1,-1), (1, 0), (1, 1), (0, -1), (0, 1),
                      (-1, -1), (-1, 0), (-1, 1)] # possible directions to move in +row +col
        for d in directions:
            if abs(r+d[0]) <= 7 and abs(r+d[0]) >= 0 and abs(c+d[1] <= 7 and abs(c+d[1] >= 0)): # check move is on the board
                sq = self.board[r+d[0]][c+d[1]]
                if sq[0] == '-':
                    moves.append(Move((r, c), (r+d[0], c+d[1]), self.board)) # move to blank space
                elif (sq[0] == 'b' and self.white_to_move) or (sq[0] == 'w' and not self.white_to_move):
                    moves.append(Move((r, c), (r+d[0], c+d[1]), self.board)) # capture enemy piece

        return moves

    def getQueenMoves(self, r, c, moves):
        # a queen can move in all directions a rook and bishop can move
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        return moves

class Move():
    # map keys to values
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow, self.startCol = startSq
        self.endRow, self.endCol = endSq
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #give every move a unique ID so they can be compared
        self.moveId = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]