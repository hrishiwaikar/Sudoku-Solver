# Sudoku Solver
# Author: Hrishikesh Waikar

#Notes
'''
try to solve the board as much as possible through basic techniques
once there are no improvements,
switch to advanced mode 
1.
'''
class SudokuSolver(object):

    def __init__(self):
        # define the board
        self.sudoku_board = Board()
        board = self.sudoku_board.board
        self.sudoku_board.displayBoard()
        self.quadrants = {}
        self.rows = {}
        self.columns = {}
        self.generate_quadrant_metadata()
        self.generate_row_metadata()
        self.generate_column_metadata()
        self.displayQuadrants()
        print self.solve()
        self.sudoku_board.displayBoard()
        self.displayQuadrants()

    def solve(self):
        # try to solve the puzzle by iteratively trying to solve the quadrants, rows and columns

        # self.solve_quadrants()
        # return
        iterations = 0
        while self.solved() is False and iterations < 10:
            iterations += 1
            print '\nIteration ' + str(iterations)
            # attempt solving all quadrants 
            quadrant_improvements = self.solve_quadrants()
            row_improvements = self.solve_rows()
            column_improvements = self.solve_columns()
            # attempt solving all rows
            # attempt solving all columns

        return self.solved()


    def solve_quadrants(self):

        quadrant_improvements = 0

        for k in range(9):
            # print '\n\n\nFor quadrant ' + str(k)
            pending_numbers = self.quadrants[k]["pending_numbers"]
            region = self.quadrants[k]["region"]
            # print "pending numbers " + str(pending_numbers)
            # for p in range(len(pending_numbers)):
            p = 0
            while p < len(pending_numbers):
                pending_number = pending_numbers[p]
                # print '\nFor pending no ' + str(pending_number)
                acceptable_matches = []
                # check with every vacant position if the pending no makes acceptable match

                for i in range(region["iStart"], region["iEnd"] + 1):
                    for j in range(region["jStart"], region["jEnd"] + 1):
                        position = self.sudoku_board.board[i][j]
                        # print 'Checking with position ' + str(i) + ' ' + str(j)
                        if position == '' and self.is_acceptable_match(i, j, pending_number) is True:
                            # print 'Found one'
                            acceptable_matches.append([i, j])
                    
                # print 'Acceptable matches ' + str(acceptable_matches)
                if len(acceptable_matches) == 1:
                    x = acceptable_matches[0][0]
                    y = acceptable_matches[0][1]
                    self.sudoku_board.board[x][y] = pending_number
                    self.remove_pending_number(x, y, pending_number)
                    quadrant_improvements += 1
                    # print 'Adding ' + str(pending_number) + ' at ' + str(x) + ', ' + str(y)
                
                p += 1
        
        return quadrant_improvements

    def solve_rows(self):
        row_improvements = 0

        for i in range(9):
            pending_numbers = self.rows[i]["pending_numbers"]

            p = 0
            while p < len(pending_numbers):
                pending_number = pending_numbers[p]
                acceptable_matches = []
                for j in range(9):
                    position = self.sudoku_board.board[i][j]
                    if position == '' and self.is_acceptable_match(i, j, pending_number) is True:
                            # print 'Found one'
                            acceptable_matches.append([i, j])

                if len(acceptable_matches) == 1:
                        print 'Found in row' 
                        x = acceptable_matches[0][0]
                        y = acceptable_matches[0][1]
                        self.sudoku_board.board[x][y] = pending_number
                        self.remove_pending_number(x, y, pending_number)
                        row_improvements += 1                
                p += 1
        return row_improvements


    def solve_columns(self):
        column_improvements = 0
        for j in range(9):
            pending_numbers = self.columns[j]["pending_numbers"]

            p = 0
        

            while p < len(pending_numbers):
                pending_number = pending_numbers[p]
                acceptable_matches = []
                for i in range(9):
                    position = self.sudoku_board.board[i][j]
                    if position == '' and self.is_acceptable_match(i, j, pending_number) is True:
                            # print 'Found one'
                            acceptable_matches.append([i, j])

                if len(acceptable_matches) == 1:
                        print 'Found in Column' 
                        x = acceptable_matches[0][0]
                        y = acceptable_matches[0][1]
                        self.sudoku_board.board[x][y] = pending_number
                        self.remove_pending_number(x, y, pending_number)
                        column_improvements += 1
                
                p += 1
        return column_improvements


    def remove_pending_number(self, x, y, pending_number):
        self.rows[x]["pending_numbers"].remove(pending_number)
        self.columns[y]["pending_numbers"].remove(pending_number)
        print 'Adding ' + str(pending_number) + ' at ' + str(x) + ', ' + str(y)
        quadrant_no = self.getQuadrantNo(x, y)

        self.quadrants[quadrant_no]["pending_numbers"].remove(pending_number)

    def is_acceptable_match(self, x, y, number):
        quadrant_no = self.getQuadrantNo(x, y)

        # print 'Qudarant no. for ' + str(x) + ' , ' + str(y) + ' : ' + str(quadrant_no)

        if number not in self.quadrants[quadrant_no]["pending_numbers"]:
            # print '\nNo ' + str(number) + ' is present in quadrant ' + str(quadrant_no) 
            return False
        
        if number not in self.rows[x]["pending_numbers"]:
            # print 'No ' + str(number) + ' is present in row ' + str(x) 
            return False
        
        if number not in self.columns[y]["pending_numbers"]:
            # print 'No ' + str(number) + ' is present in column ' + str(y) 
            return False

        # print 'No 7 is not present in quadrant ' + str(quadrant_no) + ' , row ' + str(x) + ' , col ' + str(y)
        return True


    def getQuadrantNo(self, x, y):
        quadrant_indices = self.getQuadrantStartAndEndIndices()

        for k in range(9):
            iStart = quadrant_indices[k][0]
            iEnd = quadrant_indices[k][1]
            jStart = quadrant_indices[k][2]
            jEnd = quadrant_indices[k][3]

            if iStart <= x <= iEnd and jStart <= y <= jEnd:
                return k

    def solved(self):
        for i in range(9):
            if len(self.rows[i]["pending_numbers"]) != 0:
                return False
        
        return True

    def displayQuadrants(self):
        print '\nQuadrant Metadata: '
        for q in self.quadrants:
            print q, self.quadrants[q]

        print '\nRow Metadata'

        for r in self.rows:
            print r, self.rows[r]

        print '\nColumn Metadata'
        for c in self.columns:
            print c, self.columns[c]

    def generate_quadrant_metadata(self):
       
        # generate q , key -> quadrants number, value -> metadata : pending numbers, indices,etc
        quadrants = self.quadrants
        quadrant_indices = self.getQuadrantStartAndEndIndices()

        for k in range(9):
            iStart = quadrant_indices[k][0]
            iEnd = quadrant_indices[k][1]
            jStart = quadrant_indices[k][2]
            jEnd = quadrant_indices[k][3]

            requirements = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for i in range(iStart, iEnd + 1):
                for j in range(jStart, jEnd + 1):
                    value = self.sudoku_board.board[i][j]
                    if value != '':
                        requirements.remove(value)

            quadrants[k] = {
                "pending_numbers": requirements,
                "region": {
                    "iStart": iStart,
                    "iEnd": iEnd,
                    "jStart": jStart, 
                    "jEnd": jEnd,
                }
                
            }

    def generate_row_metadata(self):
        rows = self.rows

        for i in range(9):
            requirements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for j in range(9):
                value = self.sudoku_board.board[i][j]
                if value != '':
                    requirements.remove(value)

            rows[i] = {
                "pending_numbers": requirements,
            }


    def generate_column_metadata(self):
        columns = self.columns
   

        for j in range(9):
            requirements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(9):
                value = self.sudoku_board.board[i][j]
                if value != '':
                    requirements.remove(value)

            columns[j] = {
                "pending_numbers": requirements
            }

    def getQuadrantStartAndEndIndices(self): 
        indices = {
            0: [0, 2, 0, 2],
            1: [0, 2, 3, 5],
            2: [0, 2, 6, 8],
            3: [3, 5, 0, 2],
            4: [3, 5, 3, 5],
            5: [3, 5, 6, 8],
            6: [6, 8, 0, 2],
            7: [6, 8, 3, 5],
            8: [6, 8, 6, 8]
        }

        return indices

    

class Board(object):
    def __init__(self):

        self.board = [
            ['','','', '','',1, '','',7],#0
            [1,'','', '',5, 6, 2,'',4],#1
            [5,'',3, '','',8, 1,'',9],#2
            [9,1,'', 8,3,'', '','',6],#3
            ['','','',  1,7,'', '','',''],#4
            [8,'',4,  6,9,5, '',2,1],#5
            [6,8,'', 5,1,3, 4,'', 2],#6
            ['',5,1, '',6,'', '','',''],#7
            ['','','', '',8,'', 6,1,5],#8

        ]
        # self.board = [
        #     # 0   1    2      3     4    5     6     7    8
        #     [ '', '', '',   '',  '', '',    '', '',''], # 0
        #     [ '', 2,  '',    '', '',  4,   '', '', 5 ], # 1
        #     [ 5, 3, 4,    6,  '',  '',  1, '', '' ], # 2
            
        #     [ '', 4,  '',    '', '', 7,   '',8 ,'' ], # 3
        #     [ '',  '', '',   1 , '', '',   '', 4, 9 ], # 4
        #     [ '',  '', '',    2,  '', '',  '', '', '' ], # 5
            
        #     [ '',  '',  '',   '',  '',  2,  '', '',  '' ], # 6
        #     [ 3,  9,   '',   '', '', 1,   8, 7, '' ], # 7
        #     [ '',  '',  8,    4, 7,  9,   2,  '', 6 ]  # 8
        # ]  

        # self.board = [
        #     # 0   1    2      3     4    5     6     7    8
        #     [ '',  6,  9,    '',  '',  '',    8,  '',   7 ], # 0
        #     [ 4,  '',   '',     '',  1,  '',     5,  '',  '' ], # 1
        #     [ 5,  2,  7,      6,  '',   '',     '',   3,   1 ], # 2
            
        #     [ 3,   '',  5,    2,  '',  4,     '',  6 , '' ], # 3
        #     [ '',  7,   '',   '' , '' ,  '',     '',  '',  4 ], # 4
        #     [ '',  '',  2,     1,  5,  '',       '', '',   '' ], # 5
            
        #     [ 2,   '',   6,     8,   '',   '',     4,  9,  '' ], # 6
        #     [ 9,  3,   '',    '',  '' , '',     7, 8,  2 ], # 7
        #     [ '',  '',  8,    '',  '',  '',        '',   1,  '' ]  # 8
        # ]  

    

    def displayBoard(self):
        print "\n      0    1    2       3    4    5       6    7     8"
        for i in range(9):
            
            if i in [3, 6]:
                print 

            print
            for j in range(9):
                if j == 0:
                    print str(i) + " ", 

                if j in [3, 6]:
                    print "  ",
                value = str(self.board[i][j]) if self.board[i][j] != '' else '-'
            
                print "   " + value,

        print "\n"

sudokuSolver = SudokuSolver()
