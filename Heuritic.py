##############################
# #  Heuristic Functions   # #
##############################

# O(n^2)
def manhattan_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                x2, y2 = element_position(state[x][y], goal)
                cost += abs(x2 - x) + abs(y2 - y)
    return cost



# O(n^2)
def hamming_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                if state[x][y] != goal[x][y]:
                    cost += 1
    return cost



# O(n^2)
def euclidean_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                x2, y2 = element_position(state[x][y], goal)
                cost += ((x2 - x) ** 2 + (y2 - y) ** 2) ** 0.5
    return cost


def element_position(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return i, j


# O(n^2)
def linear_conflict(state, goal):
    size = len(state)
    conflict_count = 0

    # Helper function to count linear conflicts in a single row or column
    def count_linear_conflicts(line):
        conflicts = 0
        max_val = -1

        for i in range(len(line)):
            if line[i] == 0:
                continue

            if line[i] > max_val:
                max_val = line[i]
            else:
                # Current tile is in conflict with a previous tile
                conflicts += 1

        return conflicts

    # Check rows for conflicts
    for i in range(size):
        conflict_count += count_linear_conflicts(state[i])
        conflict_count += count_linear_conflicts([state[j][i] for j in range(size)])

    return 2 * conflict_count + manhattan_distance(state, goal)
