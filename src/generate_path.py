# other imports
import numpy as np
import translate_path


class Generic:
    def __init__(self, playground_matrix, heading, verbose=False):
        self.playground_matrix = playground_matrix
        self.heading = heading
        self.verbose = verbose


class ModifiedDFS(Generic):
    def main(self):
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
                rows = self.playground_matrix.shape[0]
                cols = self.playground_matrix.shape[1]

                new_x, new_y = node[0] + dx, node[1] + dy

                if 0 <= new_x < rows and 0 <= new_y < cols and self.playground_matrix[new_x][new_y] != 4 and not (new_x, new_y) in ideal_path:
                    new_value = self.playground_matrix[new_x][new_y]
                    new_node = (new_x, new_y)

                    if new_value == 3 or new_value == 5:
                        bonus_nodes.append(new_node)

                        ideal_path.insert(ideal_path.index(node) + 1, new_node)
                        ideal_path.insert(ideal_path.index(new_node) + 1, node)

                    if new_value == 0:
                        for dy, dx in directions:
                            new_x_2, new_y_2 = new_x + dx, new_y + dy

                            if 0 <= new_x_2 < rows and 0 <= new_y_2 < cols and self.playground_matrix[new_x_2][new_y_2] != 4 and not (new_x_2, new_y_2) in ideal_path:

                                new_value = self.playground_matrix[new_x_2][new_y_2]

                                if new_value == 5:
                                    ideal_path.insert(ideal_path.index(node) + 1, new_node)
                                    ideal_path.insert(ideal_path.index(new_node) + 1, node)

        start_pos_raw = np.where(self.playground_matrix == 1)
        end_pos_raw = np.where(self.playground_matrix == 2)

        if not start_pos_raw[0] or not end_pos_raw[0]:
            print("Start or End field not found!")
            return

        start_pos = (start_pos_raw[0][0], start_pos_raw[1][0])
        finish_pos = (end_pos_raw[0][0], end_pos_raw[1][0])

        paths = find_paths_with_cost(self.playground_matrix, start_pos, finish_pos)

        sorted_paths = sorted(paths, key=lambda x: x[1])

        ideal_path = sorted_paths[0][0]

        bonus_nodes = []

        playground_matrix_final = self.playground_matrix.copy()

        for node in ideal_path:
            find_nearby_bonus_nodes(node)
            playground_matrix_final[node[0]][node[1]] = 6

        # for path translation
        translated_path = translate_path.main(self.heading, ideal_path, self.verbose)

        return translated_path, playground_matrix_final


class MyOwnSearch(Generic):
    def main(self):
        pass
