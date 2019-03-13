#!/usr/bin/env python3
#
# There is really nice tutorial showing how ANSI escape sequences work:
# http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
#
# In a nutshell, ANSI escape sequences allow you to control how stuff is printed in terminal.
# They all start with ESC ASCII character - \u001b followed by few additional characters.

import os
import time
from random import randint

def pp(x):
    print(x, sep='', end='', flush=True)

# Simplest escape sequence is for setting colors (m) - 31 stands for red foreground color.
pp("\u001b[31m")
pp("Everything is red... ")
time.sleep(2)
# 44;1 is bright blue background color
pp("\u001b[44;1m")
pp("and the background is now blue!")
# It's a good idea to reset the colors afterwards, otherwise everything else will be colored as well.
pp("\u001b[0m")
time.sleep(2)
pp(" Yay, back to normal!")
time.sleep(5)

# Now we will simulate 2D random walk by printing character and moving cursor randomly:
try:
    # clean terminal screen
    pp("\u001b[2J")
    # hide blinking cursor
    pp("\u001b[?25l")
    cols, rows = os.get_terminal_size()
    # move cursor to the middle
    pp(f"\u001b[{rows//2};{cols//2}H")
    while True:
        # Things to experiment with:
        # overwrite last printed character by space if you don't want the trace at all
        # pp(" \u001b[1D")
        # Or keep colorful trace of the walk
        # pp("\u001b[44m \u001b[1D\u001b[0m")

        # randomly move terminal cursor
        num = randint(1, 4)
        if num == 1:
          # move cursor up by one step
          pp("\u001b[1A")
        elif num == 2:
          # move cursor down
          pp("\u001b[1B")
        elif num == 3:
          # move cursor right
          pp("\u001b[1C")
        else:
          # move cursor left
          pp("\u001b[1D")

        # print the marker (X) and move cursor one step back to original position
        pp("X\u001b[1D")
        time.sleep(0.1)
finally:
    # reset colors and show cursor
    pp('\u001b[0m\u001b[?25h')
