from typing import List


def read_graph():
    file_in = open("file_in.txt", 'r')
    n = int(file_in.readline())
    graph_matrix = [None] * n
    for j in range(n):
        graph_matrix[j] = [None] * n
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
        for i in range(0, j + 1):
            if matr[i][j] is not None:
                ribs.append([i, j, matr[i][j]])
    return ribs


def sort_ribs(ribs):
    def get_weight(item):
        return item[2]

    return sorted(ribs, key=get_weight)


def merge_components(vertix1, vertix2, name_component_vertix1, name_component_vertix2, component_name_for_vertices,
                     next_vertix_in_component, size_of_component_by_its_vertix):
    component_name_for_vertices[vertix2] = name_component_vertix1
    neighbour_vertix_in_component = next_vertix_in_component[vertix2]
    while component_name_for_vertices[neighbour_vertix_in_component] != name_component_vertix1:
        component_name_for_vertices[neighbour_vertix_in_component] = name_component_vertix1
        neighbour_vertix_in_component = next_vertix_in_component[neighbour_vertix_in_component]
    size_of_component_by_its_vertix[name_component_vertix1] = size_of_component_by_its_vertix[name_component_vertix1] + \
                                                              size_of_component_by_its_vertix[name_component_vertix2]
    x = next_vertix_in_component[vertix1]
    y = next_vertix_in_component[vertix2]
    next_vertix_in_component[vertix1] = y
    next_vertix_in_component[vertix2] = x
    return component_name_for_vertices, next_vertix_in_component, size_of_component_by_its_vertix


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
        #print("p = ", p_name, "q = ", q_name)
        if p_name != q_name:
            if size[p_name] > size[q_name]:
                name, next_comp, size = merge_components(w, v, q_name, p_name, name, next_comp, size)
            else:
                name, next_comp, size = merge_components(v, w, p_name, q_name, name, next_comp, size)
            skeleton.append(loc_rib)
    return skeleton


def get_skeleton_and_weight(skeleton_with_weights):
    weight_skeleton = 0
    skeleton = []
    for bone in skeleton_with_weights:
        new_bone = [bone[0], bone[1]]
        weight_skeleton = weight_skeleton + bone[2]
        skeleton.append(new_bone)
    return skeleton, weight_skeleton

#print(get_skeleton_and_weight([[1,2,0], [0,1,5], [2,3,25]]))


def get_matr_from_ribs(skeleton, n):
    matr = [None] * n
    for j in range(n):
        matr[j] = [None] * n
    for rib in skeleton:
        i = rib[0]
        j = rib[1]
        matr[i][j] = 1
        matr[j][i] = 1
    return matr


def get_lists_from_matr(matr):
    n = len(matr)
    lists = []
    for i in range(0,n):
        list_for_vertix = []
        for j in range(0,n):
            if matr[i][j] is not None:
                list_for_vertix.append(j+1)
        lists.append(list_for_vertix)
    return lists


#print(get_lists_from_matr([[None, 1, None, None], [1, None, 1, None], [None, 1, None, 1], [None, None, 1, None]]))


def write_in_file(lists, weight):
    file_out = open("file_out.txt", 'w')
    for list_of_elements in lists:
        for element in list_of_elements:
            file_out.write(str(element))
            file_out.write(' ')
        file_out.write("0")
        file_out.write('\n')
    file_out.write(str(weight))
    file_out.close()
    return


def main():
    graph_matrix = read_graph()
    n = len(graph_matrix)
    skeleton_with_weights = find_skeleton(graph_matrix)
    print("found skeleton ribs with weight")
    skeleton, weight = get_skeleton_and_weight(skeleton_with_weights)
    matr_of_skeleton = get_matr_from_ribs(skeleton, n)
    lists_of_skeleton = get_lists_from_matr(matr_of_skeleton)
    print("lists_of_skeleton", lists_of_skeleton)
    write_in_file(lists_of_skeleton, weight)
    return


main()


#print(find_skeleton(read_graph()))
