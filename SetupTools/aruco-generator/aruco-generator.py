from __future__ import print_function
from toFile import *
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gui', action='store_const', const=True, default=False)

    return parser


parser = createParser()
gui = parser.parse_args().gui
if gui:
    from interface import *
    x, y, l, first, side, sep, mocap, origin, fp = waitInterface()
    first = first - 1
    firsto = first + 1
    origin = not origin
else:
    x = int(input("X: "))
    y = int(input("Y: "))
    l = int(input("Length of column: "))
    first = int(input("First: ")) - 1
    firsto = first + 1
    side = float(input("Side: "))
    sep = float(input("Sep: "))
    mocap = bool(int(input("Mocap (true = 1; false = 0): ")))
    origin = bool(int(input("Origin (local_origin = 1; local_origin_upside_down = 0): ")))
    fp = "/home/pi/catkin_ws/src/clever/clever/launch/aruco.launch"

Mx = []
My = []
O = []


for ll in range(x/l):
    for e in range(y):
        for i in range(l):
            Mx.append(first + 1)
            first += 1
        My.append(Mx)
        Mx = []
    O.append(My)
    My = []

aruco_map = ""
aruco_map += "[\n"
for e in range(len(O[0])):
    for j in range(len(O)):
        for q in O[j][e]:
            if e == len(O[0]) - 1 and j == len(O) - 1 and q == O[j][e][len(O[j][e])-1]:
                aruco_map += str(q)
            else:
                aruco_map += str(q) + ', '
    aruco_map += "\n"
aruco_map += "]"

print(aruco_map)
toFile(fp, x, y, firsto, side, sep, mocap, origin, aruco_map)
