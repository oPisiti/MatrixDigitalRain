#!/usr/bin/python3

import os
from random import randrange, choice
import string
import sys
from time import sleep


class Globals:
    LENGTH_MIN = 7
    LENGTH_MAX = 12
    
    TEXT_COLOR = "92"
    HEAD_COLOR = "39"
    
    MIN_DISTANCE_BETWEEN_STRIPS = 5
    MAX_DISTANCE_BETWEEN_STRIPS = 9


class Strip():
    char_pool = string.ascii_letters

    def __init__(self, column: int) -> None:
        self.column = column
        self.max_length = randrange(Globals.LENGTH_MIN, Globals.LENGTH_MAX)
        self.head_pos = randrange(0, -10, -1)
        
        self.spawned_new = False
        self.spawn_new_distance = choice([i for i in range(Globals.MIN_DISTANCE_BETWEEN_STRIPS, Globals.MAX_DISTANCE_BETWEEN_STRIPS)])

    def update(self, add_list: list, remove_list: list) -> None:
        self.head_pos += 1

        if self.head_pos >= 0:
            new_char = choice(Strip.char_pool)
            add_list.append((self.head_pos, self.column, new_char))

        if self.head_pos > self.max_length:
            remove_list.append((self.head_pos - self.max_length, self.column))


def matrix():
    # Defining the valid row and column sizes
    size = os.get_terminal_size()
    row     =  size.lines
    columns = (size.columns + 1) // 2

    strips = [Strip(c) for c in [i for i in range(0, size.columns, 2)]]

    # Creating space
    print("\n" * (row - 1), end="")
    print("\033[%d;%dH" % (0, 0), end="")

    print(f"\033[{Globals.TEXT_COLOR}m", end="")
    
    # Main loop
    add_list, remove_list = [], []
    old_add_list = []
    try:
        while(True):
            pass
            # Updating the add and remove lists 
            for i in range(len(strips)): strips[i].update(add_list, remove_list)

            # ---- Printing ----
            # Adding new chars to head
            print(f"\033[{Globals.HEAD_COLOR}m", end="")
            for (r, c, char) in add_list:
                if r > row or r < 0: continue

                print("\033[%d;%dH" % (r, c), end=char)
            
            print(f"\033[{Globals.TEXT_COLOR}m", end="")

            # Removing from tail
            for (r, c) in remove_list:
                if r > row or r < 0: continue

                print("\033[%d;%dH" % (r, c), end=" ")
            
            # Setting the head char to being normal color
            for (r, c, char) in old_add_list:
                if r > row or r < 0: continue

                print("\033[%d;%dH" % (r, c), end=char)

            # ---- Deleting and spawning----
            # Marking strips for deletion and spawning
            spawn_strip_columns = []
            delete_strips_indexes = []
            for i, strip in enumerate(strips):
                strip_tail_pos = strip.head_pos - strip.max_length

                if not strip.spawned_new:
                    # Marking for spawn
                    if strip_tail_pos > 0:
                        spawn_strip_columns.append(strip.column)
                        strip.spawned_new = True

                if strip_tail_pos >= (row + 1):
                    # Marking for deletion
                    delete_strips_indexes.append(i)   

            # Spawning new strips
            for c in spawn_strip_columns:
                strips.append(Strip(c))

            # Deleting strips
            for i in range(len(delete_strips_indexes) - 1, -1, -1):
                strips.pop(delete_strips_indexes[i])

            # sleep(0.035)
            sleep(0.2)

            old_add_list = add_list.copy()
            add_list, remove_list = [], []

    except KeyboardInterrupt:
        # Cleaning up
        print("\033[%d;%dH" % (0, 0), end="")

        for r in range(row):
            print(" " * columns * 2)

        print("\033[%d;%dH" % (0, 0), end="")
        sys.exit(130)


if __name__ == '__main__':
    matrix()