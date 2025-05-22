import requests


def get_data_from_external_source():
    """
    Get all data available from external source.

    :return: string from data source
    """
    data = requests.get("https://transport.tallinn.ee/gps.txt").text
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
    Get only bus number 8 data

    :return: list of records only for bus number 8
    """
    unfiltered_data = data_to_list()
    bus_nr_8 = []
    for line in unfiltered_data:
        if line:
            attributes = line.split(",")
            if attributes[0] == "2" and attributes[1] == "8":
                bus_nr_8.append(line)

    return bus_nr_8
