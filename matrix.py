#!/usr/bin/python3

from bisect import insort
import os
from queue import Queue
from random import randrange, choice
import string


class Strip():
    char_pool = string.ascii_letters

    def __init__(self, column: int) -> None:
        self.column = column
        self.max_length = randrange(5, 20)
        self.tail_pos = randrange(0, -10)
        
        # for _ in range(self.length):
        #     self.data.put(choice(Strip.char_pool))


    def update_queue(self, add_list: list, remove_list: list) -> None:
        self.tail_pos += 1

        new_char = choice(Strip.char_pool)
        insort(add_list, (self.tail_pos, self.column, new_char), key=lambda x:x[1])

        if self.tail_pos > self.max_length:
            insort(remove_list, (self.tail_pos, self.column), key=lambda x:x[1])


def matrix():
    # Defining the valid row and column sizes
    size = os.get_terminal_size()
    row     = size.lines // 2
    columns = size.columns // 2

    strips = [Strip(c) for c in range(columns)]

    # Main loop
    os.system("clear")
    print("\033[%d;%dH" % (10, 10), end="")
    
    # while(True):


    # print("\033[%d;%dH" % (size.lines + 1, size.columns + 1), end="")
    # print("\033[%d;%dH" % (0, 0), end="")
        


if __name__ == '__main__':
    matrix()