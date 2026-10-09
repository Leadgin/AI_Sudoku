import time

class SudokuInput:
    def __init__(self):
        self.sudokuType = input("Please enter the type of Sudoku\n1. 4x4\n2. 9x9\nChoice: ")
        self.sudokuBoard = []

        print("\nPlease enter the numbers into each row (E.g.1234)")
        print("Enter 0 for empty or missing cells")

        size = 4 if self.sudokuType == "1" else 9
        for i in range(size):
            row = str(input(f"Row {i+1}: "))
            rowNumbers = [int(x) for x in row]
            self.sudokuBoard.append(rowNumbers)

        print("\nNow enter the GOAL (solved) Sudoku state (no zeroes):")
        self.goalBoard = []
        for i in range(size):
            row = str(input(f"Goal Row {i+1}: "))
            rowNumbers = [int(x) for x in row]
            self.goalBoard.append(rowNumbers)


class DFS_Solver:
    call_count = 0
    max_stack_depth = 0

    def __init__(self, board, goal, sudokuType):
        self.board = board
        self.goal = goal
        self.size = len(self.board)
        self.box_size = 2 if sudokuType == "1" else 3
        self.current_depth = 0

        # check if initial puzzle is valid before solving
        if not self.is_valid_board():
            print("\nInitial puzzle is invalid")
            print("No solution exists.")
            return

        start_time = time.time()
        solved = self.solve()
        end_time = time.time()

        elapsed_time = end_time - start_time

        print("\n--- DFS Results ---")
        if solved:
            print("Completeness: Solution found")
            if self.board == self.goal and self.is_valid_board():
                print("Optimality: Solution matches the goal state")
            else:
                print("Optimality: A solution was found but does not match the goal")
        else:
            print("Completeness: No solution")

        print(f"Nodes expanded (DFS calls): {DFS_Solver.call_count}")
        print(f"Maximum recursion depth (space complexity): {DFS_Solver.max_stack_depth}")
        print(f"Time taken: {elapsed_time:.6f} seconds")

    def is_valid(self, row, col, num):
        # Check row
        for j in range(self.size):
            if self.board[row][j] == num and j != col:
                return False
        # Check column
        for i in range(self.size):
            if self.board[i][col] == num and i != row:
                return False
        # Check subgrid
        start_row = (row // self.box_size) * self.box_size
        start_col = (col // self.box_size) * self.box_size
        for i in range(start_row, start_row + self.box_size):
            for j in range(start_col, start_col + self.box_size):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        return True

    def is_valid_board(self):
        """Validate entire board at any stage"""
        for i in range(self.size):
            for j in range(self.size):
                num = self.board[i][j]
                if num != 0:
                    if not self.is_valid(i, j, num):
                        return False
        return True

    def dfs(self):
        DFS_Solver.call_count += 1
        self.current_depth += 1
        DFS_Solver.max_stack_depth = max(DFS_Solver.max_stack_depth, self.current_depth)

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            if self.dfs():
                                self.current_depth -= 1
                                return True
                            self.board[i][j] = 0
                    self.current_depth -= 1
                    return False
        self.current_depth -= 1
        return True

    def solve(self):
        if self.dfs():
            if self.is_valid_board():
                print("\nSolution Found:")
                for row in self.board:
                    print(row)
                return True
            else:
                print("Invalid solution produced")
                return False
        else:
            print("No solution exists.")
            return False


if __name__ == "__main__":
    sudoku_input = SudokuInput()
    DFS_Solver(sudoku_input.sudokuBoard, sudoku_input.goalBoard, sudoku_input.sudokuType)
