
from collections import deque, defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Количество вершин
        self.graph = defaultdict(list)  # Граф в формате смежности
        self.capacity = defaultdict(lambda: defaultdict(int))  # Вместимость

    def add_edge(self, u, v, w):
        self.graph[u].append(v)  # Добавляем ребро
        self.graph[v].append(u)  # Добавляем обратное ребро
        self.capacity[u][v] += w  # Увеличиваем вместимость
        self.capacity[v][u] += 0  # Инициализируем обратное ребро с вместимостью 0

    def bfs(self, s, t, parent):
        visited = [False] * (self.V)
        queue = deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()

            for v in self.graph[u]:
                if not visited[v] and self.capacity[u][v] > 0:  # Если не посещена и есть остаточная вместимость
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self, source, sink):
        parent = [-1] * (self.V)
        max_flow = 0

        while self.bfs(source, sink, parent):
            # Находим минимальную пропускную способность по пути из source в sink
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.capacity[parent[s]][s])
                s = parent[s]

            # Обновляем остаточные емкости рёбер и обратных рёбер
            v = sink
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= path_flow
                self.capacity[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow


# Пример использования
if __name__ == "__main__":
    g = Graph(6)
    g.add_edge(0, 1, 16)
    g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 3, 12)
    g.add_edge(2, 1, 4)
    g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7)
    g.add_edge(4, 5, 4)

    source = 0  # Источник
    sink = 5    # Сток

    max_flow = g.edmonds_karp(source, sink)
    print("MAX_FlOW", max_flow)
