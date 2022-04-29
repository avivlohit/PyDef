import subprocess

# implement pip as a subprocess:
try:
    import pyautogui
except ImportError as e:
    print(e)
    ans = input("Would you like to install the external library?(pyautogui), its required! (N/n to quit)")
    if ans in ["n", "N"]:
        quit()
    else:
        subprocess.call(['pip', 'install', 'pyautogui'])
        import pyautogui
try:
    import tkinter as tk
except ImportError as e:
    print(e)
    ans = input("Would you like to install the external library?(tkinter), its required! (N/n to quit)")
    if ans in ["n", "N"]:
        quit()
    else:
        subprocess.call(['pip', 'install', 'tkinter'])
        import tkinter as tk
# import tkinter as tk

lstTmp = []



def userOrNot():
    ans = input("M/nM")
    if ans in 'M':
        user = True
    else:
        user = False
    return int(user)

def screenHW():
    root = tk.Tk()
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()

    return height, width
def main():
    height, width = screenHW()
    U = userOrNot()
    lstTmp = MouseEvent(U,height, width)
    toFile(lstTmp)

def MouseEvent(U, height, width):
    bigNum = 50**3
    while bigNum > 0:
        prev_xPos, prev_yPos = pyautogui.position()
        # time.sleep(0.000003)
        xPos, yPos = pyautogui.position()
        yPos = (yPos - height) * -1
        prev_yPos = (prev_yPos - height) * -1
        x = xPos - prev_xPos
        y = yPos - prev_yPos
        right = x > 0
        left = x < 0
        up = y > 0
        down = y < 0
        M = U
        if y == 0 and x == 0:
            continue
        if y < 0:
            y *= -1
        if x < 0:
            x *= -1
        print("U: %d,\n L: %d, Up: %d,Down: %d, R: %d,\n xMovement: %d, yMovement:%d,\n (xPos: %d, yPos: %d)\n" % (M, left, up, down, right, x, y, xPos, yPos))
        strTmp = ("%d,%d,%d,%d,%d,%d,%d,%d,%d\n" % (M, left, up, down, right, x, y, xPos, yPos))
        lstTmp.append(strTmp)
        bigNum -= 1
    return lstTmp



def toFile(lstTmp):
    try:
        with open('test1.csv', 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        data = []
        print("Creating a new csv file")
    with open('test1.csv', 'w') as f:
        if len(data) == 0:
            f.write("U:, L:, Up: %d, Down:, R:, xMovement:, yMovement:, xPos: , yPos: \n")
            f.write("".join(lstTmp))
        elif len(data) > 0:
            if data[0] not in "U:, L:, Up: %d, Down:, R:, xMovement:, yMovement:, xPos: , yPos: \n":
                f.write("U:, L:, Up: %d, Down:, R:, xMovement:, yMovement:, xPos: , yPos: \n")
            f.write("".join(data))
            f.write("".join(lstTmp))


main()
