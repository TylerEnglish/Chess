"""
Store data
Responsablities:
1. Store info about current state
2. determine valid moves
3. move log
"""

from unittest.result import failfast


class GameState():
    def __init__(self):
        '''
        Board 8x8 2d list
        each element have 2 char
        1st char represents color
        2nd char represents type
        string "--" represents empty
        '''

        #numpy arrays might be faster
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)

        
        self.checkMate = False
        self.staleMate = False

    """
    takes a move as a param and excutes it
    wont work:
    1. Castling
    2. Promotion
    3. En-passant
    """
    def makeMove(self, move):
        self.board[move.start_r][move.start_c] = "--"
        self.board[move.end_r][move.end_c] = move.piece_m
        self.moveLog.append(move) #maybe to undo and see history
        self.whiteToMove = not self.whiteToMove #swap player
        #update king location
        if move.piece_m == 'wK':
            self.whiteKingLocation = (move.end_r, move.end_c)
        if move.piece_m == 'bK':
            self.blackKingLocation = (move.end_r, move.end_c)

    def undoMove(self):
        """
        Undo last move
        """
        if len(self.moveLog) != 0: #make sure that there is a move
            move = self.moveLog.pop()
            self.board[move.start_r][move.start_c] = move.piece_m
            self.board[move.end_r][move.end_c] = move.piece_cap
            self.whiteToMove = not self.whiteToMove #swap player
            #update king location
            if move.piece_m == 'wK':
                self.whiteKingLocation = (move.start_r, move.start_c)
            if move.piece_m == 'bK':
                self.blackKingLocation = (move.start_r, move.start_c)


    """
    func 1
    All moves considering checks

    func 2
    All moves without considering checks
    """
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            oppMoves = self.getAllPossibleMoves()
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    def inCheck(self): #see if player underattack
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r, c):#determine if enemy can attack square
        self.whiteToMove = not self.whiteToMove #look at oppents move
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch back
        for move in oppMoves:
            if move.end_r == r and move.end_c == c: #square under attack
                return True
        return False
 
    def getAllPossibleMoves(self):
        moves = [Move((6,4),(4,4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    #call correct move function
                    self.moveFunctions[piece](r,c,moves)
        
        return moves

    """
    start logic for pieces
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawns
            if self.board[r-1][c] == "--": #1 SQ pawn adv
                moves.append(Move((r, c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 SQ pawn adv
                    moves.append(Move((r,c), (r-2,c), self.board))

            if c-1 >= 0: #Make sure that you cant go negatice// Capture to left
                if self.board[r-1][c-1][0] == 'b': #Check for black piece
                    moves.append(Move((r,c), (r-1,c-1), self.board))

            if c+1 <= 7: #Make sure that you cant go negatice
                if self.board[r-1][c+1][0] == 'b': #Check for black piece
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        else: #black pawn moves
            if self.board[r+1][c] == "--": #1 SQ pawn adv
                moves.append(Move((r, c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 SQ pawn adv
                    moves.append(Move((r,c), (r+2,c), self.board))

            if c-1 >= 0: #Make sure that you cant go negatice// Capture to left
                if self.board[r+1][c-1][0] == 'w': #Check for black piece
                    moves.append(Move((r,c), (r+1,c-1), self.board))

            if c+1 <= 7: #Make sure that you cant go negatice
                if self.board[r+1][c+1][0] == 'w': #Check for black piece
                    moves.append(Move((r,c), (r+1,c+1), self.board))
        #add pawn promotions


    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "b" if self.whiteToMove else "w"

        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,1), (1,-1), (1,1),(-1,0), (0,-1), (1,0), (0,1))
        allyColor = "b" if self.whiteToMove else "w"

        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))




class Move():
    #maps keys to values

    #key : value
    ranks_row = {"1": 7, "2": 6, "3": 5, "4":4,
                 "5": 3, "6": 2, "7": 1, "8": 0}
    row_ranks = {v: k for k, v in ranks_row.items()}

    files_col = {"a": 0, "b": 1, "c": 2, "d": 3,
                 "e": 4, "f": 5, "g": 6, "f": 7}
    col_files = {v: k for k, v in files_col.items()}


    #Wanting to store moves
    def __init__(self, startSQ, endSQ, board):
        self.start_r = startSQ[0]
        self.start_c = startSQ[1]

        self.end_r = endSQ[0]
        self.end_c = endSQ[1]

        self.piece_m = board[self.start_r][self.start_c]
        self.piece_cap = board[self.end_r][self.end_c]

        self.move_id = self.start_r * 1000 + self.start_c *100 + self.end_r * 10 + self.end_c

    """
    Overriding equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def getChessNotation(self):
        return self.getRankFile(self.start_r, self.start_c) + self.getRankFile(self.end_r, self.end_c)

    def getRankFile(self, r, c):
        return self.col_files[c] + self.row_ranks[r]
 







