def read_graph():
    file_in = open("file_in.txt", 'r')
    n = int(file_in.readline())
    graph_matrix = [None]*n
    for j in range(n):
        graph_matrix[j] = [None]*n
    for i in range(n):
        line = file_in.readline().split()
        pairs = [*zip(
            line[::2],
            line[1::2]
        )]
        # print(pairs)
        for index, weight in pairs:
            graph_matrix[i][int(index) - 1] = int(weight)
    file_in.close()
    return graph_matrix


print(read_graph())


def get_ribs(matr):
    ribs = []
    n = len(matr)
    for i in range(0, n):
        for j in range(0, n):
            if matr[i][j] is not None:
                ribs.append([i, j, matr[i][j]])
    return ribs


def sort_ribs(ribs):
    def get_weight(item):
        return item[2]
    return sorted(ribs, key=get_weight)


def merge_components(graph_matrix, v, w, p_name, q_name):
    n = len(graph_matrix)
    name, next_comp, size = [None] * n, [None] * n, [None] * n
    name[v] = p_name
    u = next_comp[v]
    print(name, next_comp, size)
    while name[u] != p_name:
        name[u] = p_name
        u = next_comp[u]
    size[p_name] = size[p_name] + size[q_name]
    x = next_comp[v]
    y = next_comp[w]
    next_comp[v] = y
    next_comp[w] = x


def find_skeleton(graph_matrix):
    n = len(graph_matrix)
    name, next_comp, size = [None]*n, [None]*n, [None]*n
    queue_ribs = get_ribs(graph_matrix)
    queue_ribs = sort_ribs(queue_ribs)
    for i in range(n):
        name[i] = i
        next_comp[i] = i
        size[i] = 1
    T = []
    while len(T) != (n - 1):
        loc_rib = queue_ribs.pop(0)
        v = loc_rib[0]
        w = loc_rib[1]
        p_name = name[v]
        q_name = name[w]
        if p_name != q_name:
            if size[p_name] > size[q_name]:
                merge_components(graph_matrix, w, v, q_name, p_name)
            else:
                merge_components(graph_matrix, v, w, p_name, q_name)


print(find_skeleton(read_graph()))

