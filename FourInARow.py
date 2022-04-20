import random

def inarow_Neast(ch, r_start, c_start, A, N):
    """Checks for the possibility of N pieces in a row being placed horizontally"""
    num_rows = len(A)      # Number of rows is len(A)
    num_cols = len(A[0])   # Number of columns is len(A[0])
    if r_start < 0 or r_start >= num_rows:
        return False       # Out of bounds in rows
    # Other out-of-bounds checks...
    if c_start < 0 or c_start > num_cols - N:
        return False       # Out of bounds in columns
    # Are all of the data elements correct?
    for i in range(N):                  # Loop index i as needed
        if A[r_start][c_start+i] != ch: # Check for mismatches
            return False                # Mismatch found--return False
    return True                         # Loop found no mismatches--return True


def inarow_Nsouth(ch, r_start, c_start, A, N):
    """Checks for the possibility of N pieces in a row being placed vertically"""
    num_rows = len(A)
    num_cols = len(A[0])
    if c_start<0 or c_start>= num_cols:
        return False
    if r_start<0 or r_start> num_rows-N:
        return False
    if r_start<0 or r_start>num_rows+N:
        return False
    for i in range(N):
        if A[r_start+i][c_start]!= ch:
            return False
    return True


def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """Checks for the possibility of N pieces in a row being placed diagonally"""
    C=r_start
    if len(A) - r_start<= N-1 or len(A[0])-c_start<= N-1:
        return False
    for i in range(c_start, c_start+N):
        if A[C][i] != ch:
            return False
        C+=1
    return True


def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """Checks for the possibility of N pieces in a row being placed diagonally"""
    X = r_start
    if r_start < N-1 or len(A[0])-c_start <=N-1:
        return False
    for i in range(c_start, c_start+N):
        if A[X][i] != ch:
            return False
        X-=1
    return True


class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """


    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]


    def __repr__(self):
        """This method returns a string representation
           for an object of type Board.
        """
        s = ''                          # The string to return
        for row in range(0, self.height):
            s += '|'
            for col in range(0, self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # Bottom of the board
        s += '\n'
        for col in range(0, self.width): 
            s+= ' '+ str(col)

        return s       # Returning the Board


    def addMove(self, col, ox):
        """ takes two arguments, the col representing the column the checker will be added to
        and the secong argument is ox which is the character that will be added, this functions will
        add the appropriate character to the board and makes sure it slides down from the top 
        of the board"""

        H = self.height
        for row in range(0,H):
            if self.data[row][col]!= ' ':
             self.data[row-1][col] = ox
             return
        self.data[H-1][col] = ox

            
    def clear(self):
        """ should clear the board that calls it""" 

        for x in range(self.height):
            for y in range(self.width):
                self.data[x][y] = ' '
    

    def setBoard(self, moveString):
        """Accepts a string of columns and places
           alternating checkers in those columns,
           starting with 'X'.

           For example, call b.setBoard('012345')
           to see 'X's and 'O's alternate on the
           bottom row, or b.setBoard('000000') to
           see them alternate in the left column.

           moveString must be a string of one-digit integers.
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'


    def allowsMove(self,col):
        """ True if col is in-bounds + open
        False otherwise"""
        if col not in range(self.width):
            return False

        elif self.data[0][col] != ' ':
            return False
        else:
            return True


    def isFull(self):
        """ returns True if the board is completely full of checkers
        false otherwise"""
        
        for x in range(self.height):
            for y in range(self.width):
                if self.data[x][y] == " ":
                    return False
        return True


    def delMove(self, c):
        """ does the opposite of addMove, removes the top checker from the column"""

        H = self.height

        for row in range(0,H):
            if self.data[row][c] != ' ':
             self.data[row][c] = " "
             return


    def winsFor(self, ox):
        """ checks for either X or O and returns True if there are 4 of them in a row"""

        H = self.height
        W = self.width
        D = self.data

        for row in range(H):
            for col in range(W):
                if inarow_Neast(ox, row, col, D, 4) == True:
                    return True
                if inarow_Nsouth(ox, row, col, D, 4) == True:
                    return True
                if inarow_Nsoutheast(ox, row, col, D, 4) == True:
                    return True
                if inarow_Nnortheast(ox, row, col, D, 4) == True:
                    return True
        return False


    def colsToWin(self, OX):
        "It returns a list of colums at which OX would win on the next move"

        List = []

        for x in range(7):
            if self.allowsMove(x) == True:
                self.addMove(x, OX) 
                if self.winsFor(OX) == True:
                    List += [x]
            self.delMove(x)
        return List


    def ChecksOther(self, OX):
        "Checks the possibilities of the other player"

        if OX == "X":
            self.colsToWin("O")
            return self.colsToWin("O")
        elif OX == "O":
            self.colsToWin("X")
            return self.colsToWin("X")


    def aiMove(self, OX):
        "Return a winning move, or a blocking move, or default to a position in the middle"

        WINX = self.colsToWin(OX)
        WINY = self.ChecksOther(OX)

        if WINX != [] :
            return WINX[0]
        elif WINX == [] and WINY != []:
            return WINY[0]
        else:
            width = self.width
            for x in range(width):
                y = random.choice(range(width))
                if self.allowsMove(y) == True:
                    
                    return y


    def hostGame(self):
            """This method brings everything together into the familiar game. 
            It should host a game of Connect Four, using the methods listed above to do so. In particular,
            it should alternate turns between 'X' (who will always go first) and 'O' (who will always go second). 
            It should ask the user (with the input function) to select a column number for each move"""
            print('Welcome to Connect Four!')
            while True:
                print()
                print(self)
        
                self.addMove(self.aiMove("X"), "X")
                   
                print(self)
                if self.winsFor("X"):
                    print("Congratulatiosn X")
                    break 
                if self.isFull():
                    return print("It is a tie!")
                Column_2 = int(input("O's choice:"))
                while not self.allowsMove(Column_2):
                     Column_2 = int(input("O's choice:"))
                self.addMove(Column_2, 'O')
                print(self)
                if self.winsFor("O"):
                    print("Congratulations O") 
                    break
                if self.isFull():
                    return print("It is a tie!")

