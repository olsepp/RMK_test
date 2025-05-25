import csv
from collections import defaultdict
from datetime import datetime


def count_buses():
    """
    Count times each bus visited the stops in timeframe.
    :return: Dictionary of buses that visited stations in timeframe
    """
    counter = {}  # Define counter dictionary
    # Read CSV file that has record of buses and times they visited the stops
    with open("bus_schedule.csv", "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        # Iterate through each line
        for line in reader:
            vehicle_id = line[1]  # Unique ID each bus has
            if vehicle_id not in counter:
                counter[vehicle_id] = 1
            else:
                counter[vehicle_id] += 1

    return counter


def filter_schedule():
    # Get how many times each bus appears in the dataset
    buses = count_buses()

    # Dictionary to store the matching buses and the times they were at each stop
    # defaultdict allows us to automatically create a nested dict for each bus
    schedule = defaultdict(dict)

    # Open and read the CSV file again
    with open("bus_schedule.csv", "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row

        # Go through each line in the file
        for line in reader:
            timestamp = line[0]  # Timestamp when the bus was at a stop
            vehicle_id = line[1]  # ID of the bus
            stop = line[2]  # The name of the stop (e.g., ZOO or TOOMPARK)

            # Only consider buses that appeared exactly twice in total
            if buses[vehicle_id] == 2:
                # Save the timestamp for this stop under the correct vehicle ID
                schedule[vehicle_id][stop] = timestamp

    # Now, filter the result to only include buses that visited BOTH stops
    final_schedule = {}

    for vehicle_id, stops in schedule.items():
        if "ZOO" in stops and "TOOMPARK" in stops:
            # Only include if the bus visited both stops
            final_schedule[vehicle_id] = {
                "ZOO": stops["ZOO"],
                "TOOMPARK": stops["TOOMPARK"]
            }

    return final_schedule


def clean_timestamps():
    """
    Clean up timestamps in data to more readable format
    :return: same schedule as in previous function but with readable times
    """
    # Get schedule from function above
    schedule = filter_schedule()

    # Iterate through each ID and times it stopped at stations
    for bus_id, stops in schedule.items():
        # Iterate through stops to get times and update them
        for stop in stops:
            time = stops[stop]
            dt = datetime.fromisoformat(time)
            readable_time = dt.strftime("%H:%M:%S")
            stops[stop] = readable_time

    return schedule


def write_filtered_file():
    """
    Write cleaned up data to another CSV file
    :return: None
    """
    # Get schedule with readable timestamps
    schedule = clean_timestamps()

    # Open new CSV file to write into
    with open("filtered_schedule.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        # Define headers
        writer.writerow(["Bus ID", "ZOO", "TOOMPARK"])
        # Iterate through schedule and write data from dictionary to CSV file
        for bus, stops in schedule.items():
            zoo_time = stops.get("ZOO")
            toompark_time = stops.get("TOOMPARK")
            writer.writerow([bus, zoo_time, toompark_time])


write_filtered_file()
