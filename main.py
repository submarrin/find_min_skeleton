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
    return (graph_matrix)

print(read_graph())

