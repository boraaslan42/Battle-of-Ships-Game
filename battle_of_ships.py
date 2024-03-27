import os
import sys

"Bora Aslan 2220356080"
file_names = sys.argv[1:]
# takes names from terminal
existo, noexisto = [], []
f = open("Battleship.out", "w", encoding="utf8")
# Tries to open each file and raises error!
try:
    for file_name in file_names:
        if os.path.exists(file_name) is False:
            noexisto.append(file_name)
    if noexisto:
        raise IOError("IOError: input file(s) {} is/are not reachable.".format(", ".join(noexisto)))

except IOError as msg:
    print(msg)
    a = "{}".format(msg)
    f.write(a)
    quit()
except Exception:
    print("kaBOOM: run for your life!")
    f.write("kaBOOM: run for your life!\n")
    quit()
# for errors if the files are corrupted

try:
    player1txt = open("Player1.txt", "r", encoding="utf8").read().split("\n")
    player2txt = open("Player2.txt", "r", encoding="utf8").read().split("\n")
    optplayer1txt = open("OptionalPlayer1.txt", "r", encoding="utf8").read().split("\n")
    optplayer2txt = open("OptionalPlayer2.txt", "r", encoding="utf8").read().split("\n")
    player1in = open("Player1.in", "r", encoding="utf8").read()
    player2in = open("Player2.in", "r", encoding="utf8").read()
except Exception as m:
    print(m, "Try again after checking files, game over!")

    f.write(m)
    quit()
    f.write(" Try again after checking files, game over!")

    quit()

try:
    for line1, line2 in zip(player1txt, player2txt):
        if line1.count(";") != 9:
            raise IndexError(line1)
        if line2.count(";") != 9:
            raise IndexError(line2)
        for item in line1.split(";"):
            if item not in ["B", "S", "D", "C", "P", ""]:
                raise ValueError(line1)
        for item in line2.split(";"):
            if item not in ["B", "S", "D", "C", "P", ""]:
                raise ValueError(line2)
            """if item != "S" or item != "B" or item != "D" or item != "C" or item != "P" or item != "":
                print(item,"Hata")"""
except IndexError as e:
    if e.args[0] == line1:
        print("Index Error: Player1's line '{}' has more moves then it is expected".format(line1))
        f.write("Index Error: Player1's line '{}' has more moves then it is expected".format(line1))
        quit()
    if e.args[0] == line2:
        print("Index Error: Player2's line '{}' has more moves then it is expected".format(line1))
        f.write("Index Error: Player2's line '{}' has more moves then it is expected".format(line1))
        quit()
except ValueError as e:
    if e.args[0] == line1:
        print("Value Error: Player1's ship placement '{}' is not valid, fix and start the game again!".format(item))
        f.write("Value Error: Player1's ship placement '{}' is not valid, fix and start the game again!".format(item))
        quit()
    if e.args[0] == line2:
        print("Value Error: Player2's ship placement '{}' is not valid, fix and start the game again!".format(item))
        f.write("Value Error: Player2's ship placement '{}' is not valid, fix and start the game again!".format(item))
        quit()


# created because when indexing letters should be converted
# after indexing numbers should be converted to letters
def converter(var):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    if type(var) == int:
        return letters[var]
    if type(var) == str:
        return int(letters.index(var))


# CREATE TRY EXCEPTION FOR PLAYER1.TXT
player2ships, player1ships = [], []


# reads a player's input txts and creates a list to store only ships positions
def txtreader(playertxt, optplayer, lsd):
    shipC, shipD, shipS, empty = ["C1"], ["D1"], ["S1"], []
    for number, line in enumerate(playertxt):
        splitted = line.split(";")
        for letter, item in enumerate(splitted):
            place = [str(number + 1), converter(letter)]
            if item == "C":
                shipC.append(place)
            elif item == "D":
                shipD.append(place)
            elif item == "S":
                shipS.append(place)
            elif item == "":
                empty.append(place)
    lsd.append(shipD)
    lsd.append(shipS)
    lsd.append(shipC)
    for line in optplayer:
        line = line.replace(",", ";").replace(":", ";")
        parts = line.split(";")
        shipname, num, letter, direction = parts[:-1]

        if shipname[0] == "B":  # 4digits 2 ships
            temp = [shipname]
            for i in range(4):
                if direction == "down":
                    temp.append([str(int(num) + i), letter])
                else:
                    temp.append([num, converter(converter(letter) + i)])

            lsd.append(temp)

        else:
            temp = [shipname]
            for i in range(2):
                if direction == "down":
                    temp.append([str(int(num) + i), letter])
                else:
                    temp.append([num, converter(converter(letter) + i)])
            lsd.append(temp)


txtreader(player1txt, optplayer1txt, player1ships)
txtreader(player2txt, optplayer2txt, player2ships)
expected_Lengths = [4, 4, 6, 5, 5, 3, 3, 3, 3]
try:
    for index, shipss in enumerate(zip(player1ships, player2ships)):
        if len(shipss[0]) != expected_Lengths[index]:
            raise AssertionError(1)
        if len(shipss[1]) != expected_Lengths[index]:
            raise AssertionError(2)

except AssertionError as m:
    if m.args[0] == 1:
        print("AssertionError: Invalid Operation. Amount of player1's ships are wrong")
        print(1, shipss)
    if m.args[0] == 2:
        print("AssertionError: Invalid Operation. Amount of player2's ships are wrong")


# function to print out general part of every move period
def starter(ct1):
    tmp1 = "Round : {}".format(ct1).ljust(
        28) + "Grid Size: 10x10\n\n" + "Player1’s Hidden Board      Player2’s Hidden Board\n" + "  A B C D E F G H I J\t      A B C D E F G H I J"
    tmp2 = "Round : {}".format(ct1).ljust(
        28) + "Grid Size: 10x10\n\n" + "Player1’s Hidden Board      Player2’s Hidden Board\n" + "  A B C D E F G H I J\t      A B C D E F G H I J\n"
    f.write(tmp2)
    print(tmp1)


# prints ship boards of each player by getting them from matrix and adding to str
def lister(matrix1, matrix2):
    str1 = ""
    str2 = ""
    counter = 1
    for j, i in zip(matrix1, matrix2):
        if counter == 91:
            str1 += "10{}".format(matrix1[j])
            str2 += "10{}".format(matrix2[i])

        elif counter % 10 == 1:
            str1 += "{} {}".format(counter // 10 + 1, matrix1[j])
            str2 += "{} {}".format(counter // 10 + 1, matrix2[i])

        elif 10 > counter % 10 > 1:
            str1 += " {}".format(matrix1[j])
            str2 += " {}".format(matrix2[i])

        elif counter % 10 == 0:

            str1 += " {}".format(matrix1[j])
            str2 += " {}".format(matrix2[j])

            str1 += "\t    " + str2
            print(str1)
            f.write(str1 + "\n")

            str1 = ""
            str2 = ""
        counter += 1
    print("")


# prints the ships sunk or float status
# by checking the values in players dictionaries
def ships():
    f.write("\n")
    count = 0
    for i in player1ships[2][1:]:
        if M1[tuple(i)] == "X":
            count += 1
    if count == 5:

        print("Carrier\t    X".ljust(28), end="")
        f.write("Carrier\t\tX".ljust(25))
    else:
        f.write("Carrier\t\t-".ljust(25))
        print("Carrier\t    -".ljust(28), end="")
    count = 0
    for i in player2ships[2][1:]:
        if M2[tuple(i)] == "X":
            count += 1
    if count == 5:
        print("Carrier\tX")
        f.write("Carrier\t\tX\n")

    else:
        print("Carrier\t-")
        f.write("Carrier\t\t-\n")

    count1, count2 = 0, 0
    for i in player1ships[3][1:]:
        if M1[tuple(i)] == "X":
            count1 += 1
    for i in player1ships[4][1:]:
        if M1[tuple(i)] == "X":
            count2 += 1
    if count1 == 4 and count2 != 4 or count1 != 4 and count2 == 4:
        print("Battleship  X -".ljust(28), end="")
        f.write("Battleship\tX -".ljust(27))
    if count1 != 4 and count2 != 4:
        print("Battleship  - -".ljust(28), end="")
        f.write("Battleship\t- -".ljust(27))
    if count1 == 4 and count2 == 4:
        print("Battleship  X X".ljust(28), end="")
        f.write("Battleship\tX X".ljust(27))

    count1, count2 = 0, 0
    for i in player2ships[3][1:]:
        if M2[tuple(i)] == "X":
            count1 += 1
    for i in player2ships[4][1:]:
        if M2[tuple(i)] == "X":
            count2 += 1
    if count1 == 4 and count2 != 4 or count1 != 4 and count2 == 4:
        print("Battleship\tX -")
        f.write("Battleship\tX -\n")
    if count1 != 4 and count2 != 4:
        print("Battleship\t- -")
        f.write("Battleship\t- -\n")
    if count1 == 4 and count2 == 4:
        print("Battleship\tX X")
        f.write("Battleship\tX X\n")

    count = 0
    for i in player1ships[0][1:]:
        if M1[tuple(i)] == "X":
            count += 1
    if count == 3:
        print("Destroyer   X".ljust(28), end="")
        f.write("Destroyer\tX".ljust(26))
    else:
        print("Destroyer   -".ljust(28), end="")
        f.write("Destroyer\t-".ljust(26))
    count = 0
    for i in player2ships[0][1:]:
        if M2[tuple(i)] == "X":
            count += 1
    if count == 3:
        print("Destroyer\tX")
        f.write("Destroyer\tX\n")
    else:
        print("Destroyer\t-")
        f.write("Destroyer\t-\n")

    count = 0
    for i in player1ships[1][1:]:
        if M1[tuple(i)] == "X":
            count += 1
    if count == 3:
        print("Submarine   X".ljust(28), end="")
        f.write("Submarine\tX".ljust(26))
    else:
        print("Submarine   -".ljust(28), end="")
        f.write("Submarine\t-".ljust(26))
    count = 0
    for i in player2ships[1][1:]:
        if M2[tuple(i)] == "X":
            count += 1
    if count == 3:
        print("Submarine\tX")
        f.write("Submarine\tX\n")
    else:
        print("Submarine\t-")
        f.write("Submarine\t-\n")
    count1, count2, count3, count4 = 0, 0, 0, 0
    for i in player1ships[5][1:]:
        if M1[tuple(i)] == "X":
            count1 += 1
    for i in player1ships[6][1:]:
        if M1[tuple(i)] == "X":
            count2 += 1
    for i in player1ships[7][1:]:
        if M1[tuple(i)] == "X":
            count3 += 1
    for i in player1ships[8][1:]:
        if M1[tuple(i)] == "X":
            count4 += 1
    counts = [count1, count2, count3, count4]
    swims = 0
    sunk = 0
    for count in counts:
        if count == 2:
            sunk += 1
        else:
            swims += 1
    if sunk == 4:
        print("Patrol Boat X X X X".ljust(28), end="")
        f.write("Patrol Boat\tX X X X".ljust(28))
    if sunk == 3:
        print("Patrol Boat X X X -".ljust(28), end="")
        f.write("Patrol Boat\tX X X -".ljust(28))
    if sunk == 2:
        print("Patrol Boat X X - -".ljust(28), end="")
        f.write("Patrol Boat\tX X - -".ljust(28))
    if sunk == 1:
        print("Patrol Boat X - - -".ljust(28), end="")
        f.write("Patrol Boat\tX - - -".ljust(28))
    if sunk == 0:
        print("Patrol Boat - - - -".ljust(28), end="")
        f.write("Patrol Boat\t- - - -".ljust(28))
    count1, count2, count3, count4 = 0, 0, 0, 0
    for i in player2ships[5][1:]:
        if M2[tuple(i)] == "X":
            count1 += 1
    for i in player2ships[6][1:]:
        if M2[tuple(i)] == "X":
            count2 += 1
    for i in player2ships[7][1:]:
        if M2[tuple(i)] == "X":
            count3 += 1
    for i in player2ships[8][1:]:
        if M2[tuple(i)] == "X":
            count4 += 1

    counts = [count1, count2, count3, count4]
    swims = 0
    sunk = 0
    for count in counts:
        if count == 2:
            sunk += 1
        else:
            swims += 1
    if sunk == 4:
        print("Patrol Boat\tX X X X")
        f.write("Patrol Boat\tX X X X")
    if sunk == 3:
        print("Patrol Boat\tX X X -")
        f.write("Patrol Boat\tX X X -\n")
    if sunk == 2:
        print("Patrol Boat\tX X - -")
        f.write("Patrol Boat\tX X - -\n")
    if sunk == 1:
        print("Patrol Boat\tX - - -")
        f.write("Patrol Boat\tX - - -\n")
    if sunk == 0:
        print("Patrol Boat\t- - - -")
        f.write("Patrol Boat\t- - - -\n\n")


# necessary lists to check if an operand is valid
alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

# dictionaries that created to hold ships status(floating,sunk)
M2, M1 = dict(), dict()


def matrixer(dictname):
    for num in range(1, 11):
        for let in alph:
            dictname[str(num), let] = "-"


matrixer(M2)
matrixer(M1)

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]


# actual magic happens here
# this is a recursive function that calls next operands by list indexing
# inspired from recursive palindrome functions #bbm101midterm studies
# moves are played here

def moves(in1, in2, ct1=0):
    # ct is used to take a count of the rounds
    # if error is raised in return function called with mines ct1-1 because each call adds 1 to ct1
    # also if it were not called like ct-1 unvalid operands would ruin rounds
    ct1 += 1

    # if the returned list is empty print player is out of moves
    if not in1:
        print("Player1 is out of moves")
        f.write("Player1 is out of moves")
    elif not in2:
        print("Player2 is out of moves")
        f.write("Player2 is out of moves")
    # first check if the operand is valid!
    else:
        # 2,A operand to ["2","A"]
        P1moves = in1[0].split(",")
        P2moves = in2[0].split(",")
        try:
            # checking for empty and missing item operands
            if "" in P1moves or len(P1moves) == 1:
                raise IndexError(P1moves)
            if "" in P2moves or len(P2moves) == 1:
                raise IndexError(P2moves)
            # checking if first part of move operand is integer or not!
            try:
                P1moves[0] != int(P1moves[0])
            except ValueError:
                print("ValueError: operand of Player1 '{}' is invalid, Next operand will be used! \n".format(*P1moves))
                f.write(
                    "ValueError: operand of Player1 '{}' is invalid, Next operand will be used! \n".format(*P1moves))
                return moves(in1[1:], in2[:], ct1 - 1)
            try:
                P2moves[0] != int(P2moves[0])
            except ValueError:
                print("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                f.write("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                return moves(in1[:], in2[1:], ct1 - 1)
            # checking if operand is longer then expected
            if len(P1moves) != 2:
                raise ValueError(P1moves)
            if len(P2moves) != 2:
                raise ValueError(P2moves)
            # checking to see if the second part of the move is a letter or not
            if P1moves[1] not in alphabet:
                raise ValueError("C")
            if P2moves[1] not in alphabet:
                raise ValueError("D")
            # checking to see if the second part of the move is a letter which is meaningful(A,B,C,D...I,J) or not
            if P1moves[1] not in alph:
                raise AssertionError("1")
            if P2moves[1] not in alph:
                raise AssertionError("2")
            # checking to see if the first part of the move is a number which is meaningful(1,2,3,...9,10) or not

            if int(P2moves[0]) > 10 or int(P2moves[0]) < 0:
                raise AssertionError("3")
            if int(P1moves[0]) > 10 or int(P1moves[0]) < 0:
                raise AssertionError("4")

        except IndexError as e:
            if e.args[0] == P1moves:
                print("IndexError: operand of Player1 '{}' is missing arguments, Next operand will be used!\n".format(
                    *P1moves))
                f.write("IndexError: operand of Player1 '{}' is missing arguments, Next operand will be used!\n".format(
                    *P1moves))
                return moves(in1[1:], in2[:], ct1 - 1)
            if e.args[0] == P2moves:
                print("IndexError: operand of Player2 '{}' is missing arguments, Next operand will be used!\n".format(
                    *P2moves))
                f.write("IndexError: operand of Player2 '{}' is missing arguments, Next operand will be used!\n".format(
                    *P2moves))

                return moves(in1[:], in2[1:], ct1 - 1)
        except ValueError as e:
            if e.args[0] == P1moves:
                print("ValueError: operand of Player1 '{}' is invalid, Next operand will be used!\n".format(*P1moves))
                f.write("ValueError: operand of Player1 '{}' is invalid, Next operand will be used!\n".format(*P1moves))
                return moves(in1[1:], in2[:], ct1 - 1)
            if e.args[0] == P2moves:
                print("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                f.write("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                return moves(in1[:], in2[1:], ct1 - 1)
            if e.args[0] == "D":
                print("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                f.write("ValueError: operand of Player2 '{}' is invalid, Next operand will be used!\n".format(*P2moves))
                return moves(in1[:], in2[1:], ct1 - 1)
            if e.args[0] == "C":
                print("ValueError: operand of Player1 '{}' is invalid, Next operand will be used!\n".format(*P1moves))
                f.write("ValueError: operand of Player1 '{}' is invalid, Next operand will be used!\n".format(*P1moves))
                return moves(in1[1:], in2[:], ct1 - 1)
        except AssertionError as j:
            if j.args[0] == "1" or j.args[0] == "4":
                f.write("AssertionError: Invalid Operation\n")
                print("AssertionError: Invalid Operation")
                return moves(in1[1:], in2[:], ct1 - 1)
            if j.args[0] == "2" or j.args[0] == "3":
                print("AssertionError: Invalid Operation")
                f.write("AssertionError: Invalid Operation\n")
                return moves(in1[:], in2[1:], ct1 - 1)
        except Exception:
            print("kaBOOM: run for your life!")
            f.write("kaBOOM: run for your life!")
            quit()
        print("Player1's Move\n")
        f.write("Player1's Move\n\n")
        starter(ct1)
        lister(M1, M2)
        ships()
        print(" ")
        print("Enter your move: {}\n".format(",".join(P1moves)))
        f.write("Enter your move: {}\n\n".format(",".join(P1moves)))

        # register the hit | player1 hit player2
        for ship in player2ships:  # p1 hits p2 creates p2's table
            if P1moves in ship:
                dictvar = tuple(P1moves)
                M2[dictvar] = "X"
                break
            else:
                dictvar = tuple(P1moves)
                M2[dictvar] = "O"
        # print the previous hit results in table
        print("Player2's Move\n")
        f.write("Player2's Move\n\n")
        starter(ct1)
        lister(M1, M2)
        ships()

        print("\nEnter your move: {}\n".format(",".join(P2moves)))
        f.write("Enter your move: {}\n\n".format(",".join(P2moves)))

        # register the hit | player2 hit player1

        for ship in player1ships:
            dictvar = tuple(P2moves)

            # p2 hits p1 creates p1's table
            if P2moves in ship:
                M1[dictvar] = "X"
                break
            else:
                M1[dictvar] = "O"
        # round is done p2's effect will be shown in next round

        # checking the amount of each player's ship floating left to call winner function
        # if one of players ships all sunk declare who have won
        # if each has zero floating ship square left declare draw!
        count1 = 0

        for ship in player2ships:
            for sqr in ship[1:]:
                if M2[tuple(sqr)] != "X":
                    count1 += 1

        count2 = 0
        for ship in player1ships:
            for sqr in ship[1:]:
                if M1[tuple(sqr)] != "X":
                    count2 += 1

        if count1 == 0 and count2 == 0:
            a = "It is a draw!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t\t\tPlayer2’s Board\n" + "  A B C D E F G H I J\t\t  A B C D E F G H I J\n"
            b = "It is a draw!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t    Player2’s Board\n" + "  A B C D E F G H I J\t      A B C D E F G H I J"
            print(b)
            f.write(a)
            winner(M1, M2)
        elif count1 == 0:
            a = "Player1 Wins!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t\t\tPlayer2’s Board\n" + "  A B C D E F G H I J\t\t  A B C D E F G H I J\n"
            b = "Player1 Wins!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t    Player2’s Board\n" + "  A B C D E F G H I J\t      A B C D E F G H I J"
            print(b)
            f.write(a)
            winner(M1, M2)
        elif count2 == 0:
            a = "Player2 Wins!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t\t\tPlayer2’s Board\n" + "  A B C D E F G H I J\t\t  A B C D E F G H I J\n"
            b = "Player2 Wins!\n\n" + "Final Information\n\n" + "Player1’s Board\t\t    Player2’s Board\n" + "  A B C D E F G H I J\t      A B C D E F G H I J"
            print(b)
            f.write(a)
            winner(M1, M2)

        return moves(in1[1:], in2[1:], ct1)


# reveals the unsunk ships of each player to print final information
# if ones all ships sunk nothing changes in their table!
def winner(M11, M22):
    for i in M22:
        if M22[i] == "-":
            for ship in player2ships:
                if [*i] in ship:
                    M22[i] = ship[0][0]
    for i in M11:
        if M11[i] == "-":
            for ship in player1ships:
                if [*i] in ship:
                    M11[i] = ship[0][0]
    # ordinary functions to complete rest of the final information
    lister(M1, M2)
    ships()
    # quits because game ended!
    quit()


# splitting in files from ; to get each operand as an item in list for recursion
player1insplitted = player1in[:-1].split(";")
player2insplitted = player2in[:-1].split(";")
print("Battle of Ships Game\n")  # starting sentence
f.write("Battle of Ships Game\n\n")  # starting sentence
moves(player1insplitted, player2insplitted)  # calling the core function
