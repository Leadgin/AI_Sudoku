import time

class SudokuSolver:
    current_depth = 0
    max_depth = 0
    nodes_expanded = 0
    backtrack_count = 0  
    #Imageine Minecraft without the Z axis, working with matrixes
    @staticmethod
    def solve(sudokuBoard,goalBoard,size):
        if SudokuSolver.backtrack(sudokuBoard,goalBoard, size):
            print("\n============================================")
            print("Completed Sudoku:  Goal State:")
            for row in range(size):
                print(" ".join(str(num) for num in sudokuBoard[row])+" | "+" ".join(str(num) for num in goalBoard[row]))
            print(f"Backtracked {SudokuSolver.backtrack_count} times")
            print(f"\n\nCompleteness : Complete")
            print (f"Nodes Expanded : {SudokuSolver.nodes_expanded}")

        else:
            print("\n\nCompleteness : Not Complete")   

    def backtrackCounter():
        SudokuSolver.backtrack_count += 1
#================================================================    
# This is searching for empty cells and retun their coords if found     
    @staticmethod   
    def findEmpty(board, size):
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    return r, c
        return None
    
    @staticmethod
    def isValid(board, num, pos, size):
        # Row check
        for c in range(size):
            if board[pos[0]][c] == num:
                return False

        # Column check
        for r in range(size):
            if board[r][pos[1]] == num:
                return False

        # Box check
        boxSize = 2 if size == 4 else 3
        boxRow = pos[0] // boxSize
        boxCol = pos[1] // boxSize

        for r in range(boxRow * boxSize, boxRow * boxSize + boxSize):
            for c in range(boxCol * boxSize, boxCol * boxSize + boxSize):
                if board[r][c] == num:
                    return False
        return True

#================================================================
#IMPORTANT FUNCTION
    @staticmethod
    def backtrack(board,goalBoard, size):
        SudokuSolver.current_depth += 1
        SudokuSolver.nodes_expanded += 1
        SudokuSolver.max_depth = max(SudokuSolver.max_depth, SudokuSolver.current_depth)
        print("============================================")
        SudokuSolver.printBoard(board)
        find = SudokuSolver.findEmpty(board, size)
        if not find:
            SudokuSolver.current_depth -= 1
            if SudokuSolver.goalMatching(board, goalBoard, size):
                return True
            return False
        row, col = find #find becomes an array with row and column

        for num in range(1, size+1):
            if SudokuSolver.isValid(board, num, (row, col), size):
                board[row][col] = num

                if SudokuSolver.backtrack(board, goalBoard, size): #Go to line 44 (kinda like a loop)
                    SudokuSolver.current_depth -= 1
                    return True #once everything is checked and valid, it will close the functions by returning true to end the loop

                board[row][col] = 0
        SudokuSolver.backtrackCounter()
        print("Backtracking...")
        print("============================================")
        SudokuSolver.printBoard(board)
        SudokuSolver.current_depth -= 1
        return False

    @staticmethod
    def goalMatching(board, goalBoard, size):
        for r in range(size):
            for c in range(size):
                if board[r][c] != goalBoard[r][c]:
                    return False
        return True
#================================================================ 
    @staticmethod
    def printBoard(sudokuBoard):
        for row in sudokuBoard:
            print(" ".join(str(num) for num in row))
            

#================================================================
#Main
if __name__==("__main__"): 
    sudokuType = input("Please enter the type of Sudoku\n1. 4x4\n2. 9x9\nChoice: ")
    sudokuBoard = [] #its a matrix now
    goalBoard = [] 
    size = 4 if sudokuType == "1" else 9

    print(f"Please enter the numbers into each row (E.g.1234)")
    print(f"Enter 0 for empty or missing cells")
    
    for i in range(0,size):  
        row = str(input(f"Row {i+1}: "))
        rowNumbers = [int(x) for x in row] #for each loop
        sudokuBoard.append(rowNumbers) #put a list into another list = matrix
#================================================================
#for goal state
    print(f"Please enter goal state of the board (E.g.1234)")
    print(f"Enter 0 for empty or missing cells")

    for i2 in range(0,size):  
        row = str(input(f"Row {i2+1}: "))
        rowNumbers = [int(x) for x in row] 
        goalBoard.append(rowNumbers)

    start = time.time()
    SudokuSolver.solve(sudokuBoard,goalBoard,size)
    end = time.time()

    print(f"Time Complexity: {(end-start)}")
    print(f"Space Complexity: {SudokuSolver.max_depth}")