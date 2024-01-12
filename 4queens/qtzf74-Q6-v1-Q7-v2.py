# ---------- MODULE UPLOADING ----------

import copy

# ---------- Q4 ----------

def load_clause_set(filename):
    
    file = open(filename+'.txt', 'r')
    
    clause_set = []
    for line in file:
        li = list(line.split(' '))
        if li[0] == 'p':
            N = li[2]
            M = li[3]
        else:
            clause = []
            for l in li:
                if l[0] != '0':
                    clause.append(int(l))
            clause_set.append(clause)
    file.close()
    return clause_set, int(N), int(M)

# ---------- Q5 ----------

def truth_table(N):
    
    T = [] # list of truth assignments, or a truth table
    num = 2**N # Number of tests
    t_f = 1 # Switching between True and False between different assignments
    
    for i in range(num):
        T.append([])
        
    for i in range(1, N+1):
        
        num = num//2
        t_f = t_f*2
        count = 0
        
        for j in range(t_f):
            for k in range(num):
                T[count].append(i*((-1)**j))
                count += 1
                
    return T

def simple_sat_solve(clause_set, assignments):
    
    for i in range(len(clause_set)):
        
        neg = []
        
        for j in range(len(clause_set[i])):
            neg.append(int(clause_set[i][j])*(-1))
            
        count = 0
        
        while count < len(assignments):
            elim = True
            
            for e in neg:
                if e not in assignments[count]:
                    # print(T[count], 'remains.')
                    elim = False
            
            if elim:
                # print(T[count], 'is eliminated.')
                del assignments[count]
            else:
                count += 1
                
    if len(assignments) == 0:
        print(assignments)
        return 'Unsatisfiable.'
    else:
        print(assignments)
        return 'Satisfiable. There are '+str(len(assignments))+' assignments in total.'
    
# ---------- Q6 ----------

def branching_sat_solve(clause_set, partial_assignment = [1]):
    
    print(type(partial_assignment))
    l = partial_assignment[-1]
    print(l)
    resolvent = copy.deepcopy(clause_set)
    
    i = 0
    while i < len(resolvent):
        if l in resolvent[i]:
            print('remove',resolvent[i],'from',resolvent)
            resolvent.remove(resolvent[i])
        elif l*(-1) in resolvent[i]:
            print('remove',l*(-1),'from',resolvent[i])
            resolvent[i].remove(l*(-1))
            i += 1
        else:
            i += 1
        
    if len(resolvent) == 0:
        print('case 1')
        return 'Satisfiable under the partial assignment '+str(partial_assignment)+'.'
    elif [] in resolvent:
        if abs(l) > N:
            print('case 2.1')
            return 'Unsatisfiable.'
        elif l > 0:
            print('case 2.2')
        #    print(resolvent)
        #    print(partial_assignment)
            partial_assignment.remove(l)
            partial_assignment.append(l*(-1))
        #    print(partial_assignment)
            return branching_sat_solve(clause_set, partial_assignment)
        else:
            print('case 2.3')
            return 'Unsatisfiable.'
    else:
        print('case 3')
    #    print(resolvent)
    #    print(partial_assignment)
        partial_assignment.append(abs(l)+1)
    #    print(partial_assignment)
        return branching_sat_solve(resolvent, partial_assignment)           

# ---------- Q7 ----------

def unit_propagate(clause_set):
    
    li = [i for i in clause_set if len(i) == 1]
    up = 0
    if len(li) > 0:
        l = li[0][0]
    else:
        return clause_set
    not_l = l*(-1)
    for c in clause_set:
        if not_l in c:
            # print('remove',not_l,'from',c)
            c.remove(not_l)
            up = 1
    # print(clause_set)
    if up:
        clause_set.remove([l])
        return unit_propagate(clause_set)
    else:
        return clause_set

# ---------- MAIN PROGRAM ----------

filename = input("Enter the name of the file you would like to read: ")
print("\nQ4)\n")
print("DIMCAS format: ")
F, N, M = load_clause_set(filename)
print(F)
input("\n[PRESS ENTER TO PROCEED]")
print("\nQ5)\n")
if N < 10:
    T = truth_table(N)
    print(simple_sat_solve(F,T))
input("\n[PRESS ENTER TO PROCEED]")
print("\nQ6)\n")
print(branching_sat_solve(F))
input("\n[PRESS ENTER TO PROCEED]")
print("\nQ7)\n")
new_F = unit_propagate(F)
print("New clause-set after applying Unit Propagation:")
print(new_F)