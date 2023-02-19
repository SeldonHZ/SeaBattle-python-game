#----------------------------------------------------------------------------------#
#  This is the code for the console game Sea Battle written in python by Alex Kap. #
#  You can play in the sea battle using python compiler on your device, or use an  #
#  online compiler, such as https://trinket.io/python3 (I recommend this service   #
#  as it supports all output symbols, but be aware that the compiler gives only    #
#  60 seconds for data entry). If you want to play with your arrangment of ships   #
#  on a virtual field, you can keep the path for the temporary input file default  #
#  or specify your path in line 18 (using the online compiler you can't play in    #
#  this mode of the game).                                                         #
#----------------------------------------------------------------------------------#

from functools import lru_cache
import random
import time
import os 

def your_temp_path() :
    default = "C:\\Usrs\\Seldon\\Desktop"  #change this path to yours using '\\' instead of '\'
    if os.path.exists(default) :
        return default  
    else : 
        return os.getcwd() #the alternative path is the folder with this file

# write_in() is used to create a temporary file into which the player enters the position of their ships
def write_in() :
    try :
        open(f'{your_temp_path()}\\temp_file.txt', "w+", encoding="utf-8").write("\
   A B C D E F G H I J\n\
 1 . . . . . . . . . .\n\
 2 . . . . . . . . . .\n\
 3 . . . . . . . . . .\n\
 4 . . . . . . . . . .\n\
 5 . . . . . . . . . .\n\
 6 . . . . . . . . . .\n\
 7 . . . . . . . . . .\n\
 8 . . . . . . . . . .\n\
 9 . . . . . . . . . .\n\
10 . . . . . . . . . .")
    except PermissionError :
        clr_txt(["Impossible to create temp_file"]); exit()

# commands that the player can use during the game
def com(word) :
    if word == "exit" : exit()
    if word == "help" : manual()

def manual() :
    while True :
        clr_txt(["What aspect of the game are you interested in?"])
        clr_blu(["",
"1 - Game essence",
"2 - Entering and placing ships",
"3 - Violation of the rules",
"q - Quit"])
        answer = input()
        if answer == "exit" : exit()
        if answer == 'q' : break
        elif answer == '1' : clr_txt([
"Sea battle is a game for two participants (in this program you will play against a computer),",
"in which players take turns announcing coordinates on a map of the enemy, on which ships are",
"previously placed. If the enemy has a ship at these coordinates, then the ship or part of it",
"is considered destroyed. If you hit or sink the ship, you can shoot again. The goal of the", 
"player is to be the first to sink all enemy ships.",
"",
"At the beginning, a player is randomly selected to go first. If this is you, then an empty",
"computer field will appear in front of you, for which you will need to enter the coordinates",
"of a point with the probable location of the ship. If you hit, the word 'HIT' will be",
"displayed and you will be given the option to enter the coordinates of another point. If the",
"ship sinks, you will see the word 'SANK' and also have the option to fire another shot. In",
"case of a miss, the word 'MISS' will be displayed and the turn will go to the opponent.",
"Conventions on the opponent's field:", ""]); clr_comp([
"· - No data",
"○ - Miss",
"◙ - Hit",
"■ - Sank", ""]); clr_txt([
"In total, this program implements three game modes: with a virtual field and random",
"arrangement, with a virtual field and your own arrangement, with your own field on a piece of",
"paper. When playing on a piece of paper, it is necessary to inform the computer about the",
"result of its shots, and when playing with a virtual field, the computer will automatically",
"read the data on its shot.",
"Conventions on your virtual field:", ""]); clr_hum([
"· - Empty cell",
"○ - Computer miss",
"◙ - Computer hit",
"■ - Intact ship",
"X - Sunken ship", ""])
        elif answer == '2' : clr_txt([
"When answering the questions of the program, you should enter '1', 'y' or 'yes' as a positive",
"answer and anything else as a negative answer.",
"",
"When playing with a field on a sheet of paper, if the computer asks for the result of its shot,",
"you should enter '0' or 'miss' if the computer missed, '1' or 'hit' if the computer hit your",
"ship and '10' or 'sank' if your ship was destroyed by the computer.",
"",
"In total, there can be only 10 ships on the field: one of 4 cells, two of 3 cells, three of 2",
"cells and four of 1 cell. Ships can only be positioned vertically and horizontally. When",
"arranging ships, it should be remembered that there must always be free space between two",
"ships (even diagonally).",
"An example of correct placement:", ""]); clr_hum([
"    A  B  C  D  E  F  G  H  I  J ",
" 1  ·  ·  ·  ·  ·  ·  ·  ■  ·  · ",
" 2  ·  ■  ■  ■  ·  ·  ·  ·  ·  · ",
" 3  ·  ·  ·  ·  ·  ■  ·  ·  ·  ■ ",
" 4  ·  ·  ■  ·  ·  ■  ·  ·  ·  ■ ",
" 5  ·  ·  ■  ·  ·  ■  ·  ·  ·  · ",
" 6  ·  ·  ·  ·  ·  ·  ·  ·  ·  · ",
" 7  ·  ·  ·  ·  ·  ·  ·  ·  ■  · ",
" 8  ■  ■  ■  ■  ·  ·  ■  ·  ·  · ",
" 9  ·  ·  ·  ·  ·  ·  ·  ·  ·  ■ ",
"10  ·  ·  ·  ·  ■  ■  ·  ·  ·  · ", ""]); clr_txt([
"Any time the computer gives you input, you can enter the following commands:",
"help - to open this manual",
"exit - to stop running the program", ""])
        elif answer == '3' : clr_txt([
"Violation of the rules by a player is possible only in the game mode with a field on a sheet",
"of paper. In this game mode, the computer checks the possibility of placing ships by the player",
"with the data that the player enters. If inconsistencies are found, the computer will end the",
"game in its favor.",
"Rule violations:",
"-Amount of ships <10 or >10",
"-Violation of 1 cell range between ships",
"-Having a ship larger than four squares in length",
"-Non-compliance with the 4-1, 3-2, 2-3, 1-4 principle for length and amount of ships",
"",
"An example of incorrect placement:", ""]); clr_hum([
"    A  B  C  D  E  F  G  H  I  J ",
" 1  ·  ·  ·  ·  ·  ·  ·  ■  ·  · ",
" 2  ·  ■  ■  ■  ·  ·  ·  ·  ·  · ",
" 3  ·  ·  ·  ·  ·  ■  ·  ·  ·  ■ ",
" 4  ·  ·  ■  ·  ·  ■  ·  ·  ·  ■ ",
" 5  ·  ·  ■  ·  ·  ■  ·  ·  ·  · ",
" 6  ·  ·  ■  ·  ·  ·  ·  ·  ·  · ",
" 7  ·  ·  ·  ·  ·  ·  ·  ·  ■  · ",
" 8  ■  ■  ■  ■  ·  ·  ■  ·  ·  · ",
" 9  ·  ·  ·  ·  ·  ·  ■  ·  ·  ■ ",
"10  ·  ·  ·  ·  ■  ■  ·  ·  ·  · ", ""]); clr_txt([
"In this case, 2 errors can be distinguished: the player did not fulfill the condition of a",
"distance of 1 cell between ships at points G9 and F10, and the player entered an invalid",
"amount of 3-cell and 1-cell ships (one 3-cell should be replaced with 1-cell).",
"",
"It should be noted that in the virtual field modes the computer checks the player's ship data",
"only for the correct placement and does not use this data to gain an advantage in the game.", ""])
        elif answer == "help" : clr_txt(["You are already in the manual"])
        else : clr_txt(["Invalid command input"])

#functions that change text color
def clr_txt(text) : #yellow
    for ln in text :
        print("\033[33m\033[40m{}".format(ln), end="")
        print("\033[0m{}".format(""))

def clr_red(text) : #red
    for ln in text :
        print("\033[31m\033[40m{}".format(ln), end="")
        print("\033[0m{}".format(""))

def clr_blu(text) : #blue
    for ln in text :
        print("\033[36m\033[40m{}".format(ln), end="")
        print("\033[0m{}".format(""))

def clr_comp(text) : #color format for computer ships
    for ln in text :
        for word in ln :
            if word == " " or word == "·" : print("\033[37m\033[40m{}".format(word), end="")
            elif word == '○' : print("\033[36m\033[40m{}".format(word), end="")
            elif word == '◙' or word == '■' : print("\033[31m\033[40m{}".format(word), end="")
            else : print("\033[33m\033[40m{}".format(word), end="")
        print("\033[0m{}".format(""))

def clr_hum(text) : #color format for player ships
    for ln in text :
        for word in ln :
            if word == " " or word == "·" : print("\033[37m\033[40m{}".format(word), end="")
            elif word == '○' or word == "■" : print("\033[36m\033[40m{}".format(word), end="")
            elif word == 'X' or word == '◙' : print("\033[31m\033[40m{}".format(word), end="")
            else : print("\033[33m\033[40m{}".format(word), end="")
        print("\033[0m{}".format(""))

def msg_clr(output) :
    global ub
    if ub < 0 : 
        if output == "HIT" or output == "SANK" : clr_red([output])
        if output == "MISS" : clr_blu([output])
        if ub == -2 or output == "MISS" :
            clr_txt(["Press ENTER to continue"])
            word = input()
            com(word)

def low2upp_case(i) :
    k = ""
    for j in i :
        if 96 < ord(j) < 123 : k += chr(ord(j) - 32)
        else : k += j
    return k

# phrases that this program can read
def yes_cnd(i) :
    i = low2upp_case(i)
    if i == "Y" or i == "YES" or i == "1" : return 1
    else : return 0

def sank_cnd(i) :
    i = low2upp_case(i)
    if (i == '10') or (i == 'SANK') : return 1
    else : return 0

def hit_cnd(i) :
    i = low2upp_case(i)
    if (i == '1') or (i == 'HIT') : return 1
    else : return 0

def mis_cnd(i) : 
    i = low2upp_case(i)
    if (i == '0') or (i == 'MISS') : return 1
    else : return 0

# The area_in, area_out and area_chk functions are needed to remove the neighbors of 
# cell number i from the array of free cells of the playing field.
def area_in(i) :
    a0 = a1 = a2 = a3 = 0; imput_file[i] = 0
    if i % 10 > 0 : imput_file[i - 1] = 0; a0 = 1
    if i > 9 : imput_file[i - 10] = 0; a1 = 1
    if i < 90 : imput_file[i + 10] = 0; a2 = 1
    if i % 10 < 9 : imput_file[i + 1] = 0; a3 = 1
    if a0 == a1 == 1 : imput_file[i - 11] = 0
    if a0 == a2 == 1 : imput_file[i + 9] = 0
    if a3 == a2 == 1 : imput_file[i + 11] = 0
    if a3 == a1 == 1 : imput_file[i - 9] = 0

def area_out(i) :
    a0 = 0; a1 = 0; a2 = 0; a3 = 0
    if i % 10 > 0 : a0 = 1
    if a0 == 1 and comp_cord_out[i - 1] == 0 : comp_cord_out[i - 1] = -1
    if i > 9 : a1 = 1
    if a1 == 1 and comp_cord_out[i - 10] == 0 : comp_cord_out[i - 10] = -1
    if i < 90 : a2 = 1
    if a2 == 1 and comp_cord_out[i + 10] == 0 : comp_cord_out[i + 10] = -1
    if i % 10 < 9 : a3 = 1
    if a3 == 1 and comp_cord_out[i + 1] == 0 : comp_cord_out[i + 1] = -1
    if a0 == 1 and a1 == 1 and comp_cord_out[i - 11] == 0 : comp_cord_out[i - 11] = -1
    if a0 == 1 and a2 == 1 and comp_cord_out[i + 9] == 0 : comp_cord_out[i + 9] = -1
    if a3 == 1 and a2 == 1 and comp_cord_out[i + 11] == 0 : comp_cord_out[i + 11] = -1
    if a3 == 1 and a1 == 1 and comp_cord_out[i - 9] == 0 : comp_cord_out[i - 9] = -1

def area_chk(y, emp_space) :
    a0 = 0; a1 = 0; a2 = 0; a3 = 0
    if y in emp_space: emp_space.remove(y)
    if y % 10 > 0: a0 = 1 
    if a0 == 1 and y - 1 in emp_space: emp_space.remove(y - 1)
    if y > 9: a1 = 1
    if a1 == 1 and y - 10 in emp_space: emp_space.remove(y - 10) 
    if y < 90: a2 = 1
    if a2 == 1 and y + 10 in emp_space: emp_space.remove(y + 10)
    if y % 10 < 9: a3 = 1
    if a3 == 1 and y + 1 in emp_space: emp_space.remove(y + 1)
    if a0 == 1 and a1 == 1 and y - 11 in emp_space: emp_space.remove(y - 11)
    if a0 == 1 and a2 == 1 and y + 9 in emp_space: emp_space.remove(y + 9)
    if a3 == 1 and a2 == 1 and y + 11 in emp_space: emp_space.remove(y + 11)
    if a3 == 1 and a1 == 1 and y - 9 in emp_space: emp_space.remove(y - 9)

def srch_cnt1(y) : #looking for cells with a possible continuation of the ship after a successful hit
    if len(lit) == y + 1 : lit.pop(y)
    if y == 1 :
        for i in [-10, 10, 1, -1] :
            if (abs(i) == 10 or lit[0] % 10 != (9 + 9*i)/2) and (lit[0] + i) in emp_space : chc_id.append(lit[0] + i)
    else :
        i = lit[0] - lit[1]
        if y == 2 : j = 0; k = 1
        else : 
            j = int(2 - abs(lit[0] - lit[2])/abs(i))
            i = int((lit[j] - lit[2])/2)
            k = 2
        if (abs(i) == 10 or lit[j] % 10 != int(9 + 9*i)/2) and (lit[j] + i) in emp_space : chc_id.append(lit[j] + i)
        if (abs(i) == 10 or lit[k] % 10 != int(9 - 9*i)/2) and (lit[k] - i) in emp_space : chc_id.append(lit[k] - i)

def srch_cnt2(y) : #selection of the cell with the highest probability of having a continuation of the ship
    global dev, gen
    lit.append(random.choice(chc_id)); dev = y
    if gen == 1 : quest()
    else : virtual()

def generation() : #randomly generates ships 
    ship = 0
    blk = 0
    while ship < 10 :
        i = random.choice(emp_space)
        direct = random.choice([1, 10])
        if ship >= 6 : cord[blk] = i; y = i; area_chk(y, emp_space); blk += 1; ship += 1
        else :
            temp = int(ship / 3) + 7 + bool(ship > 0)
            if (i % 10 < temp or direct != 1) and (i < temp*10 or direct != 10) and \
            (i + direct in emp_space) and (temp != 8 or i + 2*direct in emp_space):
                cord[blk] = i; blk += 1
                cord[blk] = i + direct; blk += 1
                if temp < 9 : cord[blk] = i + 2*direct; blk += 1
                if temp == 7 : cord[blk] = i + 3*direct; blk += 1
                for y in range(i, i + (11 - temp)*direct, direct) : area_chk(y, emp_space)
                ship += 1

def virtual() : 
    global play_input, dev, ub
    clr_txt([G0[lit[-1] % 10] + " " + str(lit[-1]//10 + 1) + "?"]) #the computer prints its guess
    if lit[-1] in player_cord : #the computer determines if the guess was successful
        Data.append(lit[-1])
        play_cord_out[lit[-1]] = -2
        s1[0] = sum([play_cord_out[player_cord[0]], play_cord_out[player_cord[1]], play_cord_out[player_cord[2]], play_cord_out[player_cord[3]]])
        for y in range(1, 3) : s1[y] = sum([play_cord_out[player_cord[3*y + 1]], play_cord_out[player_cord[3*y + 2]], play_cord_out[player_cord[3*y + 3]]])
        for y in range(3, 6) : s1[y] = sum([play_cord_out[player_cord[2*y + 4]], play_cord_out[player_cord[2*y + 5]]])
        for y in range(6, 10) : s1[y] = play_cord_out[player_cord[y + 10]]
        for y in range(10) :
            if s1[y] == -2*bool(y < 1) - 2*bool(y < 3) - 2*bool(y < 6) - 2*bool(y < 10) :
                play_input = "SANK"
                num[dev] = num[dev] - 1
                play_cord_out[player_cord[y*bool(y < 3) + y*bool(y < 6) + y + bool(y > 0) + 3*bool(y > 2) + 6*bool(y > 5)]] = -3
                if y < 6 : play_cord_out[player_cord[y*bool(y < 3) + y*bool(y < 6) + y + bool(y > 0) + 3*bool(y > 2) + 6*bool(y > 5) + 1]] = -3
                if y < 3 : play_cord_out[player_cord[y*bool(y < 3) + y*bool(y < 6) + y + bool(y > 0) + 3*bool(y > 2) + 6*bool(y > 5) + 2]] = -3
                if y < 1 : play_cord_out[player_cord[y*bool(y < 3) + y*bool(y < 6) + y + bool(y > 0) + 3*bool(y > 2) + 6*bool(y > 5) + 3]] = -3
                break
        else : play_input = "HIT"
    else :
        play_input = "MISS" 
        play_cord_out[lit[-1]] = -1

    TD_array = [[0] * 11 for i in range(11)]; h = 0
    clr_txt(["----------[YOUR FIELD]----------"])
    for i in range(11): #the computer prints out the result of its shot and the player's field
        for j in range(11):
            TD_array[i][j] = "·"
            if i > 0 and j != 0: 
                if play_cord_out[h] == 1: TD_array[i][j] = "■"
                if play_cord_out[h] == -1: TD_array[i][j] = "○"
                if play_cord_out[h] == -2: TD_array[i][j] = "◙"
                if play_cord_out[h] == -3: TD_array[i][j] = "X"
                h += 1
            if i == 0 and j != 0 : TD_array[i][j] = colum[j - 1]
            if j == 0 and i != 0 : TD_array[i][j] = lines[i - 1]
            if i == 0 and j == 0 : TD_array[i][j] = " "
    for row in TD_array: clr_hum(['  '.join([str(elem) for elem in row])])
    ub = -2
    msg_clr(play_input)

def quest():
    global dev, play_input
    clr_txt([G0[lit[-1] % 10] + " " + str(lit[-1]//10 + 1) + "?"]) #the computer prints its guess
    while True :
        clr_txt(["Enter data correctly"])
        play_input = input() #the player must answer if the guess is successful
        com(play_input)
        if mis_cnd(play_input) + sank_cnd(play_input) + hit_cnd(play_input) > 0 : break
        else : clr_txt(["You must enter miss (0), hit (1) or sank (10)"])
    if sank_cnd(play_input) + hit_cnd(play_input) > 0 :
        Data.append(lit[-1])
        if sank_cnd(play_input) : num[dev] = num[dev] - 1

def out() : #prints the computer game field
    TD_array = [[0] * 11 for i in range(11)]; h = 0
    clr_txt(["--------[COMPUTER FIELD]--------"])
    for i in range(11):
        for j in range(11):
            TD_array[i][j] = "·"
            if i > 0 and j != 0: 
                if comp_cord_out[h] == -1: TD_array[i][j] = "○"
                if comp_cord_out[h] == -2: TD_array[i][j] = "◙"
                if comp_cord_out[h] == -3: TD_array[i][j] = "■"
                h += 1
            if i == 0 and j != 0 : TD_array[i][j] = colum[j - 1]
            if j == 0 and i != 0 : TD_array[i][j] = lines[i - 1]
            if i == 0 and j == 0 : TD_array[i][j] = " "
    for row in TD_array: clr_comp(['  '.join([str(elem) for elem in row])])

def inp() :
    global output, dest_by_hum, win, ub
    while True :
        clr_txt(["Enter data correctly"])
        inp_let = input() #the player guesses ship location
        com(inp_let)
        inp_num = ''.join(x for x in inp_let if x.isdigit())
        if len(inp_let) != 0 : inp_let = inp_let[0]
        if len(inp_let) != 0 and 96 < ord(inp_let) < 123 : inp_let = chr(ord(inp_let) - 32)
        if (inp_num == "10" and len(inp_let) == 1 and (64 < ord(inp_let) < 75)) or ((len(inp_num) == len(inp_let) == 1) and \
            (48 < ord(inp_num) < 58) and (64 < ord(inp_let) < 75)) : break
        else : clr_txt(["The data must be entered in the format of a letter and a number (for example A8 or a 8)"])
    inp_let = chr(ord(inp_let) - 17)
    output = "MISS"; ub = int(inp_num + inp_let) - 10; d1 = [0]*10
    if comp_cord_out[ub] < 0 : clr_txt(["There is no point in shooting that cell"]); output = "SANK"
    elif ub in cord : 
        comp_cord_out[ub] = -2
        output = "HIT"
        ub = -1
        d1[0] = sum([comp_cord_out[cord[0]], comp_cord_out[cord[1]], comp_cord_out[cord[2]], comp_cord_out[cord[3]]])
        for x in range(1, 3) : d1[x] = sum([comp_cord_out[cord[3*x + 1]], comp_cord_out[cord[3*x + 2]], comp_cord_out[cord[3*x + 3]]])
        for x in range(3, 6) : d1[x] = sum([comp_cord_out[cord[2*x + 4]], comp_cord_out[cord[2*x + 5]]])
        for x in range(6, 10) : d1[x] = comp_cord_out[cord[x + 10]]
        for x in range(10) : 
            if d1[x] == -2*bool(x < 1) - 2*bool(x < 3) - 2*bool(x < 6) - 2*bool(x < 10) : 
                output = "SANK"
                comp_cord_out[cord[x*bool(x < 3) + x*bool(x < 6) + x + bool(x > 0) + 3*bool(x > 2) + 6*bool(x > 5)]] = -3
                if x < 6 : comp_cord_out[cord[x*bool(x < 3) + x*bool(x < 6) + x + bool(x > 0) + 3*bool(x > 2) + 6*bool(x > 5) + 1]] = -3
                if x < 3 : comp_cord_out[cord[x*bool(x < 3) + x*bool(x < 6) + x + bool(x > 0) + 3*bool(x > 2) + 6*bool(x > 5) + 2]] = -3
                if x < 1 : comp_cord_out[cord[x*bool(x < 3) + x*bool(x < 6) + x + bool(x > 0) + 3*bool(x > 2) + 6*bool(x > 5) + 3]] = -3
                dest_by_hum += 1
                if dest_by_hum == 10 : win = 1
                break
    else :
        output = "MISS"
        comp_cord_out[ub] = -1
        ub = -1
    for i in cord : 
        if comp_cord_out[i] == -3 : area_out(i)

@lru_cache(maxsize=8192)
def check(mes, num) : #checks if ships can be placed in free cells (if the player is cheating)
    global anti_cheat
    mes = list(mes); num = list(num)
    for i in mes :
        num_copy = num.copy(); emp_space = mes.copy()
        if num_copy[3] == 1 : temp = 7
        elif num_copy[2] > 0 : temp = 8
        elif num_copy[1] > 0 : temp = 9
        elif num_copy[0] > 0 : temp = 10
        for di in [1, 10] :
            if (i % 10 < temp or di == 10) and (i < temp*10 or di == 1) and (temp > 9 or i + di in emp_space) \
            and (temp > 8 or i + 2*di in emp_space) and (temp != 7 or i + 3*di in emp_space) :
                for y in range(i, i + (11 - temp)*di, di) : area_chk(y, emp_space)
                num_copy[10 - temp] -= 1
                if num_copy == [0, 0, 0, 0] : anti_cheat = 1; return
                else : check(tuple(emp_space.copy()), tuple(num_copy.copy()))
                num_copy = num.copy(); emp_space = mes.copy()
                if anti_cheat == 1 : return

def gamemode2() : #provides the player with randomly generated ship placements
    global player_cord, emp_space, cord
    while True :
        clr_txt(["Would you like to use this ship placement?", ""])
        cord = [-1]*20
        emp_space = list(range(100))
        generation()
        colum = [" A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        lines = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10"]
        TD_array = [[0] * 11 for i in range(11)]
        for i in range(11):
            for j in range(11):
                TD_array[i][j] = "·"
                if i > 0 and j != 0: 
                    if (i - 1)*10 + j - 1 in cord: TD_array[i][j] = "■"
                if i == 0 and j != 0 : TD_array[i][j] = colum[j - 1]
                if j == 0 and i != 0 : TD_array[i][j] = lines[i - 1]
                if i == 0 and j == 0 : TD_array[i][j] = " "
        for row in TD_array: clr_hum(['  '.join([str(elem) for elem in row])])
        print() 
        ans = input()
        com(ans)
        if yes_cnd(ans) : break
    player_cord = cord.copy()

def gamemode3() : #allows the player to create their own virtual ship placements
    global player_cord, imput_file, gen
    write_in()
    empty_file = open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read()
    ini_file = []
    for i in open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read().split("\n"):
        for j in i.split(" "): ini_file.append(list(map(lambda y: y, j.split(" "))))
    imput_error = 1
    while imput_error > 0 :
        if imput_error != 3 : clr_txt(["Enter ship data", "replace dots with X for your ships"])
        if imput_error == 2 : write_in()
        empty_file = open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read()
        os.system(fr'{your_temp_path()}\\temp_file.txt')
        imput_file = open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read()
        imput_error = 1  
        if empty_file == imput_file : 
            clr_txt(["You have not changed the file"])
            os.remove(f'{your_temp_path()}\\temp_file.txt')
            exit()
        else :
            empty_file = []
            for i in open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read().split("\n"):
                for j in i.split(" "): empty_file.append(list(map(lambda y: y, j.replace("X",".").split(" "))))
            if empty_file != ini_file : clr_txt(["Invalid format"]); imput_error = 2
            else:
                empty_file = []; imput_file = []; count = 0; num = [0, 0, 0, 0]
                for i in open(f'{your_temp_path()}\\temp_file.txt', "r", encoding="utf-8").read().split("\n"):
                    for j in i.split(" "): empty_file.append(list(map(lambda y: y, j.split(" "))))
                for i in empty_file :
                    if i == ['.'] : imput_file.append(0)
                    if i == ['X'] : imput_file.append(1); count += 1
                player_cord = [] 
                for temp in range(7, 11) :
                    for y in range(100) : 
                        for di in [1, 10] :
                            if (y % 10 < temp or di == 10) and (y < temp*10 or di == 1) and (imput_file[y] == 1) and \
                            (temp > 9 or imput_file[y + di] == 1) and (temp > 8 or imput_file[y + 2*di] == 1) and \
                            (temp != 7 or imput_file[y + 3*di] == 1) :
                                for i in range(y, y + (11 - temp)*di, di): area_in(i)
                                if temp == 7 : num[3] += 1; player_cord += [y, y + di, y + 2*di, y + 3*di]
                                if temp == 8 : num[2] += 1; player_cord += [y, y + di, y + 2*di]
                                if temp == 9 : num[1] += 1; player_cord += [y, y + di]
                                if temp == 10 : num[0] += 1; player_cord += [y]
                if num == [4, 3, 2, 1] and count == 20 : clr_txt(["Your ships are placed"]); imput_error = 0
                else : clr_txt(["Invalid placement of ships"]); imput_error = 3
    os.remove(f'{your_temp_path()}\\temp_file.txt')

def comp_win() : #the computer displays the location of their ships if the player loses
    TD_array = [[0] * 11 for i in range(11)]; h = 0
    for i in range(11):
        for j in range(11):
            TD_array[i][j] = "·"
            if i > 0 and j != 0: 
                for ij in cord : 
                    if ij == h: TD_array[i][j] = "■"
                h += 1
            if i == 0 and j != 0 : TD_array[i][j] = colum[j - 1]
            if j == 0 and i != 0 : TD_array[i][j] = lines[i - 1]
            if i == 0 and j == 0 : TD_array[i][j] = " "
    for row in TD_array: clr_comp(['  '.join([str(elem) for elem in row])])

def hum_frst_mv() : #used if player goes first
    global frst_mv, dest_by_hum, output
    clr_txt(["<<YOUR TURN>>", "--------[COMPUTER FIELD]--------"])
    TD_array = [[0] * 11 for i in range(11)] 
    for i in range(11):
        for j in range(11):
            TD_array[i][j] = "·"
            if i == 0 : TD_array[i][j] = colum[j - 1]
            if j == 0 : TD_array[i][j] = lines[i - 1]
            if i == 0 and j == 0 : TD_array[i][j] = " "
    for row in TD_array: clr_hum(['  '.join([str(elem) for elem in row])])
    while output == "HIT" or output == "SANK" :
        if frst_mv == 2 : clr_txt(["<<YOUR TURN>>"])
        inp()
        if dest_by_hum == 10 : break
        out(); msg_clr(output); frst_mv = 2

def bgn_qstns() : 
    global gen
    clr_txt(["Are you familiar with the rules of the game? (y/n)"])
    rules = input()
    com(rules)
    if yes_cnd(rules) == 0 : manual()
    while True :
        clr_txt(["Ways to arrange your ships:", ""]); clr_blu([
"1 - On a piece of paper",
"2 - Virtual field with random generation",
"3 - Virtual field with your own placement"])
        gen = input()
        com(gen)
        if gen == '1' or gen == '2' or gen == '3' : gen = int(gen); break
        elif gen != "help" : clr_txt(["Invalid command input"])

def main() :
    global colum, G0, lines, cord, comp_cord_out, play_cord_out, s1, lit, chc_prb, result, ub,\
    chc_id, Data, dev, num, dest_by_hum, dest_by_comp, win, gen, output, frst_mv, imput_file, emp_space, \
    player_cord, anti_cheat, play_input
    win = 1
    clr_txt(["Do you want to start the game? (y/n)"])
    play_input = input()
    com(play_input)
    if yes_cnd(play_input) : win = 0
    while win == 0 :
        bgn_qstns()                  #the player generates their ships
        if gen == 3 : gamemode3()
        if gen == 2 : gamemode2()
        cord = [-1]*20
        emp_space = list(range(100)) #one-dimensional array with cell coordinates
        generation()                 #the computer generates its ships
        colum = [" A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        G0 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        lines = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10"]
        Data = []                    #the coordinates of the ships that the computer found
        misData = []                 #the coordinates of empty cells that the computer fired at
        num = [4, 3, 2, 1]           #types of player ships that were not found (and amount)
        dest_by_comp = 0             #the number of ships that the computer destroyed
        dest_by_hum = 0              #the number of ships that the player destroyed
        prog = 0
        output = "SANK"
        comp_cord_out = [0]*100
        play_cord_out = [0]*100
        s1 = [0]*10
        if gen == 1 : player_cord = []
        for y in player_cord : play_cord_out[y] = 1
        frst_mv = random.randint(0, 1)

        frst_mv = 1

        if frst_mv == 0 :
            clr_txt(["You go first"])
            hum_frst_mv()
        if frst_mv == 1 or frst_mv == 2 :
            if frst_mv == 1 : clr_txt(["Computer goes first"])
            while win == 0 :
                anti_cheat = 1; play_input = "SANK"
                while sank_cnd(play_input) : #computer move
                    if prog == 0 :
                        clr_txt(["<<COMPUTER TURN>>"])
                        lit = [0]; result = [0]*100; emp_space = list(range(100))
                        for i in Data : #computer updates its information
                            area_chk(i, emp_space)
                        for i in misData : 
                            if i in emp_space : emp_space.remove(i)  
                        lit[0] = random.choice(emp_space) #chooses random cell 
                        dev = 0
                        if gen == 1 : quest()
                        else : virtual()
                        if num[0] < 0 : anti_cheat = 0; break
                    if hit_cnd(play_input) or prog > 0 :
                        if prog < 2 : #if the previous shot hit the ship, selects the adjacent cell with the highest probability
                            clr_txt(["<<COMPUTER TURN>>"])
                            if num[1] + num[2] + num[3] == 0 : anti_cheat = 0; break
                            prog = 1; chc_id = []
                            srch_cnt1(prog)
                            if chc_id == [] : anti_cheat = 0; break
                            srch_cnt2(prog)
                            if num[1] < 0 : anti_cheat = 0; break
                        if hit_cnd(play_input) or prog > 1 :
                            if prog < 3 : 
                                clr_txt(["<<COMPUTER TURN>>"])
                                if num[2] + num[3] == 0 : anti_cheat = 0; break
                                prog = 2; chc_id = []
                                srch_cnt1(prog)
                                if chc_id == [] : anti_cheat = 0; break
                                srch_cnt2(prog)
                                if num[2] < 0 : anti_cheat = 0; break
                            if hit_cnd(play_input) or prog > 2 :
                                clr_txt(["<<COMPUTER TURN>>"])
                                if num[3] == 0 : anti_cheat = 0; break
                                prog = 3; chc_id = []
                                srch_cnt1(prog)
                                if chc_id == [] : anti_cheat = 0; break
                                srch_cnt2(prog)
                                if num[3] < 0 : anti_cheat = 0; break
                                if hit_cnd(play_input) : anti_cheat = 0; break
                    if mis_cnd(play_input) : misData.append(lit[-1]); emp_space.remove(lit[-1])
                    if sank_cnd(play_input) :
                        prog = 0; dest_by_comp += 1
                        if dest_by_comp == 10 : win = 1; break
                    if gen == 1 :
                        anti_cheat = 0 #checks if the player is cheating
                        check(tuple(emp_space), tuple(num))
                        check.cache_clear()
                    if anti_cheat == 0 : break
                if anti_cheat == 0 : clr_txt(["You violated the rules, game over."]); dest_by_comp = 10; win = 1
                #if win == 0 :
                #    output = "SANK" #player move
                #    clr_txt(["<<YOUR TURN>>"])
                #    out()
                #    while output == "HIT" or output == "SANK" :
                #        inp(); out(); msg_clr(output)
                #        if dest_by_hum == 10 : break
                #        if output == "HIT" or output == "SANK" : clr_txt(["<<YOUR TURN>>"])
            if dest_by_hum == 10 : clr_txt(["Congratulations, you win!"])
            if dest_by_comp == 10 :
                clr_txt(["Computer wins", "Location of computer ships"])
                comp_win()
            clr_txt(["Play again?"]); play_input = input()
            com(play_input)
            if yes_cnd(play_input) : win = 0

if __name__ == '__main__' : #this file should be run as a script 
    main()