# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
#
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left,
# up, and down motions. NOTE: the 'v' should be
# lowercase.
#
# Your function should be able to do this for any
# provided grid, not just the sample grid below.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function. [4, 5]
# note: array addressing is [-y, x]

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():

    expand = [[ -1 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand[init[0]][init[1]] = 0
    expansion_number = 1

    motions = [[ ' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    closed = [[ 0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    g = 0
    y = init[0]
    x = init[1]
    open = [[g,y,x]]

    found = False
    resign = False # no valid path to goal

    while not found and not resign:
        if len(open) == 0:
            resign = True
            #return 'fail'
            #return motions
            break
        else:
            #remove node from list
            open.sort()
            open.reverse() #pop comes at end of list
            next = open.pop()
            g = next[0]
            y = next[1]
            x = next[2]

            if y == goal[0] and x == goal[1]:
                found = True
                #return next
                #return motions
                break
            else:
                #expand winning element and add to list
                for i in range(len(delta)):
                    y2 = y + delta[i][0]
                    x2 = x + delta[i][1]
                    if y2 >= 0 and y2 < len(grid) and x2 >= 0 and x2 < len(grid[0]):
                        if closed[y2][x2] == 0 and grid[y2][x2] == 0:
                            g2 = g + cost
                            open.append([g2, y2, x2])
                            closed[y2][x2] = 1
                            expand[y2][x2] = expansion_number
                            expansion_number += 1
                            motions[y2][x2] = i
    #return expand

    #for i in range(len(motions)):
    #    print motions[i]

    #work backwards from solution
    plan = [[ ' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    y = goal[0]
    x = goal[1]
    plan[y][x] = '*'
    while y != init[0] or x != init[1]:
            y2 = y - delta[motions[y][x]][0]
            x2 = x - delta[motions[y][x]][1]
            plan[y2][x2] = delta_name[motions[y][x]]
            y = y2
            x= x2
    return plan

plan =  search()

for i in range(len(plan)):
    print plan[i]
