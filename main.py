from Node import Node


def q_learning():
    q_tables = [[]]
    for i in range(10):
        print("hi")


def initialise_nodes():
    nodes = []
    for index in range(10):
        nodes.append(Node(index))
    for index in range(9):
        nodes[index].give_neighbours([nodes[index+1], 1])
    nodes[9].give_neighbours([nodes[0], 1])
    return nodes


def print_graph(nodes):
    for node in nodes:
        print(str(node))


if __name__ == "__main__":
    graph = initialise_nodes()
    print_graph(graph)
