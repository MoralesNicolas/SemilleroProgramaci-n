
while True:
    try:
        x = int(input(""))
        y= int(input(""))
        c =x*y
        print(c)
        break
    except ValueError as e:
        print(e.args[0])