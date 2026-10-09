import heapq
import time


class GBFS_Solver:
    expanded_nodes = 0
    max_frontier_size = 0

    def __init__(self, board):
        self.board = board
        self.size = len(self.board)
        self.solve()



    def Heuristic(self,board):
        return sum(row.count(0) for row in board)



    def Find_Empty_Cell(self,board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return i,j
        return None


    def GBFS_Algorithm(self):
        frontier = []
        heapq.heappush(frontier, (self.Heuristic(self.board), self.board))
        visited = set()

        key = tuple(tuple(r) for r in self.board)
        visited.add(key)


        while frontier:
            h,state = heapq.heappop(frontier)
            GBFS_Solver.expanded_nodes += 1
            GBFS_Solver.max_frontier_size = max(GBFS_Solver.max_frontier_size, len(frontier))

            
            if self.Heuristic(state) == 0:
                return state


            empty = self.Find_Empty_Cell(state)
            if not empty:
                continue
            row, col = empty


            for num in range(1, self.size + 1):
                if self.valid_moves(state, row, col, num):
                    new_state = [r[:] for r in state]
                    new_state[row][col] = num
                    key = tuple(tuple(r) for r in new_state)
                    if key not in visited:
                        visited.add(key)
                        heapq.heappush(frontier, (self.Heuristic(new_state) , new_state))

        return None

    def valid_moves(self,board,row,col,num):
        if num in board[row]:
            return False

        if num in [board[i][col] for i in range(self.size)]:
            return False


        sub_size = int(self.size ** 0.5)
        start_row, start_col = row - row % sub_size, col - col % sub_size
        for i in range(start_row, start_row + sub_size):
            for j in range(start_col, start_col + sub_size):
                if board[i][j] == num:
                    return False
        return True
                            

    
    def solve(self):
        start_time = time.time()
        solution = self.GBFS_Algorithm()
        end_time  = time.time()
        
        if solution:
            print("Goal State Reached")
            for row in solution:
                 print(row)
        else:
            print("\nIncomplete")

                
        print(f"\nTime Complexity: {end_time - start_time:.6f} seconds")
        print(f"Space Complexity: {GBFS_Solver.max_frontier_size}")
        print(f"Expanded Nodes: {GBFS_Solver.expanded_nodes}")


if __name__ == "__main__":
    
    sudokuBoard = eval(input("Enter Sudoku Board : "))
    GBFS_Solver(sudokuBoard)


#Perform well with 4*4 in terms of time but with 9*9 it will usually be incomplete.
#to make it better maybe need to put like better heruistic instead of number of remaining cells since its not a high qualitiy heuristic            
