import sys
import numpy as np

def checkUsage(arg):
    if arg == "-h" or arg == "--help":
        print("USAGE:\t./304pacman file c1 c2\n\tfile\tfile describing the board, using the following characters:\n\t\t\t'0' for an empty square,\n\t\t\t'1' for a wall,\n\t\t\t'F' for the ghost's position,\n\t\t\t'P' for Pacman's position.\n\tc1\tcharacter to display for a wall\n\tc2\tcharacter to display for an empty space.")
        sys.exit(0)

def checkArgs(args):
    if len(args) != 3:
        print("Invalid number of arguments. Try ./304pacman -h for usage")
        sys.exit(84)
    if len(args[1]) != 1 or len(args[2]) != 1:
        print("Arguments c1 and c2 must be a single characters. Try ./304pacman -h for usage")
        sys.exit(84)

def parseFile(fileName):
    fd = open(fileName, 'r')
    data = fd.read()
    map = data.split('\n')
    if len(map[-1]) == 0:
        map.pop()
    mapLength = len(map[0])
    ghostCount = 0
    pacmanCount = 0
    for y in map:
        if len(y) != mapLength:
            print("file must contains an equal number of characters on each lines. Try ./304pacman -h for usage")
            sys.exit(84)
        for x in y:
            if x != '1' and x != '0' and x != 'F' and x != 'P':
                print("file must only contains 1, 0, F or P characters. Try ./304pacman -h for usage")
                sys.exit(84)
            if x == 'F':
                ghostCount += 1
            elif x == 'P':
                pacmanCount += 1
    if ghostCount != 1 or pacmanCount != 1:
        print("file must contains exactly one P and one F characters. Try ./304pacman -h for usage")
        sys.exit(84)
    return map

def parse(args):
    if len(args) == 1:
        checkUsage(args[0])
    checkArgs(args)
    map = parseFile(args[0])
    return [map, args[1], args[2]]