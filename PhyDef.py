import struct
import pandas as pd
import mouse

file = open("/dev/input/mice", "rb")
lstTmp = []


def getMouseEvent(M):
    buf = file.read(3)

    '''
    button = ord(str(buf[0])[0])
    button1 = ord(str(buf[1])[0])
    down = (button & 0x4) > 0
    left = (button & 0x3) > 0
    up = (button & 0x8) > 0
    right = (button & 0x8) > 0
    
    Possition : 
    
    X -server needed

    # mouse = Controller()
    # current_mouse_position = mouse.position
    # print(current_mouse_position)
    
    
    '''

    x, y = struct.unpack("bb", buf[1:])
    down = y < 0
    left = x < 0
    up = y > 0
    right = x > 0
    print(mouse.get_position())
    xPos = mouse.get_position()[0]
    yPos = (mouse.get_position()[1] -1023) * -1
    maxYPos = 1023
    print("U: %d, R: %d, Up: %d, Down: %d, L: %d, xMovement: %d, yMovement:%d, xPos: %d, yPos: %d\n" % (M, right, up, down, left, x, y,xPos,yPos))
    strTmp = ("%d,%d,%d,%d,%d,%d,%d,%d,%d\n" % (M, right, up, down, left, x, y, xPos, yPos))
    lstTmp.append(strTmp)
    # return stuffs

    return lstTmp


def main():
    bigNum = 1000
    U = userOrNot()
    lstTmp = getMouseEvent(U)
    while bigNum > 0:
        lstTmp = getMouseEvent(U)
        bigNum -= 1
    toFile(lstTmp)
    csvFileToPd()
    file.close()


def toFile(lstTmp):
    try:
        with open('test1.csv', 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        data = []
        print("Creating a new csv file")
    with open('test1.csv', 'w') as f:
        if len(data) == 0:
            f.write("U:, R:, Up: %d, Down:, L:, xMovement:, yMovement:, xPos: , yPos: \n")
            f.write("".join(lstTmp))
        elif len(data) > 0:
            if data[0] not in "U:, R:, Up: %d, Down:, L:, xMovement:, yMovement:, xPos: , yPos: \n":
                f.write("U:, R:, Up: %d, Down:, L:, xMovement:, yMovement:, xPos: , yPos: \n")
            f.write("".join(data))
            f.write("".join(lstTmp))


def userOrNot():
    ans = input("M/nM")
    if ans in 'M':
        U = True
    else:
        U = False
    return int(U)


def csvFileToPd():
    with open('test1.csv', 'r') as f:
        df = pd.read_csv(f)
        print(df)

main()