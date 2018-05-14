from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from webSudoku import SudokuBoard, SudokuScraper
from copy import deepcopy

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

#todo
#Implement a solve button + function
#Implement Game Checkers + levels
#Scrape Thousands of sudokus to use as a base rather than scraping every time
#implement clear single cell
#possibly implement a 'sudoku from image' function (Open CV/Tesseract)

class SudokuUI(Frame):

    def __init__(self, parent, game):
        self.game = game
        self.clear_game = deepcopy(game)
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0
        self.__initUI()
    
    def __initUI(self):
        self.parent.title("Simple Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width = WIDTH, height = HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text = "Clear Answers", command = self.__clear_answers)
        clear_button.pack(fill = BOTH, side = BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = (MARGIN + i * SIDE, MARGIN)
            y0 = (MARGIN, MARGIN + i * SIDE)
            x1 = (MARGIN + i * SIDE, WIDTH - MARGIN)
            y1 = (HEIGHT - MARGIN, MARGIN + i * SIDE)

            self.canvas.create_line(x0[0], y0[0], x1[0], y1[0], fill = color)
            self.canvas.create_line(x0[1], y0[1], x1[1], y1[1], fill = color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.clear_game[i][j]
                    color = "black" if answer == original else "blue"
                    self.canvas.create_text(x, y, text = answer, tags = "numbers", fill = color)
    
    def __clear_answers(self):
        self.game, self.clear_game = self.clear_game, deepcopy(self.clear_game)
        self.canvas.delete("victory")
        self.__draw_grid()
        self.__draw_puzzle()

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE 
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline = "red", tags = "cursor")
    
    def __key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in '1234567890':
            self.game[self.row][self.col] = int(event.char)
            print(self.game[self.row][self.col])
            print(self.clear_game[self.row][self.col])
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()

    def __draw_victory(self):
        #to fix with checkers
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32)
        )
    
if __name__ == '__main__':
    puzzle = SudokuScraper(level = 4).getSudoku()
    game = SudokuBoard(puzzle).getBoard()
    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()