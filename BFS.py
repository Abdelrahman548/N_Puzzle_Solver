from queue import PriorityQueue
import time
import matplotlib.pyplot as plt
import numpy as np
import Heuritic as heu
import os
from datetime import datetime

class BFS:
    PUZZLE_SIZES = [3, 4, 5]
    def __init__(self, initial):
        if BFS.isValid(initial):
            self.__size = len(initial)
            self.__initial = initial
            self.__goal = self.__setGoal()
            self.__visited = set()
            self.__pq = PriorityQueue()
            self.__valid = True
            self.__moves=0
            self.__startT = None
            self.__endT = None
            self.__path = []
            self.__isDone = False
        else:
            self.__valid = False
            raise ValueError("Invalid Board Size or Values")


    @staticmethod
    def isValid(board):
        n = len(board)

        # Check if the board is squared
        if n != len(board[0]):
            return False
        
        # Check if the board is 8 or 15 or 24 puzzle
        if n not in BFS.PUZZLE_SIZES:
            return False
        
        #Convert to 1d
        flattened = [val for row in board for val in row]
        # Check if the values are distinct and in the range from 0 to n^2 - 1
        if sorted(flattened) != list(range(n**2)):
            return False
        
        return True

    def __setGoal(self):
        n = self.__size
        board = [[i + j * n + 1 for i in range(n)] for j in range(n)]
        board[-1][-1] = 0
        return board

    def getInitial(self):
        return self.__initial
    
    # Get Node's Children
    def __expand(self, state):
        children = []

        # Get 0 position row,col
        blank = self.__getBlankPos(state)

        # right down left up
        for m in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = [blank[0] + m[0], blank[1] + m[1]]

            # if new position inside board range make a new state of Movement
            if self.__isLegal(new_pos[0], new_pos[1]):
                new_state = [row[:] for row in state]
                new_state[blank[0]][blank[1]] = state[new_pos[0]][new_pos[1]]
                new_state[new_pos[0]][new_pos[1]] = 0
                children.append(new_state)
        return children

    def solve(self, funNum):
        self.__path = []
        levelinc=1
        if not self.__valid:
            return

        if (funNum > 3) or (funNum < 0):
            raise ValueError('Wrong Function Input')

        self.__startTime()
        value = self.__calculateHeuristic(self.__initial, funNum)
        self.__pq.put((value, 0, [self.__initial, 0, []]))  # Include an empty list for the path
        while not self.__pq.empty():
            _, _, Node = self.__pq.get()
            current_state, level, path = Node

            self.__path.append((current_state, level, path))  # Save the path to the current state
            if len(self.__path)>80000:
                return -1
            if self.__isSolved(current_state):
                self.__endTime()
                self.__isDone = True
                self.__moves=len(path + [current_state])
                return path + [current_state]

            if tuple(map(tuple, current_state)) not in self.__visited:
                self.__visited.add(tuple(map(tuple, current_state)))

                level += levelinc
                for child in self.__expand(current_state):
                    value = self.__calculateHeuristic(child, funNum)
                    
                    self.__pq.put((value + level, 0, [child, level, path + [current_state]]))
        return -1

    def __isSolved(self, current_state):
        return current_state == self.__goal

    def __calculateHeuristic(self, state, funNum):
        if funNum == 0:
            return heu.manhattan_distance(state, self.__goal)
        elif funNum == 1:
            return heu.hamming_distance(state, self.__goal)
        elif funNum == 2:
            return heu.euclidean_distance(state, self.__goal)
        elif funNum == 3:
            return heu.linear_conflict(state, self.__goal)
        # Add the Fourth Heuristic Here and Change if range in solve()

    def __getBlankPos(self, state):
        for i in range(self.__size):
            for j in range(self.__size):
                if state[i][j] == 0:
                    return [i, j]

    def __isLegal(self, row, col):
        rowlen = len(self.__goal)
        return 0 <= row < rowlen and 0 <= col < rowlen

    def __startTime(self):
        self.__startT = time.time()

    def __endTime(self):
        self.__endT = time.time()

    def getTime(self):
        if self.__isDone:
            #return time in seconds
            return (self.__endT - self.__startT)
        else:
            return 0

    def getNumOfSteps(self):
        if self.__isDone:
            return len(self.__path)-1
        else:
            return 0
    def getMoves(self):
        if self.__isDone:
            return self.__moves-1
        else:
            return 0
    
    @staticmethod
    def getGraph(steps_values, time_values):
        heuristic_names = ['Manhattan', 'Hamming', 'Euclidean', 'Linear Conflict']
        num_heuristics = len(heuristic_names)

        # Create a list of x values for each heuristic
        x_values = np.arange(num_heuristics)

        # Plot a bar chart for each heuristic
        for i in range(len(heuristic_names)):
            plt.bar(i, steps_values[i], label=heuristic_names[i], alpha=0.7)

            # Add time as text at the bottom of each rectangle
            plt.text(i, 1.0, f'{time_values[i]:.2f}\n seconds', ha='center', va='bottom', color='black')

        # Ensure the directory exists
        os.makedirs('./Graphs', exist_ok=True)
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H-%M-%S")
        filename = f'./Graphs/heuristic_comparison_{timestamp}.png'

        plt.title('Heuristic Comparison')
        plt.xlabel('Heuristic')
        plt.ylabel('Number of Steps')
        plt.xticks(x_values, heuristic_names)  # Set x-axis ticks at the center of each bar
        plt.legend()
        plt.savefig(filename)
        plt.show()
