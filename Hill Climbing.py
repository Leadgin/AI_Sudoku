import random
import copy
import time
import sys   # <-- added for memory size estimation

#===================================================
# Create a matrix to mark fixed (pre-filled) cells
#===================================================
def fixed_cells(puzzle,N):
    return [[puzzle[r][c] != 0 for c in range(N)] for r in range(N)]
    # it have inner loop and outer loop, it will loop the column in range 9 first and return True or False, if the value = 0 , Return false
    # After that go through the outer loop, it will loop the row in range 9 then return True or False, if the value = 0, it will return False
    # 0 in here means empty and use False to represent it
    # If not = 0 means pre-filled use True to represent it

#===================================================
# Find the empty cells in the board and return their coordinates
#===================================================
#This function fills each block with random numbers ensuring no duplicates within the block
def fill_random(board, fixed, N,block_size):  
    # used to loop the first number in each block
    for brow in range(0, N, block_size):                       #This is outer loop, it will loop the row in range 0 to 9 with step 3
        for bcolumn in range(0, N, block_size):                #This is inner loop, it will loop the column in range 0 to 9 with step 3
            
            missing = set(range(1, N + 1))                     # Create a set of all possible numbers in the block
            
            # Remove already-fixed numbers from missing
            for r in range(brow, brow + block_size):            # Loop through rows in the block
                for c in range(bcolumn, bcolumn + block_size):  # Loop through columns in the block
                    if fixed[r][c]:                             # If the cell is fixed (pre-filled)
                        missing.discard(board[r][c])            # Remove the fixed number from missing
            
            # Randomly shuffle remaining numbers
            missing = list(missing)                             # Convert set to list for shuffling
            random.shuffle(missing)                             # Shuffle the list of missing numbers
            
            # Fill non-fixed spots in the block
            for r in range(brow, brow + block_size):             # Loop through rows in the block
                for c in range(bcolumn, bcolumn + block_size):   # Loop through columns in the block
                    if not fixed[r][c]:                          # If the cell is not fixed
                        board[r][c] = missing.pop()              # Fill it with a number from missing

#===================================================
# Score function 
#===================================================
# This function evaluates the board by counting unique numbers in each row and column
#This function is used to tracking the progress of the algorithm to check whether the board is improving, plateauing, or getting worse
def evaluate(board, N):              
    score = 0                       # Initialize score
    for r in range(N):              # Loop through each row
        row_values = set(board[r])  # Create a set of values in the row
        row_values.discard(0)       # Remove 0 (empty cells) from the set 
        score += len(row_values)    # Add the count of unique numbers in the row to score

    for c in range(N):                  # Loop through each column
        columnValues = {board[r][c] for r in range(N) if board[r][c] !=0 }   # Create a set of values in the column, excluding 0
        score += len(columnValues)     # Add the count of unique numbers in the column to score
    return score                       #The score is based on the number of unique numbers in rows and columns

#=======================================================================================
# Generate a neighbor by swapping two non-fixed cells within a randomly chosen block
#========================================================================================
#This function generates a neighbor by swapping two non-fixed cells within a randomly chosen block
def randomSwapInBlock(board, fixed, N,block_size):
    new_board = copy.deepcopy(board)            # Create a copy of the current board to modify

    br = random.choice(range(0, N, block_size))  # Randomly select the starting row of a block
    bc = random.choice(range(0, N, block_size))  # Randomly select the starting column of a block
    
    cells = []  
    for r in range(br, br + block_size):        # loop over rows in the block
        for c in range(bc, bc + block_size):    # loop over columns in the block
            if not fixed[r][c]:                 # only take non-fixed cells
                cells.append((r, c))            # add coordinates to list

    #if there are at least two non-fixed cells, swap two of them
    if len(cells) >= 2:
        a, b = random.sample(cells, 2)   
        new_board[a[0]][a[1]], new_board[b[0]][b[1]] = new_board[b[0]][b[1]], new_board[a[0]][a[1]]  
    return new_board

#=================================================================================
# Function to calculate actual memory used by an object recursively
#=================================================================================
def total_size(obj, seen=None):
    """Recursively finds the memory footprint of a Python object including nested objects"""
    if seen is None:
        seen = set()
    size = sys.getsizeof(obj)
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(total_size(k, seen) + total_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(total_size(i, seen) for i in obj)
    return size

#=================================================================================
# Function to calculate actual space used by the algorithm
#=================================================================================
def estimate_space(board, neighbor, best_board, fixed, score_log):
    total = 0
    total += total_size(board)
    total += total_size(neighbor)
    total += total_size(best_board)
    total += total_size(fixed)
    total += total_size(score_log)
    return total

#=================================================================================
# Sudoku Solver Class using hill climbing with sideways moves and random restarts
#=================================================================================
#This function implements the hill climbing algorithm with sideways moves and random restarts
def hill_climb_sudoku(puzzle, goalBoard, N, max_steps=10000, sideways_limit=50):

    # The initial setup
    block_size = int(N ** 0.5)          # Calculate block size (2 for 4x4, 3 for 9x9)

    fixed = fixed_cells(puzzle, N)      # Create a matrix to mark fixed cells by calling fixed_cells function
    board = copy.deepcopy(puzzle)       # Copy the initial puzzle to starting board by calling copy.deepcopy function
    fill_random(board, fixed, N, block_size)   # Fill the board with random numbers in each block by calling fill_random function
    
    score = evaluate(board, N)          # Evaluate the initial board by calling evaluate function

    best_board = copy.deepcopy(board)   # Keep track of the best board found 
    best_score = score         # Keep track of the best score found 
    score_log = [score]        # Log of scores for each step
    sideways_moves = sideways_limit # counts how many times the algorithm can move to a neighbor without improving the score, 
                                    #We need sideways moves to prevent the algorithm from getting stuck on a plateau.

    neighbor = copy.deepcopy(board)  # Initialize neighbor for space calculation

    #Checking process
    
    for step in range(max_steps):
        # check if goal is reached (board matches user goalBoard) 
        if board == goalBoard:
            return board, score, step, score_log, True

        # Generate a neighbor by swapping two non-fixed cells within a block
        neighbor = randomSwapInBlock(board, fixed, N, block_size)
        neighbor_score = evaluate(neighbor, N)

        # Decide whether to move to the neighbor, stay, or restart
        if neighbor_score > score:  
            board, score = neighbor, neighbor_score
            sideways_moves = sideways_limit
        elif neighbor_score == score and sideways_moves > 0:  
            board = neighbor
            sideways_moves -= 1
        else:  
            board = copy.deepcopy(puzzle)
            fill_random(board, fixed, N, block_size)
            score = evaluate(board, N)
            sideways_moves = sideways_limit

        score_log.append(score)
        # Track the best board and score found so far
        if score > best_score:
            best_board = copy.deepcopy(board)
            best_score = score

    return best_board, best_score, max_steps, score_log, False

#This function reads the Sudoku board from user input
def read_board_from_user(size, label):
    print(f"Please enter the numbers into each row for {label} (E.g. {'1234' if size==4 else '123456789'})")
    print(f"Enter 0 for empty or missing cells")
    board = []
    for i in range(size):
        row = str(input(f"Row {i+1}: "))
        rowNumbers = [int(x) for x in row] 
        board.append(rowNumbers)
    return board

#This is the main function to run the hill climbing Sudoku solver
if __name__==("__main__"): 
    sudokuType = input("Please enter the type of Sudoku\n1. 4x4\n2. 9x9\nChoice: ")
    size = 4 if sudokuType == "1" else 9

    sudokuBoard = read_board_from_user(size, "the puzzle (initial state)")
    goalBoard = read_board_from_user(size, "the goal state")

    start = time.time()
    final_board, final_score, iterations, log, complete = hill_climb_sudoku(
        sudokuBoard, goalBoard, size, max_steps=10000, sideways_limit=50
    )
    end = time.time()

    print("\n============================================")
    print("Completed (Current Board) | Goal State:")
    for r in range(size):
        left = " ".join(str(num) for num in final_board[r])
        right = " ".join(str(num) for num in goalBoard[r])
        print(left + " | " + right)

    if complete:
        print("\nCompleteness : Complete")
    else:
        print("\nCompleteness : Not Complete")

    print(f"Expansions/Iterations (steps examined): {iterations}")
    print(f"Final Score (row+col uniqueness measure): {final_score}")
    print(f"Time Complexity (elapsed seconds): {(end-start)}")

    # Calculate actual space complexity at the very end
    memory_used = estimate_space(final_board, final_board, final_board, fixed_cells(sudokuBoard, size), log)
    print(f"Space Complexity (actual bytes used): {memory_used}")
