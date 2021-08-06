from tkinter import Frame, Label, CENTER
import random

import constants as c


def gen():
    return random.randint(0, c.GRID_LEN - 1)


def new_game(n, m):
    matrix = []
    for i in range(n):
        matrix.append([-1] * m)

    # matrix = add_two(matrix)
    # matrix = add_two(matrix)
    return matrix


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('Counter')
        self.master.bind("<Key>", self.key_down)

        self.commands = {c.KEY_UP: self.up, c.KEY_DOWN: self.down,
                         c.KEY_LEFT: self.left, c.KEY_RIGHT: self.right,
                         c.KEY_UP_ALT: self.up, c.KEY_DOWN_ALT: self.down,
                         c.KEY_LEFT_ALT: self.left, c.KEY_RIGHT_ALT: self.right,
                         c.KEY_H: self.left, c.KEY_L: self.right,
                         c.KEY_K: self.up, c.KEY_J: self.down}

        self.grid_cells = []
        self.init_grid()
        self.look_at = [0, 0]
        self.matrix = new_game(c.GRID_HEIGHT, c.GRID_WIDTH)
        self.history_matrixs = []
        self.update_grid_cells()
        self.pack(fill="both", expand=True)
        self.mainloop()

    def up(self):
        self.look_at[0] -= 1
        if self.look_at[0] < 0:
            self.look_at[0] = c.GRID_HEIGHT-1
            return True
        return False

    def down(self):
        self.look_at[0] += 1
        if self.look_at[0] >= c.GRID_HEIGHT:
            self.look_at[0] = 0
            return True
        return False

    def left(self):
        self.look_at[1] -= 1
        if self.look_at[1] < 0:
            self.look_at[1] = c.GRID_WIDTH-1
            self.up()
            return True
        return False

    def right(self):
        self.look_at[1] += 1
        if self.look_at[1] >= c.GRID_WIDTH:
            self.look_at[1] = 0
            if self.down():
                return True
            return False
        return False

    def init_grid(self):
        self.grid()
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,)
                        #    width=c.SIZE_WIDTH, height=c.SIZE_HEIGHT + (c.SIZE_HEIGHT // c.GRID_HEIGHT))
        background.grid(row=0, column=0)

        for i in range(c.GRID_WIDTH):
            cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                            #  width=2,
                            #  height=2)
                            width=c.SIZE_WIDTH / c.GRID_WIDTH,
                            height=c.SIZE_HEIGHT / c.GRID_HEIGHT)
            cell.grid(row=0, column=i, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
            t = Label(master=cell,
                      text=c.Numbers_chinese[i] ,
                      bg=c.BACKGROUND_COLOR_DICT[8],
                      fg=c.CELL_COLOR_DICT[8],
                      justify=CENTER,
                      font=c.FONT,
                      width=3,
                      height=1)
            t.grid()

        for i in range(c.GRID_HEIGHT):
            grid_row = []
            for j in range(c.GRID_WIDTH):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    #  width=2,
                    #  height=2)
                    width=c.SIZE_WIDTH / c.GRID_WIDTH,
                    height=c.SIZE_HEIGHT / c.GRID_HEIGHT)
                cell.grid(row=i+1, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                        bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                        justify=CENTER, font=c.FONT, width=3, height=1)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
        background2 = Frame(self, bg="#000000",)
                        #    width=c.SIZE_WIDTH, height=c.SIZE_HEIGHT + (c.SIZE_HEIGHT // c.GRID_HEIGHT))
        background2.grid(row=1, column=0)
        t = Label(master=background2,
                  text="退出按‘q’或者返回键")
        t.grid()

    def update_grid_cells(self):
        for i in range(c.GRID_HEIGHT):
            for j in range(c.GRID_WIDTH):
                new_number = self.matrix[i][j]
                FONT_color = c.BLUE if (i%2 == 0) else c.RED
                if i==self.look_at[0] and j == self.look_at[1]:
                    if new_number >= 0:
                        self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_DICT[2],
                                                    fg=c.CELL_COLOR_DICT[2])
                    else:
                        self.grid_cells[i][j].configure(text="...", bg=c.BACKGROUND_COLOR_DICT[2],
                                                    fg=c.CELL_COLOR_DICT[2])
                else:
                    if new_number >= 0:
                        self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                                                        fg=FONT_color)
                    else:
                        self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                # if new_number == 0:
                #     self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                # else:
                #     self.grid_cells[i][j].configure(text=str(new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                #                                     fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in c.EXITS:
            exit(0)
        # if key == c.KEY_BACK and len(self.history_matrixs) > 1:
        #     self.matrix = self.history_matrixs.pop()
        #     self.update_grid_cells()
        #     print('back on step total step:', len(self.history_matrixs))
        if key in c.NUMBERS:
            self.matrix[self.look_at[0]][self.look_at[1]] = int(key[1])
            new_one = self.commands[c.KEY_RIGHT]()
            if new_one:
                self.new_line()
        elif key in self.commands:
            self.commands[repr(event.char)]()
        elif key == c.DELETE:
            self.matrix[self.look_at[0]][self.look_at[1]] = -1
            self.left()
        self.update_grid_cells()
        # if key in self.commands:
        #     self.matrix, done = self.commands[repr(event.char)](self.matrix)
        #     if done:
        #         self.matrix = logic.add_two(self.matrix)
        #         # record last move
        #         self.history_matrixs.append(self.matrix)
        #         self.update_grid_cells()
        #         if logic.game_state(self.matrix) == 'win':
        #             self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        #             self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        #         if logic.game_state(self.matrix) == 'lose':
        #             self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
        #             self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def new_line(self):
        new_matrix = []
        for i in range(c.GRID_HEIGHT-1):
            new_matrix.append(self.matrix[i+1])
        new_matrix.append([-1] * c.GRID_WIDTH)
        self.matrix = new_matrix
        self.look_at = [c.GRID_HEIGHT-1, 0]
game_grid = GameGrid()
