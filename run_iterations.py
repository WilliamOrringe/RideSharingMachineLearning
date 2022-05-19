import csv

from Riders import Riders


def read_file():
    file = open('data/cleandata/clean_data.csv', 'r')
    csv_reader = csv.DictReader(file)
    first_line = True
    file_data = []
    for row in csv_reader:
        file_data.append(row)
    print(file_data)


def who_being_picked_up(pickup_time, ride_data):
    drivers = []
    for datum2 in ride_data:
        if datum2['pickup_time'] == pickup_time:
            drivers.append(datum2)
    return drivers


def run_an_iteration(number=1451):
    beans = []
    segment = 100
    for i in range(number):
        total = round(number / segment)
        if i % total == 0:
            print(round(i * 100 / number), "%")
        goat = who_being_picked_up(i)
        beans.append(goat)
    print(beans)


def update_q_values():
    pass


def cost_function(riders: [Riders]):
    total = 0
    for rider in riders:
        total += rider.wait_time
    return total


if __name__ == "__main__":
    read_file()
