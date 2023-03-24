import tkinter as tk
from tkinter import messagebox

def solve(board):
    def is_valid(num, row, col):
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row+3):
            for j in range(box_col, box_col+3):
                if board[i][j] == num:
                    return False
        return True
    
    def backtrack():
        nonlocal board
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(num, i, j):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = 0
                    return False
        return True
    backtrack()

def solve_board():
    board = [[int(entry.get()) if entry.get() else 0 for entry in row] for row in entries]
    for i in range(9):
        for j in range(9):
            if board[i][j] > 9:
                messagebox.showerror("Invalid Input", "Please enter a valid number between 0 and 9")
                return
    if is_valid_board(board):
        solve(board)
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(board[i][j]))
    else:
        messagebox.showerror("Invalid Board", "The input Sudoku board is invalid.")
    
def clear_board():
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, '0')

def is_valid_board(board):
    for i in range(9):
        row = set()
        col = set()
        box = set()
        for j in range(9):
            if board[i][j] != 0 and board[i][j] in row:
                return False
            row.add(board[i][j])
            if board[j][i] != 0 and board[j][i] in col:
                return False
            col.add(board[j][i])
            box_row = 3 * (i // 3) + j // 3
            box_col = 3 * (i % 3) + j % 3
            if board[box_row][box_col] != 0 and board[box_row][box_col] in box:
                return False
            box.add(board[box_row][box_col])
    return True

root = tk.Tk()
root.title("Sudoku Solver")

entries = []
for i in range(9):
    row = []
    for j in range(9):
        entry = tk.Entry(root, width=2, font=('Arial', 20))
        entry.grid(row=i, column=j)
        row.append(entry)
    entries.append(row)

solve_button = tk.Button(root, text="Solve", command=solve_board)
solve_button.grid(row=9, column=4)

clear_button = tk.Button(root, text="Clear", command=clear_board)
clear_button.grid(row=9, column=5)

root.mainloop()
