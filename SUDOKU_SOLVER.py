import random
import copy

class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    
    def is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_board(self, board):
        """Solve the board using backtracking"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_board(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def fill_board(self):
        """Fill the board with a valid solution"""
        numbers = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(self.board, i, j, num):
                            self.board[i][j] = num
                            if self.check_board() or self.fill_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True
    
    def check_board(self):
        """Check if board is completely filled"""
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def remove_numbers(self, difficulty):
        """Remove numbers based on difficulty level"""
        # Difficulty levels: Easy (40-45), Medium (46-52), Hard (53-58)
        if difficulty == "Easy":
            cells_to_remove = random.randint(40, 45)
        elif difficulty == "Medium":
            cells_to_remove = random.randint(46, 52)
        else:  # Hard
            cells_to_remove = random.randint(53, 58)
        
        cells_removed = 0
        while cells_removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0
                
                # Check if puzzle still has unique solution
                board_copy = copy.deepcopy(self.board)
                if self.has_unique_solution(board_copy):
                    cells_removed += 1
                else:
                    self.board[row][col] = backup
    
    def has_unique_solution(self, board):
        """Check if the puzzle has a unique solution"""
        solutions = []
        self.count_solutions(board, solutions)
        return len(solutions) == 1
    
    def count_solutions(self, board, solutions):
        """Count the number of solutions (stop at 2 for efficiency)"""
        if len(solutions) >= 2:
            return
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            self.count_solutions(board, solutions)
                            board[i][j] = 0
                    return
        
        # If we reach here, board is complete
        solutions.append(copy.deepcopy(board))
    
    def generate_puzzle(self, difficulty="Medium"):
        """Generate a new Sudoku puzzle"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board()
        self.remove_numbers(difficulty)
        return copy.deepcopy(self.board)
    
    def get_solution(self, puzzle):
        """Get the solution for a given puzzle"""
        solution = copy.deepcopy(puzzle)
        self.solve_board(solution)
        return solution
