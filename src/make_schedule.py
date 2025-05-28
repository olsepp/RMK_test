from bus_data import get_data
import time
import datetime
import csv
from math import radians, sin, cos, sqrt, atan2

# Constant values for bus stations
ZOO_STOP = 59.426231, 24.658889
TOOMPARK_STOP = 59.436846, 24.733343


def is_near(coordinate1, coordinate2, threshold=50):
    """
    Returns True if coordinates1 and coordinates2 are within `threshold` meters of each other.

    Uses the Haversine formula to calculate the great-circle distance between two points
    on the Earth based on their latitude and longitude.

    :param coordinate1: Tuple of (latitude, longitude) in decimal degrees (e.g. (59.426231, 24.658889))
    :param coordinate2: Tuple of (latitude, longitude) in decimal degrees
    :param threshold: Distance in meters within which the two points are considered "near"
    :return: Boolean - True if distance <= threshold, False otherwise
    """

    # Earth’s radius in meters
    earth_radius = 6371000

    # Convert coordinates from degrees to radians
    latitude1, longitude1 = radians(coordinate1[0]), radians(coordinate1[1])
    latitude2, longitude2 = radians(coordinate2[0]), radians(coordinate2[1])

    # Differences in latitude and longitude
    differences_in_latitude = latitude2 - latitude1
    differences_in_longitude = longitude2 - longitude1

    # Haversine formula to calculate distance
    a = sin(differences_in_latitude / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(differences_in_longitude / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Final distance between bus and station in meters
    distance = earth_radius * c

    # Return True if distance is within the threshold
    return distance <= threshold


def construct_bus_schedule(csv_writer, logs):

    """
    Build bus schedule as CSV file
    :param csv_writer: csv writer from outer scope
    :param logs: set seen from outer scope, holds records
    :return: None
    """

    # Initialize current time to make logs
    now = datetime.datetime.now()

    # Log the time when check was executed
    print(f"Checking at {now.time()}")

    # Get new filtered bus data
    data = get_data.filter_data()

    # Iterate through filtered data
    for line in data:

        fields = line.split(",")

        # Make sure that line of record is valid
        if len(fields) < 7:

            # Let user know that the line of data was incomplete
            print("Incomplete line of data")
            continue

        try:
            # Convert latitude and longitude of bus into right format
            latitude = int(fields[3]) / 1_000_000
            longitude = int(fields[2]) / 1_000_000

            # Put coordinates into tuple to use them later in distance calculations
            coordinates = (latitude, longitude)

            # Extract unique vehicle ID from records
            vehicle_id = fields[6]
        except (ValueError, IndexError):
            continue

        # Check if bus is near ZOO bus station
        if is_near(coordinates, ZOO_STOP) and (vehicle_id, "ZOO") not in logs:

            # If conditions are met, log it into CSV file and to logs set
            csv_writer.writerow([now.isoformat(), vehicle_id, "ZOO"])
            logs.add((vehicle_id, "ZOO"))

            # Let user know that bus is at ZOO station
            print(f"🟢 ZOO: {vehicle_id} at {now.time()}")

        # Check if bus is near TOOMPARK bus station
        if is_near(coordinates, TOOMPARK_STOP) and (vehicle_id, "TOOMPARK") not in logs:

            # If conditions are met, log it into CSV file and to logs set
            csv_writer.writerow([now.isoformat(), vehicle_id, "TOOMPARK"])
            logs.add((vehicle_id, "TOOMPARK"))

            # Let user know that bus was at TOOMPARK station
            print(f"🔵 TOOMPARK: {vehicle_id} at {now.time()}")


# Define a set to keep track of buses when they reach station
seen = set()

# Open a CSV file to write data into
with open("bus_schedule.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write headers for data
    writer.writerow(["timestamp", "vehicle_id", "stop"])

    # Loop to keep the live data checking going
    while True:

        # Get the current hour
        hour = datetime.datetime.now().hour

        # Stop the loop at 09:00
        if hour == 9:
            print("Stopped logging at 09:00.")
            break

        # Wait for 08:00 to start collecting data
        if hour != 8:
            print("Waiting for 08:00...")
            time.sleep(10)
            continue

        # Call function to initialize data collection
        construct_bus_schedule(writer, seen)

        # Wait 5 seconds, same interval after which the live data is updated
        time.sleep(5)

