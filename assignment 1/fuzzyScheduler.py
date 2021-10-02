import sys
from cspProblem import CSP, Constraint
from searchGeneric import AStarSearcher
from cspConsistency import Search_with_AC_from_CSP


## extend CSP class ##
class New_CSP(CSP):
    def __init__(self,domains,constraints,soft_constraints,soft_cost):
        super().__init__(domains,constraints)
        self.soft_constraints = soft_constraints
        self.soft_cost = soft_cost

## Add heuristic function into Search_with_AC_from_CSP ##
class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self,csp):
        super().__init__(csp)
        self.cost = []
        self.soft_cons = csp.soft_constraints
        self.soft_cost = sf_cost

    def heuristic(self,node):
        List_minCost = []
        for t in node:
            if t in self.soft_cons:
                List_Cost = []
                time_exp = self.soft_cons[t]
                for v in node[t]:
                    time_act = v[1]
                    if time_act - time_exp> 0:
                        Day_Diff = time_act//12 - time_exp//12
                        Hour_Diff = time_act%12 - time_exp%12
                        Diff = Day_Diff*24 + Hour_Diff
                        Cost = Diff* self.soft_cost[t]
                        List_Cost.append(Cost)
                    else:
                        List_Cost.append(0)

                if List_Cost !=[]:
                    m = min(List_Cost)
                    List_minCost.append(m)

        sum = 0
        for i in List_minCost:
            sum += i
        cost = sum
        return cost


### Functions of binary constraint ###

def bi_before(tsk1,tsk2):
    t1_end, t2_sta = tsk1[1], tsk2[0]
    if t1_end - t2_sta <= 0:
        return True
    else:
        return False

def bi_after(tsk1,tsk2):
    t2_end, t1_sta = tsk2[1], tsk1[0]
    if t2_end - t1_sta <= 0:
        return True
    else:
        return False

def bi_sameday(tsk1,tsk2):
    t1_sta, t2_sta = tsk1[0], tsk2[0]
    if t1_sta//12 - t2_sta//12 == 0 :
        return True
    else:
        return False

def bi_startsat(tsk1,tsk2):
    t1_sta, t2_end = tsk1[0], tsk2[1]
    if t1_sta - t2_end == 0:
        return True
    else:
        return False


### Functions of hard constraint ###
# domain, <t> <day>
def hd_day(day):
    def Inner(p):
        if p[0]//12 - day==0:
            return True
        else:
            return False
    return Inner

# domain, <t> <time>
def hd_hour(hour):
    def Inner(p):
        if p[0] % 12 - hour ==0:
            return True
        else:
            return False
    return Inner

# domain, <t> starts-before <day> <time>
def hd_starts_before_dh(day,hour):
    def Inner(p):
        if hour + day*12 -p[0] >= 0:
            return True
        else:
            return False
    return Inner

# domain, <t> starts-before <time>
def hd_starts_before_h(hour):
    def Inner(p):
        if hour - p[0]%12 >= 0:
            return True
        else:
            return False
    return Inner

# domain, <t> starts-after <day> <time>
def hd_starts_after_dh(day,hour):
    def Inner(p):
        if p[0] - hour - day*12 >= 0:
            return True
        else :
            return False
    return Inner

# domain, <t> starts-after <time>
def hd_starts_after_h(hour):
    def Inner(p):
        if p[0]%12 - hour >= 0:
            return True
        else:
            return False
    return Inner

# domain, <t> ends-before <day> <time>
def hd_ends_before_dh(day,hour):
    def Inner(p):
        if day*12 + hour -p[1] >=0:
            return True
        else:
            return False
    return Inner

# domain, <t> ends-before <time>
def hd_ends_before_h(hour):
    def Inner(p):
        if hour - p[1]%12 >=0:
            return True
        else:
            return False
    return Inner

# domain, <t> ends-after <day> <time>
def hd_ends_after_dh(day,hour):
    def Inner(p):
        if p[1] - day*12 + hour >= 0:
            return True
        else:
            return False
    return Inner

# domain, <t> ends-after <time>
def hd_ends_after_h(hour):
    def Inner(p):
        if p[1]%12 - hour >= 0:
            return True
        else:
            return False
    return Inner

# domain, <t> starts-in <day> <time>-<day> <time>
def hd_starts_in(day1, day2, hour1, hour2):
    def Inner(p):
        if p[0] - day1*12 - hour1>=0 :
            if p[0] - day2*12 - hour2 <= 0:
                return True
            else:
                return False
        else:
            return False
    return Inner

# domain, <t> ends-in <day> <time>-<day> <time>
def hd_ends_in(day1, day2, hour1, hour2):
    def Inner(p):
        if p[1] -day1*12 - hour1>=0 :
            if p[1] - day2*12 -hour2 <= 0:
                return True
            else:
                return False
        else:
            return False
    return Inner

# Receive file
input_file = sys.argv[1]
dic_day = {'mon': 10, 'tue': 11, 'wed': 12, 'thu': 13, 'fri': 14}
dic_hour = {'9am': 1, '10am': 2, '11am':3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm':9}
Time_Domain = set()

# Time_Domain includes 45 numbers which represent specific time on weekday
i = 10
while i < 14:
    j = 1
    while j < 10:
        k = j + i * 12
        Time_Domain.add(k)
        j += 1
    i += 1
# Initialise Dictionary for Task_Period, Task_Domain, Soft_Constraint, Soft_Cost
Task_Period, T_Domain = {}, {}
sf_constraint, sf_cost = {}, {}
# Initialise List for Hard_Constraint
hd_constr = []

# Read file
f =  open(input_file,'r')
for l in f:
    # Remove all '\n' and ' '
    l = l.strip()
    l = l.replace(',', '')
    # Remove the first '-' in each line, eg. starts-before -> startsbefore
    l = l.replace('-','',1)
    # Split <time> and <day> in case11 and case12
    l = l.replace('-', ' ')
    # Turn String into List
    List = l.split(' ')
    Len = len(List)
    # skip comment line
    if '#' in List:
        continue
    # Receive task and duration parameters
    if 'task' in List:
        # Receive task and task duration
        T, Du= List[1], List[2]
        duration = int(Du)
        Task_Period[T] = duration
        Value, p = set(), set()
        # set Value adds Start-Time
        for i in Time_Domain:
            if i % 12 + duration - 9 <= 0:
                Value.add(i)
        # set p adds possible pairs (start-time, end-time)
        for j in Value:
            pair = (j, j + duration)
            p.add(pair)
        T_Domain[T] = p

    # Receive binary constraint requirements
    elif 'constraint' in List:
        # Receive Task name and Preposition
        Tsk1, Tsk2, Prep = List[1], List[-1], List[2]
        # hard_constraint add Constraint due to prepositions
        if Prep == 'before' :
            Constr = Constraint((Tsk1,Tsk2),bi_before)
            hd_constr.append(Constr)
        if Prep == 'after' :
            Constr = Constraint((Tsk1,Tsk2),bi_after)
            hd_constr.append(Constr)
        if Prep == 'startsat' :
            Constr = Constraint((Tsk1,Tsk2),bi_startsat)
            hd_constr.append(Constr)
        if Prep == 'sameday' :
            Constr = Constraint((Tsk1,Tsk2),bi_sameday)
            hd_constr.append(Constr)

    # Receive soft constraint requirements
    elif 'endsby' in List:
        # Receive soft constraint parameters: Task, Day, Time
        T, day, time = List[1], dic_day[List[3]], dic_hour[List[4]]
        time_cal = day*12 + time
        sf_cost[T]=int(List[-1])
        sf_constraint[T]= time_cal

    # Receive hard constraint requirements
    else:
        # Receive Task, Time, Possible_Day, Possible_Hour
        T, Time = List[1], List[2]
        Posi_Day, Posi_Hour = List[-2], List[-1]
        # Case1: domain, <t> <time>
        if Time in dic_hour:
            hour = dic_hour[Time]
            Constr = Constraint((T,), hd_hour(hour))
            hd_constr.append(Constr)

        # Case2: domain, <t> <day>
        elif Time in dic_day:
            day = dic_day[Time]
            Constr = Constraint((T,), hd_day(day))
            hd_constr.append(Constr)

        elif 'startsbefore' in List:
            # Case3: domain, <t> starts-before <day> <time>
            if Len == 5:
                day = dic_day[Posi_Day]
                hour = dic_hour[Posi_Hour]
                func = hd_starts_before_dh(day,hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)
            # Case4: domain, <t> starts-before <time>
            if Len == 4:
                hour = dic_hour[Posi_Hour]
                func = hd_starts_before_h(hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)

        elif 'startsafter' in List:
            # Case5: domain, <t> starts-after <day> <time>
            if Len == 5:
                day = dic_day[Posi_Day]
                hour = dic_hour[Posi_Hour]
                func = hd_starts_after_dh(day, hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)
            # Case6: domain, <t> starts-after <time>
            if Len == 4:
                hour = dic_hour[Posi_Hour]
                func = hd_starts_after_h(hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)

        elif 'endsbefore' in List:
            # Case7: domain, <t> ends-before <day> <time>
            if Len == 5:
                day = dic_day[Posi_Day]
                hour = dic_hour[Posi_Hour]
                func = hd_ends_before_dh(day, hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)
            # Case8: domain, <t> ends-before <time>
            if Len == 4:
                hour = dic_hour[Posi_Hour]
                func = hd_ends_before_h(hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)

        elif 'endsafter' in List:
            # Case9: domain, <t> ends-after <day> <time>
            if Len == 5:
                day = dic_day[Posi_Day]
                hour = dic_hour[Posi_Hour]
                func = hd_ends_after_dh(day, hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)
            # Case10: domain, <t> ends-after <time>
            if Len == 4:
                hour = dic_hour[Posi_Hour]
                func = hd_ends_after_h(hour)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)

        #Range between <day> <time> and <day> <time>
        else:
            # <day1> <time1> and <day2> <time2>
            d1, d2 = List[3], List[5]
            h1, h2 = List[4], List[6]
            day1, day2 = dic_day[d1], dic_day[d2]
            hour1, hour2 = dic_hour[h1], dic_hour[h2]
            # Case11: domain, <t> starts-in <day> <time>-<day> <time>
            if 'startsin' in List:
                func = hd_starts_in(day1,day2,hour1, hour2)
                Constr= Constraint((T,), func)
                hd_constr.append(Constr)
            # Case12: domain, <t> ends-in <day> <time>-<day> <time>
            elif 'endsin' in List:
                func = hd_ends_in(day1, day2, hour1, hour2)
                Constr = Constraint((T,), func)
                hd_constr.append(Constr)

# Creates CSP object
C_prob = New_CSP(T_Domain,hd_constr,sf_constraint,sf_cost)
# Creates SearchProblem
S_problem = Search_with_AC_from_Cost_CSP(C_prob)
# Creates Solution(whether it exists or not)
Solve = AStarSearcher(S_problem).search()

# if Solution exists
if Solve !=None:
    Solve = Solve.end()
    for Tsk in Solve:
        List_S = list(Solve[Tsk])
        Row = List_S[0]
        Ele = Row[0]
        for d in dic_day:
            if dic_day[d] - Ele//12 == 0:
                day = d
        for h in dic_hour:
            if dic_hour[h] - Ele%12 == 0:
                hour = h
        print(Tsk + ":" + day + " " + hour)
    Cost_Val= int(S_problem.heuristic(Solve))
    print("cost:"+ str(Cost_Val))
else:
    print('No solution')



