# other imports
import numpy as np

import translate_path


def main(playground_matrix, verbose=False):
    def is_valid(x, y, matrix, visited):
        rows = matrix.shape[0]
        cols = matrix.shape[1]

        return 0 <= x < rows and 0 <= y < cols and matrix[x][y] != 4 and not visited[x][y]

    def find_paths_with_cost(matrix, start, end):
        rows = matrix.shape[0]
        cols = matrix.shape[1]

        visited = [[False for _ in range(cols)] for _ in range(rows)]
        paths = []

        def dfs(x, y, path, cost):
            if not is_valid(x, y, matrix, visited):
                return

            visited[x][y] = True
            path.append((x, y))

            if matrix[x][y] == 3:
                cost -= 3
            elif matrix[x][y] == 5:
                cost -= 6
            else:
                cost += 1

            if (x, y) == end:
                paths.append((list(path), cost))
            else:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    dfs(new_x, new_y, path, cost)

            visited[x][y] = False
            path.pop()

        dfs(start[0], start[1], [], 0)
        return paths

    def find_nearby_bonus_nodes(node):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            rows = playground_matrix.shape[0]
            cols = playground_matrix.shape[1]

            new_x, new_y = node[0] + dx, node[1] + dy

            if 0 <= new_x < rows and 0 <= new_y < cols and playground_matrix[new_x][new_y] != 4 and not (new_x, new_y) in ideal_path:
                new_value = playground_matrix[new_x][new_y]

                if new_value == 3 or new_value == 5:
                    bonus_node = (new_x, new_y)

                    bonus_nodes.append(bonus_node)

                    ideal_path.insert(ideal_path.index(node) + 1, bonus_node)
                    ideal_path.insert(ideal_path.index(bonus_node) + 1, node)

                    find_nearby_bonus_nodes(bonus_node)

                return

    start_pos_raw = np.where(playground_matrix == 1)
    end_pos_raw = np.where(playground_matrix == 2)

    if not start_pos_raw[0] or not end_pos_raw[0]:
        print("Start or End field not found!")
        return

    start_pos = (start_pos_raw[0][0], start_pos_raw[1][0])
    finish_pos = (end_pos_raw[0][0], end_pos_raw[1][0])

    paths = find_paths_with_cost(playground_matrix, start_pos, finish_pos)

    sorted_paths = sorted(paths, key=lambda x: x[1])

    ideal_path = sorted_paths[0][0]

    bonus_nodes = []

    for node in ideal_path:
        find_nearby_bonus_nodes(node)

