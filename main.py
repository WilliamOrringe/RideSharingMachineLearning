from Drivers import Drivers
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
        nodes[index].give_neighbours([nodes[index + 1], 1])
    nodes[9].give_neighbours([nodes[0], 1])
    return nodes


def initialise_drivers(number_of_drivers, capacity):
    drivers2 = []
    for index in range(number_of_drivers):
        drivers2.append(Drivers(capacity))
    return drivers2


def print_graph(nodes, drivers2):
    print(nodes)
    print(drivers2)


if __name__ == "__main__":
    graph = initialise_nodes()
    drivers = initialise_drivers(5, 5)
    for driver in drivers:
        driver.set_random_position(graph)
        print(driver.get_position())
    print_graph(graph, drivers)
