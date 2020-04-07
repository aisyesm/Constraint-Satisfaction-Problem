#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    
    ourCSP = CSP("Futushiki")

    dim = len(futo_grid)
    full_domain = []

    for i in range(1,dim+1):
        full_domain.append(i)
    
    var_array = [full_domain[:] for i in range(1,dim+1)]

    found_sign = False
    sign = ''

    for i, row in enumerate(futo_grid):
        for j, col in enumerate(row):
            if j%2 == 0:
                if int(j/2) == 0:
                    found_sign = False                          #for the last cell in row
                if col == 0:
                    var_array[i][int(j/2)] = Variable('cell[{}][{}]'.format(i, int(j/2)), full_domain)
                else:
                    assigned_var = Variable('cell[{}][{}]'.format(i, int(j/2)), [col])
                    assigned_var.assign(col)
                    var_array[i][int(j/2)] = assigned_var

                ourCSP.add_var(var_array[i][int(j/2)])

                if found_sign == True:
                    if sign == '>':
                        sat_tuples = []
                        c_uneq = Constraint('C({},{})'.format(int(j/2)-1, int(j/2)), [var_array[i][int(j/2)-1], var_array[i][int(j/2)]])
                        for x in var_array[i][int(j/2)-1].cur_domain():
                            for y in var_array[i][int(j/2)].cur_domain():
                                if x > y:
                                    sat_tuples.append([x,y])
                        c_uneq.add_satisfying_tuples(sat_tuples)
                        ourCSP.add_constraint(c_uneq)
                    elif sign == '<':
                        sat_tuples = []
                        c_uneq = Constraint('C({},{})'.format(int(j/2)-1, int(j/2)), [var_array[i][int(j/2)-1], var_array[i][int(j/2)]])
                        for x in var_array[i][int(j/2)-1].cur_domain():
                            for y in var_array[i][int(j/2)].cur_domain():
                                if x < y:
                                    sat_tuples.append([x,y])
                        c_uneq.add_satisfying_tuples(sat_tuples)
                        ourCSP.add_constraint(c_uneq)
            else:
                if col == '.':
                    found_sign = False
                else:
                    found_sign = True
                    sign = col
    
    for i,row in enumerate(var_array):
        for j, col in enumerate(row):
            for m in range(1,dim-j):                #col constraints
                sat_tuples = []
                c_uneq = Constraint('C_col([{},{}],[{},{}])'.format(i, j, i, j + m), [var_array[i][j], var_array[i][j+m]])
                #print('C_row([{},{}],[{},{}])'.format(i, j, i, j + m))
                for x in var_array[i][j].cur_domain():
                    for y in var_array[i][j+m].cur_domain():
                        if x != y:
                            sat_tuples.append([x,y])
                #print(sat_tuples)
                c_uneq.add_satisfying_tuples(sat_tuples)
                ourCSP.add_constraint(c_uneq)

            for m in range(1,dim-i):                #row constraints
                sat_tuples = []
                c_uneq = Constraint('C_row([{},{}],[{},{}])'.format(i, j, i+m, j), [var_array[i][j], var_array[i+m][j]])
                #print('C_col([{},{}],[{},{}])'.format(i, j, i+m, j))
                for x in var_array[i][j].cur_domain():
                    for y in var_array[i+m][j].cur_domain():
                        if x != y:
                            sat_tuples.append([x,y])
                #print(sat_tuples)
                c_uneq.add_satisfying_tuples(sat_tuples)
                ourCSP.add_constraint(c_uneq)

    #ourCSP.print_all()
    return ourCSP, var_array

#futoshiki_csp_model_1(board_1)

def futoshiki_csp_model_2(futo_grid):
    ourCSP = CSP("Futushiki")

    dim = len(futo_grid)
    full_domain = []

    for i in range(1,dim+1):
        full_domain.append(i)
    
    var_array = [full_domain[:] for i in range(1,dim+1)]
    found_sign = False
    sign = ''

    for i, row in enumerate(futo_grid):
        for j, col in enumerate(row):
            if j%2 == 0:
                if int(j/2) == 0:
                    found_sign = False                          #for the last cell in row
                if col == 0:
                    var_array[i][int(j/2)] = Variable('cell[{}][{}]'.format(i, int(j/2)), full_domain)
                else:
                    assigned_var = Variable('cell[{}][{}]'.format(i, int(j/2)), [col])
                    assigned_var.assign(col)
                    var_array[i][int(j/2)] = assigned_var

                ourCSP.add_var(var_array[i][int(j/2)])

                if found_sign == True:
                    if sign == '>':
                        sat_tuples = []
                        c_uneq = Constraint('C({},{})'.format(int(j/2)-1, int(j/2)), [var_array[i][int(j/2)-1], var_array[i][int(j/2)]])
                        for x in var_array[i][int(j/2)-1].cur_domain():
                            for y in var_array[i][int(j/2)].cur_domain():
                                if x > y:
                                    sat_tuples.append([x,y])
                        c_uneq.add_satisfying_tuples(sat_tuples)
                        ourCSP.add_constraint(c_uneq)
                    elif sign == '<':
                        sat_tuples = []
                        c_uneq = Constraint('C({},{})'.format(int(j/2)-1, int(j/2)), [var_array[i][int(j/2)-1], var_array[i][int(j/2)]])
                        for x in var_array[i][int(j/2)-1].cur_domain():
                            for y in var_array[i][int(j/2)].cur_domain():
                                if x < y:
                                    sat_tuples.append([x,y])
                        c_uneq.add_satisfying_tuples(sat_tuples)
                        ourCSP.add_constraint(c_uneq)
            else:
                if col == '.':
                    found_sign = False
                else:
                    found_sign = True
                    sign = col

    for i, row in enumerate(var_array):                     #row constraints
        sat_tuples = []
        assigned_values = []
        c_uneq = Constraint('C_row {}'.format(i), row)
        #print('C_row {}'.format(i))

        for j, col in enumerate(row):
            cell_dom = col.cur_domain()
            if cell_dom != full_domain:
                y = 0
                for x in cell_dom:
                    y = x
                assigned_values.append([j,y])
          
        temp_dom = []
        for j in full_domain:
            temp_dom.append(j)

        if len(assigned_values) != 0:
            for index, value in assigned_values:
                temp_dom.remove(value)
        
        permutations = itertools.permutations(temp_dom)
        for perm in permutations:
            sat_tuples.append(list(perm))

        if len(assigned_values) != 0:
            for index, value in assigned_values:
                for perm in sat_tuples:
                    perm.insert(index, value)
        #print(sat_tuples)
        c_uneq.add_satisfying_tuples(sat_tuples)
        ourCSP.add_constraint(c_uneq)


    var_array_transpose = zip(*var_array)                   #column constrains
    var_array_temp = []

    for row in var_array_transpose:
        var_array_temp.append(list(row))

    for i, row in enumerate(var_array_temp):                   
        sat_tuples = []
        assigned_values = []
        c_uneq = Constraint('C_col {}'.format(i), row)
        #print('C_col {}'.format(i))

        for j, col in enumerate(row):
            cell_dom = col.cur_domain()
            if cell_dom != full_domain:
                y = 0
                for x in cell_dom:
                    y = x
                assigned_values.append([j,y])
          
        temp_dom = []
        for j in full_domain:
            temp_dom.append(j)

        if len(assigned_values) != 0:
            for index, value in assigned_values:
                temp_dom.remove(value)
        
        permutations = itertools.permutations(temp_dom)
        for perm in permutations:
            sat_tuples.append(list(perm))

        if len(assigned_values) != 0:
            for index, value in assigned_values:
                for perm in sat_tuples:
                    perm.insert(index, value)
        #print(sat_tuples)
        c_uneq.add_satisfying_tuples(sat_tuples)
        ourCSP.add_constraint(c_uneq)

    #ourCSP.print_all()
    return ourCSP, var_array