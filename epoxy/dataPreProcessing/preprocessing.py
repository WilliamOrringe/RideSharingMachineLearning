from datetime import datetime
import csv


def get_ride_data():
    ride_data = []
    with open("../../data/yellow_tripdata_2013-01.csv", newline='', encoding="utf8") as ride_file:
        reader = csv.DictReader(ride_file)
        for index, row in enumerate(reader):
            if index >= 100000:
                break
            ride_data.append(row)
    ride_file.close()
    return ride_data


def feature_selection(ride_data):
    for datum in ride_data:
        datum.pop("VendorID")
        datum.pop("RatecodeID")
        datum.pop("store_and_fwd_flag")
        datum.pop("payment_type")
        datum.pop("fare_amount")
        datum.pop("extra")
        datum.pop("mta_tax")
        datum.pop("tip_amount")
        datum.pop("tolls_amount")
        datum.pop("improvement_surcharge")
        datum.pop("total_amount")
        datum.pop("congestion_surcharge")
    return ride_data


def feature_selection2(ride_data):

    features = ["vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count",
                          "trip_distance", "pickup_longitude", "pickup_latitude", "rate_code",
                          "store_and_fwd_flag", "dropoff_longitude", "dropoff_latitude",
                          "payment_type", "fare_amount", "surcharge", "mta_tax", "tip_amount",
                          "tolls_amount", "total_amount"]
    features_to_delete = ["vendor_id", "rate_code", "store_and_fwd_flag", "payment_type",
                          "fare_amount", "surcharge", "mta_tax", "tip_amount", "tolls_amount",
                          "total_amount"]
    print(features)
    for datum in ride_data:
        for features in features_to_delete:
            datum.pop(features)
    return ride_data


def delete_low_distance(ride_data):
    for datum in ride_data:
        if float(datum["trip_distance"]) < 0.5:
            del datum
    return ride_data


# def add_seconds(ride_data):
#     for datum in ride_data:
#         first = datetime.fromisoformat(datum['tpep_pickup_datetime'])
#         second = datetime.fromisoformat(datum['tpep_dropoff_datetime'])
#         total_seconds = round((second - first).total_seconds())
#         datum['time'] = total_seconds
#         datum.pop("tpep_pickup_datetime")
#         datum.pop("tpep_dropoff_datetime")
#     return ride_data

def add_seconds(ride_data):
    for datum in ride_data:
        first = datetime.fromisoformat(datum['pickup_datetime'])
        second = datetime.fromisoformat(datum['dropoff_datetime'])
        total_seconds = round((second - first).total_seconds())
        datum['time'] = total_seconds
        datum.pop("pickup_datetime")
        datum.pop("dropoff_datetime")
    return ride_data


if __name__ == "__main__":
    ride_data1 = get_ride_data()
    ride_data2 = feature_selection2(ride_data1)
    ride_data3 = delete_low_distance(ride_data2)
    ride_data4 = add_seconds(ride_data3)
    print(ride_data4[0])
