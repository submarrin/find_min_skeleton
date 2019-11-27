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
    for j in range(0, n):
        for i in range(0, j+1):
            if matr[i][j] is not None:
                ribs.append([i, j, matr[i][j]])
    return ribs


def sort_ribs(ribs):
    def get_weight(item):
        return item[2]
    return sorted(ribs, key=get_weight)


matr = read_graph()
ribs = get_ribs(matr)
print(ribs)
sorted_ribs = sort_ribs(ribs)
print(sorted_ribs)


def merge_components(v, w, p_name, q_name, name, next_comp, size):
    name[v] = p_name
    u = next_comp[v]
    while name[u] != p_name:
        name[u] = p_name
        u = next_comp[u]
    size[p_name] = size[p_name] + size[q_name]
    x = next_comp[v]
    y = next_comp[w]
    next_comp[v] = y
    next_comp[w] = x
    return name, next_comp, size


def find_skeleton(graph_matrix):
    n = len(graph_matrix)
    name, next_comp, size = [None] * n, [None] * n, [None] * n
    queue_ribs = get_ribs(graph_matrix)
    queue_ribs = sort_ribs(queue_ribs)
    for i in range(n):
        name[i] = i
        next_comp[i] = i
        size[i] = 1
    # print(name, next_comp, size)
    skeleton = []
    while len(skeleton) != (n - 1):
        loc_rib = queue_ribs.pop(0)
        v = loc_rib[0]
        w = loc_rib[1]
        p_name = name[v]
        q_name = name[w]
        print("p = ", p_name, "q = ", q_name)
        if p_name != q_name:
            if size[p_name] > size[q_name]:
                name, next_comp, size = merge_components(w, v, q_name, p_name, name, next_comp, size)
            else:
                name, next_comp, size = merge_components(v, w, p_name, q_name, name, next_comp, size)
            new_rib = [v + 1, w + 1]
            skeleton.append(new_rib)
    return skeleton


print(find_skeleton(read_graph()))

