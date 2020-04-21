import mss


with mss.mss(display=":1") as sct:
    for filename in sct.save():
        print(filename)

