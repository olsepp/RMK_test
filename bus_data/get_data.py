import requests


def get_data_from_external_source():
    """
    Get all data available from external source.

    :return: string from data source
    """
    data = requests.get("https://transport.tallinn.ee/gps.txt").content.decode("utf-8")

    return data


def data_to_list():
    """
    Put data from external source to list.

    :return: data as list
    """
    data = get_data_from_external_source()
    return data.split("\n")


def filter_data():
    """
    Get data only for bus number 8 and that is heading in Äigrumäe direction.

    :return: list of records only for bus number 8 that is heading towards Äigrumäe
    """
    # Get unfiltered data from previous function
    unfiltered_data = data_to_list()

    # Initialize a list to store data that represents bus number 8
    bus_nr_8 = []

    # Iterate through unfiltered data
    for line in unfiltered_data:

        # Check if record has data
        if line:

            # Split record into parts, so it is easier to get specific part
            attributes = line.split(",")

            # Check for vehicle type "2", because "2" = bus, bus number 8 and final destination "Äigrumäe"
            if attributes[0] == "2" and attributes[1] == "8" and attributes[len(attributes) - 1] == "Äigrumäe":

                # If conditions are met, append record to list
                bus_nr_8.append(line)

    return bus_nr_8


