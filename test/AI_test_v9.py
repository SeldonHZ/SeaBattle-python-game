#----------------------------------------------------------------------------------#
#  This is the script to calculate average amount of shots it takes for AI to win. #
#  It does it through running several games and you can adjust amount of games in  #
#  line 151 to decrease calculation time or increase accuracy. This is test of Sea #
#  Battle v9 and awerage result for this test is 55.2 shots. I use such programs   #
#  to determine wether new AI version is more efficient with new features or not.  #
#----------------------------------------------------------------------------------#

import random
from functools import lru_cache
import time
# phrases that this program can read
def yes_cnd(i) :
    if i == "Y" or i == "YES" or i == "1" : return 1
    else : return 0

def sank_cnd(i) :
    if (i == '10') or (i == 'SANK') : return 1
    else : return 0

def hit_cnd(i) :
    if (i == '1') or (i == 'HIT') : return 1
    else : return 0

def mis_cnd(i) : 
    if (i == '0') or (i == 'MISS') : return 1
    else : return 0

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

def area_amount(y) :
    weight = 1
    a0 = 0; a1 = 0; a2 = 0; a3 = 0
    if y % 10 > 0: a0 = 1 
    if a0 == 1 and y - 1 in emp_space: weight += 1
    if y > 9: a1 = 1
    if a1 == 1 and y - 10 in emp_space: weight += 1 
    if y < 90: a2 = 1
    if a2 == 1 and y + 10 in emp_space: weight += 1
    if y % 10 < 9: a3 = 1
    if a3 == 1 and y + 1 in emp_space: weight += 1
    if a0 == 1 and a1 == 1 and y - 11 in emp_space: weight += 1
    if a0 == 1 and a2 == 1 and y + 9 in emp_space: weight += 1
    if a3 == 1 and a2 == 1 and y + 11 in emp_space: weight += 1
    if a3 == 1 and a1 == 1 and y - 9 in emp_space: weight += 1
    return weight

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
    global dev
    for i in chc_id : chc_prb.append(result[i])
    lit.append(max(chc_prb)); lit[y] = chc_id[chc_prb.index(lit[y])]; dev = y
    virtual()

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
    global play_input, dev
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

def gen_adv(mes, num, aim) : #generates ships to find a cell with the highest probability of having a ship 
    global aim_out, error
    for err in range(error) :
        num_copy = num.copy(); emp_space = mes.copy(); aim_copy = aim.copy()
        i = random.choice(emp_space)
        di = random.choice([1, 10])
        if num_copy[3] == 1 : temp = 7
        elif num_copy[2] > 0 : temp = 8
        elif num_copy[1] > 0 : temp = 9
        elif num_copy[0] > 0 : temp = 10
        if (i % 10 < temp or di == 10) and (i < temp*10 or di == 1) and (temp > 9 or i + di in emp_space) \
         and (temp > 8 or i + 2*di in emp_space) and (temp != 7 or i + 3*di in emp_space) :
            aim_copy.append(i)
            if temp < 10 : aim_copy.append(i + di)
            if temp < 9 : aim_copy.append(i + 2*di)
            if temp == 7 : aim_copy.append(i + 3*di)
            for y in range(i, i + (11 - temp)*di, di) : area_chk(y, emp_space)
            num_copy[10 - temp] -= 1
            if num_copy == [0, 0, 0, 0] : aim_out = aim_copy.copy(); return
            elif emp_space != [] : gen_adv(emp_space.copy(), num_copy.copy(), aim_copy.copy())
            else : return
        if aim_out != [] : return

def main() : 
    global cord, play_cord_out, s1, lit, chc_prb, result,\
    chc_id, Data, dev, num, dest_by_comp, win, output, emp_space, \
    player_cord, play_input, error, aim_out
    cycle = 1000 #amount of test cycles: the bigger amount --> the more accuracy is and the more time it will take to cuclulate result
    cyc = 0
    summation = 0
    mini = 100
    maxi = 0
    while cyc < cycle :
        sm = 0
        win = 0
        cord = [-1]*20
        emp_space = list(range(100)) #one-dimensional array with cell coordinates
        generation()                 #the computer generates its ships
        player_cord = cord.copy()
        Data = []                    #the coordinates of the ships that the computer found
        misData = []                 #the coordinates of empty cells that the computer fired at
        num = [4, 3, 2, 1]           #types of player ships that were not found (and amount)
        dest_by_comp = 0             #the number of ships that the computer destroyed
        prog = 0
        output = "SANK"
        play_cord_out = [0]*100
        for y in player_cord : play_cord_out[y] = 1
        s1 = [0]*10
        while win == 0 :
            play_input = "SANK"    
            while sank_cnd(play_input) : #computer move
                if prog == 0 :
                    #this is the "brain" module
                    #---------------------------------------#
                    lit = [0]; emp_space = list(range(100))
                    for i in Data : #computer updates its information
                        area_chk(i, emp_space)
                    for i in misData : 
                        if i in emp_space : emp_space.remove(i)  
                    result = [0]*100
                    ayin = 0
                    accuracy = 200
                    error = 3
                    stime = time.time() 
                    while ayin < accuracy : #generates ships in free cells to calculate the probability of finding a ship for each cell
                        aim = []; aim_out = []
                        gen_adv(emp_space.copy(), num, aim)
                        if aim_out != [] : 
                            ayin += 1
                            for i in aim_out : result[i] += 1
                        etime = time.time()
                        if etime - stime > 1 and max(result) > 2 : break
                        if etime - stime > 1 and max(result) <= 2 : stime = time.time(); error += 5
                    lit[0] = result.index(max(result)) #chooses cell with the highest probability
                    #---------------------------------------#
                    dev = 0
                    virtual()
                if hit_cnd(play_input) or prog > 0 :
                    if prog < 2 : #if the previous shot hit the ship, selects the adjacent cell with the highest probability
                        prog = 1; chc_id = []; chc_prb = []
                        srch_cnt1(prog)
                        srch_cnt2(prog)
                    if hit_cnd(play_input) or prog > 1 :
                        if prog < 3 : 
                            prog = 2; chc_id = []; chc_prb = []
                            srch_cnt1(prog)
                            srch_cnt2(prog)
                        if hit_cnd(play_input) or prog > 2 :
                            prog = 3; chc_id = []; chc_prb = []
                            srch_cnt1(prog)
                            srch_cnt2(prog)
                if mis_cnd(play_input) : misData.append(lit[-1]); emp_space.remove(lit[-1]); summation += 1; sm += 1
                if sank_cnd(play_input) :
                    prog = 0; dest_by_comp += 1
                    if dest_by_comp == 10 : win = 1; break
        cyc += 1
        mini = min(mini, sm)
        maxi = max(maxi, sm)  
    print("Amount of shots for this AI to win")
    print("Average:",summation/cyc + 20,"Minimum:",mini + 20, "Maximum:",maxi + 20, sep = " ")

if __name__ == '__main__' : #this file should be run as a script 
    main()
