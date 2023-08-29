#other imports
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

class Node:
    def __init__(self, grid, x, y):
        self.x = x
        self.y = y
        self.grid = grid
        self.type = NodeType.EMPTY
        self.g_score = float('inf')
        self.f_score = float('inf')

    def get_neighbors(self):
        # Collection of arrays representing the x and y displacement
        rows = len(self.grid)
        cols = len(self.grid[0])
        directions = [[1, 0], [0, 1], [0, -1], [-1, 0]]
        neighbors = []
        for direction in directions:
            neighbor_x = self.x  + direction[0]
            neighbor_y = self.y + direction[1]
            if neighbor_x >= 0 and neighbor_y >= 0 and neighbor_x < cols and neighbor_y < rows:
                neighbors.append(self.grid[neighbor_y][neighbor_x])
        return neighbors


class NodeType(Enum):
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3

def main(array):
    array = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 2],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 3, 3, 0, 0, 0, 0, 0],
         [0, 0, 1, 3, 0, 0, 0, 0],
         [0, 0, 0, 3, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]])

    rows = 8
    cols = 8
    grid = []

    start = None
    end = None

    for y in enumerate(array):
        row_nodes = []
        for x in range(cols):
            node = Node(grid, x, y[0])

            node.type = NodeType(array[y[0]][x])

            if node.type == NodeType.START:
                start = node
            elif node.type == NodeType.END:
                end = node

            row_nodes.append(node)
        grid.append(row_nodes)

    def distance(node1, node2):
        return math.sqrt(math.pow(node1.x - node2.x, 2) + math.pow(node1.y - node2.y, 2))

    def h_score(start, end):
        x_dist = abs(end.x - start.x)
        y_dist = abs(end.y - start.y)
        diagonal_steps = min(x_dist, y_dist)
        straight_steps = y_dist + x_dist - 2 * diagonal_steps
        return diagonal_steps * math.sqrt(2) + straight_steps

    def reconstruct_path(grid, came_from, current):
        path = [current]
        current_key = str(current.x) + ' ' + str(current.y)
        while current_key in came_from:
            current = came_from[current_key]
            current_key = str(current.x) + ' ' + str(current.y)
            path.insert(0, current)
        return path

    def a_star(grid, start, end):
        open_set = []
        closed_set = []
        came_from = {}

        start.g_score = 0
        start.f_score = h_score(start, end)

        open_set.append(start)

        i = 0
        while len(open_set) > 0:
            i += 1
            current = lowest_f_score(open_set)
            open_set.remove(current)
            closed_set.append(current)

            if current == end:
                return reconstruct_path(grid, came_from, current)

            for neighbor in current.get_neighbors():
                if neighbor in closed_set or neighbor.type == NodeType.WALL:
                    continue
                # If both adjacent nodes are walls, dont let it be searched
                adj_node_1 = grid[current.y][neighbor.x]
                adj_node_2 = grid[neighbor.y][current.x]

                if adj_node_1.type == NodeType.WALL and adj_node_2.type == NodeType.WALL:
                    continue
                tentative_g_score = current.g_score + distance(current, neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)
                elif tentative_g_score > neighbor.g_score:
                    # Not a better path
                    continue
                # Found a better path
                came_from[str(neighbor.x) + ' ' + str(neighbor.y)] = current
                neighbor.g_score = tentative_g_score
                neighbor.f_score = neighbor.g_score + h_score(neighbor, end)

    def lowest_f_score(node_list):
        final_node = None
        for node in node_list:
            if not final_node or node.f_score < final_node.f_score:
                final_node = node
        return final_node

    path = a_star(grid, start, end)

    output_path = copy.copy(array)

    for node in path:
        output_path[node.y][node.x] = 5

    _, ax = plt.subplots(1, 2, constrained_layout=True)

    ax[0].matshow(array)

    ax[1].matshow(output_path)

    plt.show()

