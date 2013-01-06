# ----------
# User Instructions:
#
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal.
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value():

    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]

    closed[goal[0]][goal[1]] = 1
    value[goal[0]][goal[1]] = 0
    open = [[0, goal[0],goal[1]]]
        
    while len(open) > 0:
#        for i in value:
#            print i

        open.sort()
        open.reverse()
        next = open.pop()
#            print next
        v = next[0]
        y = next[1]
        x = next[2]
        for i in range(len(delta)):
            v2 = v + cost_step
            y2 = y + delta[i][0]
            x2 = x + delta[i][1]
            if y2 >= 0 and y2 < len(grid) and x2 >=0 and x2 < len(grid[0]):
                if closed[y2][x2] == 0 and grid[y2][x2] == 0:
                    value[y2][x2] = v2
                    open.append([v2, y2,x2])
                    closed[y2][x2] = 1

    return value #make sure your function returns a grid of values as demonstrated in the previous video.

value = compute_value()

for i in value:
    print i