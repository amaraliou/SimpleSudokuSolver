from pulp import *
from random import randint
from webSudoku import SudokuBoard, SudokuScraper


class SudokuSolver:


    def __init__(self, board):
        self.Sequence = [str(i) for i in range(1, 10)]
        self.Rows = self.Sequence
        self.Cols = self.Sequence
        self.Vals = self.Sequence
        self.prob = LpProblem("Sudoku Problem", LpMinimize)
        self.choices = LpVariable.dicts("Choice", (self.Vals, self.Rows, self.Cols), 0, 1, LpInteger)
        self.Boxes = []
        self.Board = board
        for i in range(3):
            for j in range(3):
                self.Boxes += [[(self.Rows[3*i + k], self.Cols[3*j + l]) for k in range(3) for l in range(3)]]
    

    def setConstraints(self):
        for row in self.Rows:
            for col in self.Cols:
                self.prob += lpSum([self.choices[v][row][col] for v in self.Vals]) == 1, ""

        for v in self.Vals:
            for r in self.Rows:
                self.prob += lpSum([self.choices[v][r][c] for c in self.Cols]) == 1,""
        
            for c in self.Cols:
                self.prob += lpSum([self.choices[v][r][c] for r in self.Rows]) == 1,""

            for b in self.Boxes:
                self.prob += lpSum([self.choices[v][r][c] for (r,c) in b]) == 1,""
            
        for i in range(9):
            for j in range(9):
                if not self.Board[i][j] == 0:
                    self.prob += self.choices[str(self.Board[i][j])][str(i+1)][str(j+1)] == 1,""

    def solve(self):
        self.setConstraints()
        self.prob.solve()
        row = []
        solvedPuzzle = []
        for r in self.Rows:
            for c in self.Cols:
                for v in self.Vals:
                    if value(self.choices[v][r][c])==1:             
                        row.append(int(v))
                if c == '9':
                    solvedPuzzle.append(row)
                    row = []
        return solvedPuzzle

        
if __name__ == '__main__':
    puzzle = SudokuScraper(level = 4).getSudoku()
    solved = SudokuSolver(puzzle).solve()
    SudokuBoard(solved).ppBoard()