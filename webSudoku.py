from bs4 import BeautifulSoup
from urllib2 import urlopen
import selenium

class SudokuBoard:


    def __init__(self, sudoku = [[0 for i in range(9)] for j in range(9)]):
        self.board = sudoku

    def setBoard(self, sudoku):
        self.board = sudoku
    
    def getIndexes(self):
        return [(row, col, self.board[row - 1][col - 1]) for row in range(1, 10) for col in range(1, 10)]

    def ppBoard(self):
        for row in self.board:
            print("  ".join([str(cell) for cell in row]) + '\n')

    def setCell(self, row, col, val):
        self.board[row - 1][col - 1] = val

class SudokuScraper:


    def __init__(self, level = 1):
        self.url = 'https://nine.websudoku.com/?level='
        self.level = level
        self.sudoku = []
        self.soup = BeautifulSoup(urlopen(self.url + str(self.level)), 'html.parser')
        return

    def getSudoku(self):
        for i in range(9):
            row = []
            for j in range(9):
                cell = self.soup.find('input', {'id': 'f' + str(j) + str(i)}).get('value')
                if cell:
                    row.append(int(cell))
                else:
                    row.append(0)
            self.sudoku.append(row)
        return self.sudoku