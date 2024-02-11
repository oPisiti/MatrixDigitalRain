#!/usr/bin/python3

import argparse
import os
from random import randrange, choice
import string
import sys
from time import sleep


class Globals:
    CHAR_POOL = string.ascii_letters

    DELTA_T = 0.035

    LENGTH_MIN = 20
    LENGTH_MAX = 30
    
    TEXT_COLOR = "92"
    HEAD_COLOR = "39"
    
    MIN_DISTANCE_BETWEEN_STRIPS = 20
    MAX_DISTANCE_BETWEEN_STRIPS = 45

    MIN_INITIAL_POS = -70


class Strip():

    def __init__(self, column: int, pos: int = None) -> None:
        self.column = column
        self.max_length = randrange(Globals.LENGTH_MIN, Globals.LENGTH_MAX)
        
        if pos is None: self.head_pos = randrange(0, -10, -1)
        else:           self.head_pos = pos
        
        self.spawned_new = False
        self.spawned_new_distance = randrange(Globals.MIN_DISTANCE_BETWEEN_STRIPS, Globals.MAX_DISTANCE_BETWEEN_STRIPS)

    def update(self, add_list: list, remove_list: list) -> None:
        self.head_pos += 1

        if self.head_pos >= 0:
            new_char = choice(Globals.CHAR_POOL)
            add_list.append((self.head_pos, self.column, new_char))

        if self.head_pos > self.max_length:
            remove_list.append((self.head_pos - self.max_length, self.column))


def matrix() -> None:
    parse_arguments()

    # Defining the valid row and column sizes
    size = os.get_terminal_size()
    row     =  size.lines
    columns = (size.columns + 1) // 2

    strips = [Strip(c, randrange(Globals.MIN_INITIAL_POS, 0)) for c in [i for i in range(0, size.columns, 2)]]

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
                        spawn_strip_columns.append((strip.column, strip.spawned_new_distance))
                        strip.spawned_new = True

                if strip_tail_pos >= (row + 1):
                    # Marking for deletion
                    delete_strips_indexes.append(i)   

            # Spawning new strips
            for (c, d) in spawn_strip_columns:
                strips.append(Strip(c, -d))

            # Deleting strips
            for i in range(len(delete_strips_indexes) - 1, -1, -1):
                strips.pop(delete_strips_indexes[i])

            # Avoids staggers. https://stackoverflow.com/questions/24344992/python-3-4-time-sleep-hangs-unexpectely-when-preceeded-by-a-print-call 
            sys.stdout.flush()
            sleep(Globals.DELTA_T)

            old_add_list = add_list.copy()
            add_list, remove_list = [], []

    except KeyboardInterrupt:
        # Cleaning up
        print("\033[%d;%dH" % (0, 0), end="")

        for r in range(row):
            print(" " * (columns * 2 - 1))

        print("\033[%d;%dH" % (0, 0), end="")
        sys.exit(130)


def parse_arguments() -> None:
    # Parsing command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Sets the speed to slow", action="store_true")
    parser.add_argument("-f", help="Sets the speed to fast", action="store_true")
    parser.add_argument("-e", help="Uses the extended set of chars. Includes things like '#$%&\()' and also numbers", action="store_true")
    args = parser.parse_args()

    # Dealing with arguments
    if args.s:   Globals.DELTA_T = 0.065
    elif args.f: Globals.DELTA_T = 0.025

    if args.e:   Globals.CHAR_POOL = string.printable[:-6]


if __name__ == '__main__':
    matrix()