# Sudoku Solver
# Author: Hrishikesh Waikar

#Notes
'''
try to solve the board as much as possible through basic techniques
once there are no improvements,
switch to advanced mode 
First find 
'''

import copy

'''
Represents a number and it's 2 possible positions, one of which is going to be correct.
'''
class DualPositionTrial(object):
    def __init__(self, number, position_1, position_2, location_type):
        self.number = number
        self.position_1 = position_1
        self.position_2 = position_2
        self.type = location_type
    
class SudokuSolver(object):

    def __init__(self, board=None, number=None, x=None, y=None):
        self.quadrants = {}
        self.rows = {}
        self.columns = {}
        self.dual_position_trials = []
        self.encountered_failure_condition = False
            
        if board is None:
            # define the board
            print "Creating an initial board"
            self.sudoku_board = Board()
            # print self.solve()
            # self.sudoku_board.displayBoard()
            # self.displayQuadrants()
            
        else:
            print 'Creating a board out of prev board ' 
            self.sudoku_board = Board(board, number, x, y)

        self.generate_quadrant_metadata()
        self.generate_row_metadata()
        self.generate_column_metadata()
        self.sudoku_board.displayBoard()
        self.in_confusion_state = False            
        self.displayQuadrants()
        print '\n\n'
            
    def is_solved(self):
        # check quadrants
        for k in range(9):
            region = self.quadrants[k]["region"]
            requirements = [1, 2, 3, 4, 5, 6, 7 , 8 , 9]

            for i in range(region["iStart"], region["iEnd"] + 1):
                for j in range(region["jStart"], region["jEnd"] + 1):
                    value = self.sudoku_board.board[i][j]
                    if value != '':
                        # print 'Value is ' + str(value) + ' at ' + str(i) + ' ' + str(j)
                        if value not in requirements:
                            print 'Req doesnt have the value ' + str(value) + ' at ' + str(i) + ' ' + str(j)
                        requirements.remove(value)
                
            if len(requirements) != 0:
                return False

        # check rows
        for i in range(9):
            requirements = [1, 2, 3, 4, 5, 6, 7 , 8 , 9]
            for j in range(9):
                value = self.sudoku_board.board[i][j]
                if value != '':
                    requirements.remove(value)
            
            if len(requirements) != 0:
                return False

        # check cols 
        for j in range(9):
            requirements = [1, 2, 3, 4, 5, 6, 7 , 8 , 9]
            
            for i in range(9):
                value = self.sudoku_board.board[i][j]
                if value != '':
                    requirements.remove(value)
            
            if len(requirements) != 0:
                return False

        return True

    
    def master_solve(self):
        # solve using preliminary solve initially
        # if not solved, inititate stage 2 
        preliminary_result = self.solve()  # can be success or a confusion state

        if preliminary_result is True:
            return preliminary_result
        
        self.displayTrials()
        
        if preliminary_result is None:

            current_trial_index = 0
            count = 0
            while len(self.dual_position_trials) > 0 and count < 50:
                count += 1
                dual_position_trial = self.dual_position_trials[current_trial_index]
                
                # create a child solver trying number at position 1 from dual position trial
                number = dual_position_trial.number
                position_1 = dual_position_trial.position_1
                position_2 = dual_position_trial.position_2

                print '\n\n    ====    ====   =====   \nCreating a child solver process ' 
                print 'For number ' + str(number) + ' at position 1 ' + str(position_1)
                print 'Parent board '
                print self.sudoku_board.board
                child_solver = SudokuSolver(copy.deepcopy(self.sudoku_board.board), number, position_1[0], position_1[1])
                child_result = child_solver.solve()
                print 'First Child result'
                print child_result

                # success condition
                if child_result is True:
                    # apply the position 1 to this board and re solve again knowing it will bear success

                    self.sudoku_board.board[position_1[0]][position_1[1]] = number
                    self.in_confusion_state = False
                    self.solve()
                    
                    return True

                # failure condition
                elif child_result is False: 
                    print 'Since first child result is false, assigning value to second position' 
                    
                    # then it is certain that position 2 is correct
                    self.sudoku_board.board[position_2[0]][position_2[1]] = number
                    self.generate_quadrant_metadata()
                    self.generate_row_metadata()
                    self.generate_column_metadata()
        
                    self.dual_position_trials = []
                    self.in_confusion_state = False
                    self.sudoku_board.displayBoard()
                    print 'Solving after assigngin to the second position'
                    position_2_result = self.solve()
                    if position_2_result is False:
                        print '\n\n\n\n ALERT! Both positions are failing, something is wrong !!!\n\n\n\n'
                        return False
                    if position_2_result is True:
                        # This other position was not only correct but lead to success
                        print '\n\nFOund SUCCESS in the other position\n\n'
                        return True

                    if position_2_result is None:
                        print '\n\nAssumption that the other position is correct is is verified'

                    print 'Removing trial at index: ' + str(current_trial_index) + ' , ' + str(self.dual_position_trials[current_trial_index].number)
                    del self.dual_position_trials[current_trial_index]
                    current_trial_index = 0

                # Confusion State
                elif child_result is None:
                    # verify with position 2
                    
                    # check the other position by creating a child solver at position 2
                    print '\n\n    ====    ====   =====   \nCreating the 2ND child solver process ' 
                    print 'For number ' + str(number) + ' at position 2 ' + str(position_2)
                    print 'Parent board '
                    self.sudoku_board.displayBoard()
                    second_child_solver = SudokuSolver(copy.deepcopy(self.sudoku_board.board), number, position_2[0], position_2[1])
                    second_child_result = second_child_solver.solve()
                    print 'Second child solver result ' + str(second_child_result)

                    if second_child_result is None:
                        print 'Even Second child gave a confusion state'
                        current_trial_index += 1

                    elif second_child_result is False:
                        # This means the first child is certainly correct
                        print '\nSecond position faliled while 1st position was inconclusive, hence 1st position is definitely correct'
                        self.sudoku_board.board[position_1[0]][position_1[1]] = number
                        self.generate_quadrant_metadata()
                        self.generate_row_metadata()
                        self.generate_column_metadata()
                        self.dual_position_trials = []
                        self.in_confusion_state = False
                        position_1_result = self.solve()
                        print 'Verifying if position 1 result is None: ' + str(position_1_result)
                        if position_1_result is not None:
                            print '\n\nALERT, position 1 result is not None'
                            return False
                        if position_1_result is None:
                            print 'Thus verified position 1 result is NOne, although it is a correct position now'
                            del self.dual_position_trials[current_trial_index]
                            current_trial_index = 0

                    elif second_child_result is True:
                        print '\nBEfore update'
                        self.sudoku_board.displayBoard()
                        self.sudoku_board.board[position_2[0]][position_2[1]] = number
                        print '\nAfter update'
                        self.generate_quadrant_metadata()
                        self.generate_row_metadata()
                        self.generate_column_metadata()
                        self.sudoku_board.displayBoard()
                        self.in_confusion_state = False
                        self.solve()
                        
                        return True


                                
    # ''' 
    # Solves with preliminary logic 
    # Returns result as one of - True: Success, False: Failure, None: Confusion
    # '''

    def solve(self):
        print '\nSolving ...'
        # try to solve the puzzle by iteratively trying to solve the quadrants, rows and columns

        iterations = 0
        blank_count = 0
        
        while self.is_solved() is False and blank_count < 2:
            iterations += 1
            print '\nIteration ' + str(iterations)
            # attempt solving all quadrants 
            quadrant_improvements = self.solve_quadrants()
            row_improvements = self.solve_rows()
            column_improvements = self.solve_columns()

            print 'Quadrant improvements ' + str(quadrant_improvements)
            print 'Row improvements ' + str(row_improvements)
            print 'Column improvements ' + str(column_improvements)

            if quadrant_improvements + row_improvements + column_improvements == 0:
                self.in_confusion_state = True
                blank_count = blank_count + 1


        self.sudoku_board.displayBoard()
        # print 'Solved ' + str(self.is_solved())
        

        if self.encountered_failure_condition is True:
            return False
        elif self.is_solved() is True:
            return True
        else:
            return None
        
    
    
    def displayTrials(self):
        print "\n\nTrial Options"
        for trial in self.dual_position_trials:
            print
            print "Trial Number " + str(trial.number) + ", Type: " + str(trial.type)
            print "Position 1: " + str(trial.position_1) + " , Position 2: " + str(trial.position_2)
        

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
                if len(acceptable_matches) == 0:
                    print '\nFAILURE STATE REACHEDD for pending no ' + str(pending_number) + ' in quadrant ' + str(k)
                    self.encountered_failure_condition = True
                    return 0

                if len(acceptable_matches) == 1:
                    x = acceptable_matches[0][0]
                    y = acceptable_matches[0][1]
                    self.sudoku_board.board[x][y] = pending_number
                    self.remove_pending_number(x, y, pending_number)
                    quadrant_improvements += 1
                    # print 'Adding ' + str(pending_number) + ' at ' + str(x) + ', ' + str(y)
                
                if self.in_confusion_state is True and len(acceptable_matches) == 2:
                    self.dual_position_trials.append(DualPositionTrial(pending_number, acceptable_matches[0], acceptable_matches[1], "QUADRANT"))

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

                if len(acceptable_matches) == 0:
                    print '\nFAILURE STATE REACHEDD for pending no ' + str(pending_number) + ' in row ' + str(i)
                    return 0
            
                if len(acceptable_matches) == 1:
                        print 'Found in row' 
                        x = acceptable_matches[0][0]
                        y = acceptable_matches[0][1]
                        self.sudoku_board.board[x][y] = pending_number
                        self.remove_pending_number(x, y, pending_number)
                        row_improvements += 1    

                if self.in_confusion_state is True and len(acceptable_matches) == 2:
                    self.dual_position_trials.append(DualPositionTrial(pending_number, acceptable_matches[0], acceptable_matches[1], "ROW"))
                
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

                if len(acceptable_matches) == 0:
                    print '\nFAILURE STATE REACHEDD for pending no ' + str(pending_number) + ' in column ' + str(j)
                    return 0

                if len(acceptable_matches) == 1:
                        print 'Found in Column' 
                        x = acceptable_matches[0][0]
                        y = acceptable_matches[0][1]
                        self.sudoku_board.board[x][y] = pending_number
                        self.remove_pending_number(x, y, pending_number)
                        column_improvements += 1

                if self.in_confusion_state is True and len(acceptable_matches) == 2:
                    self.dual_position_trials.append(DualPositionTrial(pending_number, acceptable_matches[0], acceptable_matches[1], "COLUMN"))
                
                
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
                        if value not in requirements:
                            print 'Value missing ' + str(value)
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
    def __init__(self, board=None, number=None, x=None, y=None):
        if board is None:
            print 'Creating a board'
            # original hard 
            # self.board = [
            #     [7,'','',  '','','', 1,'',''],#0
            #     ['',1,'',  '','',2, '','',9],#1
            #     ['','','',  5,7,'', '',2,''],#2
            #     [6,3,8,    '',4,'', '',9,''],#3
            #     ['','','',  1,2,'', '','',''],#4
            #     ['','','',  '','',9, '',8,''],#5
            #     ['',2,4,   '','','', 5,'', 8],#6
            #     [5,'',3,   '','','', '','',''],#7
            #     ['','','', '','','', '',6,''],#8
            # ]

            # board at reaching first confusion state (L0)
            # self.board = [
            #     [7,'',2,  '','','', 1,'',''],#0
            #     ['',1,'',  '','',2, '','',9],#1
            #     ['','','',  5,7,1, '',2,''],#2
            #     [6,3,8,     7,4,5,  2,9,1],#3
            #     ['','','',  1,2,8, '','',''],#4
            #     [2,'',1,  '','',9, '',8,''],#5
            #     [9,2,4,   '','','', 5,'', 8],#6
            #     [5,6,3,   '','','', '','',''],#7
            #     [1,8,7,   '',5,'', '',6,''],#8
            # ]

            # board at reaching first confusion state (L0)
            # self.board = [
            #     [7,'',2,  '','','', 1,'',''],#0
            #     ['',1,'',  '','',2, '','',9],#1
            #     ['','','',  5,7,1, '',2,''],#2
            #     [6,3,8,     7,4,5,  2,9,1],#3
            #     ['','','',  1,2,8, '','',''],#4
            #     [2,'',1,  '','',9, '',8,''],#5
            #     [9,2,4,   '','','', 5,'', 8],#6
            #     [5,6,3,   '','','', '','',''],#7
            #     [1,8,7,   '',5,'', '',6,''],#8
            # ]
            

            #board after assignments due to failures helping determine so
            # self.board = [
            #     [7,'',2,   '','','', 1,'',''],#0
            #     [8,1,'',  '','',2, 7,'',9],#1
            #     [3,4,'',  5,7,1, '',2,''],#2
            #     [6,3,8,     7,4,5,  2,9,1],#3
            #     ['','','',  1,2,8, '','',''],#4
            #     [2,'',1,  '','',9, '',8,''],#5
            #     [9,2,4,   '','','', 5,'', 8],#6
            #     [5,6,3,   '','','', '','',''],#7
            #     [1,8,7,   '',5,'', '',6,''],#8
            # ]
            # ======================

            #Extreme problem , starting position

            # self.board = [
            #     ['','',5,   '','','', 6,'',2],#0
            #     ['',3,'',  '',4,'', 5,'',''],#1
            #     ['','','',  '',3,'', 9,'',''],#2
            #     [6,'','',     '','','',  '',9,''],#3
            #     ['','','',  '','','', '','',''],#4
            #     ['',4,'',  2,'',3, '','',7],#5
            #     [5,2,'',   3,'','', '',8, ''],#6
            #     [9,7,'',   '','',8, '','',4],#7
            #     ['',8,6,   '','','', '','',''],#8
            # ]
            # 0    1    2       3    4    5       6    7     8

            # 0     4    9    5       1    8    7       6    3    2
            # 1     2    3    8       9    4    6       5    7    1
            # 2     1    6    7       5    3    2       9    4    8

            # 3     6    5    2       7    1    4       8    9    3
            # 4     7    1    3       8    6    9       4    2    5
            # 5     8    4    9       2    5    3       1    6    7

            # 6     5    2    4       3    9    1       7    8    6
            # 7     9    7    1       6    2    8       3    5    4
            # 8     3    8    6       4    7    5       2    1    9 



            # Extreme prob, 1st confusion state
            
            # self.board = [
            #     [4,9,5,   '','','',  6,3,2],#0
            #     [2,3,'',  '',4,'',   5,7,''],#1
            #     ['',6,'',  '',3,2,   9,4,''],#2
            #     [6,'','',  '','','', '',9,''],#3
            #     ['','','',  '','','', '','',5],#4
            #     ['',4,9,   2,'',3,   '','',7],#5
            #     [5,2,4,    3,'','',  '',8, 6],#6
            #     [9,7,'',   '','',8,  '','',4],#7
            #     ['',8,6,   '','','', '','',9],#8
            # ]

            #===================
            # ANother Extreme problem 

            # self.board = [
            #     ['','',6,   '','','', '','',''],#0
            #     ['',7,'',  6,8,'', '','',5],#1
            #     ['','','',  '','',2, '','',3],#2
            #     ['',8,'',     '','','',  6,1,''],#3
            #     ['','','',  '','','', '','',''],#4
            #     [5,'',4,  9,'',1, '','',8],#5
            #     [8,'','',   '',9,5, 3,'', ''],#6
            #     ['','','',   '','','', 1,4,''],#7
            #     [3,9,'',   '',4,'', '','',''],#8
            # ]


            #=======================================

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

            # ========== Hard 1
            self.board = [
                [5,'','',   '',7,'', 1,'',''],#0
                [9,'','',  '','','', '','',''],#1
                ['',7,'',  '',4,'',  9,'',''],#2
                ['',1,4,   '',5,6,   '','',''],#3
                ['','',8,  3,'','',  '','',''],#4
                ['','',5,  '','',8,  '',3,''],#5
                ['','','',   '','',2, '','',5],#6
                [1,'','',  '','','',  3,4,''],#7
                ['','','',   6,9,'',  '','',''],#8
            ]

        else:
            self.board = board
            print 'parent Board as available to child '
            print self.board
            # self.displayBoard()
            self.board[x][y] = number 
            print 'Updated board with no ' + str(number) + ' at ' + str(x) + ' , ' + str(y)

    

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
print 'Solve result ' + str(sudokuSolver.master_solve())