import time

class SudokuAStar:
    nodesExpanded = 0
    maxFrontier = 0

    @staticmethod
    def copyBoard(originalBoard):
        #like deepcopy, used for testing
        #basically makes a copy of og board to test lor, later update until goal state then gg
        return [list(row) for row in originalBoard] 

    @staticmethod
    def findEmpty(board, size):
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    return r, c
        return None

    @staticmethod
    def isValid(board, num, pos, size):
        r, c = pos
        # row
        for j in range(size):
            if board[r][j] == num:
                return False
        # col
        for i in range(size):
            if board[i][c] == num:
                return False
        # box
        boxSize = 2 if size == 4 else 3
        boxRow = (r // boxSize) * boxSize
        boxColumn = (c // boxSize) * boxSize
        for i in range(boxRow, boxRow + boxSize):
            for j in range(boxColumn, boxColumn + boxSize):
                if board[i][j] == num:
                    return False
        return True

    @staticmethod
    def emptyCells(board, size):
        # h(n): remaining blanks (admissible if each placement costs 1)
        blanks = 0
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    blanks += 1
        return blanks

    @staticmethod
    def filledCells(board, size):
        filled = 0
        for r in range(size):
            for c in range(size):
                if board[r][c] != 0:
                    filled += 1
        return filled

    @staticmethod
    def goalMatching(board, goalBoard, size):
        for r in range(size):
            for c in range(size):
                if board[r][c] != goalBoard[r][c]:
                    return False
        return True

    @staticmethod
    def printResuts(left, right, size):
        print("Completed Sudoku:  Goal State:")
        for r in range(size):
            print(" ".join(str(x) for x in left[r]) + " | " +
                  " ".join(str(x) for x in right[r]))

    # ---------------- A* core (list-based PQ) ----------------
    @staticmethod
    def AAAAAAAAAAAAStar(startBoard, goalBoard, size):
        SudokuAStar.nodesExpanded = 0
        SudokuAStar.maxFrontier = 0

        gn = SudokuAStar.filledCells(startBoard, size) #filled cell's number (effort so far)
        hn = SudokuAStar.emptyCells(startBoard, size) #empty cell's number (effort remaining)
        
        # frontier = fn and gn + board state
        frontier = [[gn + hn, gn, SudokuAStar.copyBoard(startBoard)]]
        if len(frontier) > SudokuAStar.maxFrontier:
            SudokuAStar.maxFrontier = len(frontier)

        # like exams doing search tree
        while frontier:
            # compare frontier's fn and pick smallest fn
            minFn = 0
            for i in range(1, len(frontier)):
                if frontier[i][0] < frontier[minFn][0]:
                    minFn = i
            f, g, board = frontier.pop(minFn) #take out smallest fn by pop (aka expanding)

            SudokuAStar.nodesExpanded += 1

            #finish
            if SudokuAStar.emptyCells(board, size) == 0:
                if SudokuAStar.goalMatching(board, goalBoard, size):
                    return True, board #complete, return the completed board to print 

            emptyPos = SudokuAStar.findEmpty(board, size)
            if emptyPos is None:
                continue
            r, c = emptyPos #insert row and col of empty cell

            for num in range(1, size + 1):
                if SudokuAStar.isValid(board, num, (r, c), size): #do checking if putting the value is valid
                    newBoard = SudokuAStar.copyBoard(board)
                    newBoard[r][c] = num #write on deepcopy board

                    #------------------------updates------------------------
                    newGN = g + 1
                    newHN = SudokuAStar.emptyCells(newBoard, size)

                    frontier.append([newGN + newHN, newGN, newBoard])

                    if len(frontier) > SudokuAStar.maxFrontier:
                        SudokuAStar.maxFrontier = len(frontier)

        return False, startBoard #not complete, return startboard cause cannot finish lor

    @staticmethod
    def solve(startBoard, goalBoard, size):
        complete, completedBoard = SudokuAStar.AAAAAAAAAAAAStar(startBoard, goalBoard, size)
        print("\n============================================")
        if complete:
            SudokuAStar.printResuts(completedBoard, goalBoard, size) #compare completed and goal board
            print(f"Nodes expanded: {SudokuAStar.nodesExpanded}")
            print(f"Max frontier size: {SudokuAStar.maxFrontier}")
            print("\nCompleteness : Complete")
        else:
            print("No solution found.")
            print(f"Nodes expanded: {SudokuAStar.nodesExpanded}")
            print(f"Max frontier size: {SudokuAStar.maxFrontier}")
            print("\nCompleteness : Not Complete")

# ================================ Main ================================
if __name__==("__main__"): 
    sudokuType = input("Please enter the type of Sudoku\n1. 4x4\n2. 9x9\nChoice: ")
    sudokuBoard = []
    goalBoard = []
    size = 4 if sudokuType == "1" else 9

    print(f"Please enter the numbers into each row (E.g. 1204 for 4x4, or 123056709 for 9x9)")
    print("Enter 0 for empty or missing cells")
    for i in range(size):
        row = input(f"Row {i+1}: ").strip()
        nums = [int(x) for x in row]
        assert len(nums) == size, "Row length mismatch"
        sudokuBoard.append(nums)

    print(f"Please enter goal state of the board (E.g. 1234 for 4x4, or 123456789 for 9x9)")
    print("Enter 0 for empty or missing cells")
    for i in range(size):
        row = input(f"Row {i+1}: ").strip()
        nums = [int(x) for x in row]
        assert len(nums) == size, "Row length mismatch"
        goalBoard.append(nums)

    start = time.time()
    SudokuAStar.solve(sudokuBoard, goalBoard, size)
    end = time.time()

    print(f"Time Complexity (wall time): {(end-start)} s")
    print(f"Space Complexity (max frontier): {SudokuAStar.maxFrontier}")
