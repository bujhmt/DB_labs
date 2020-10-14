import os
import tty
import sys
import termios

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def readChar():
    tty.setcbreak(sys.stdin)
    x = sys.stdin.read(1)[0]
    return x