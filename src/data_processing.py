import csv
from datetime import datetime, timedelta

# Input CSV file containing filtered bus schedule
FILTERED_DATA = "filtered_schedule.csv"

# Time it takes Rita to walk from home to ZOO stop (5 minutes)
HOME_TO_STATION = 300
# Time it takes Rita to walk from TOOMPARK stop to the meeting room (4 minutes)
STATION_TO_WORK = 240

# Latest time she can arrive at TOOMPARK to reach her 9:05 meeting
LATEST_ARRIVAL = datetime.strptime("09:05:00", "%H:%M:%S") - timedelta(seconds=STATION_TO_WORK)


def probability_by_minute():
    """ Write a CSV file for every minute Rita could leave home in timeframe.
    Include the bus she could catch and probability of being late.
    """
    # Load all bus data from the filtered schedule
    buses = []
    with open(FILTERED_DATA, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse ZOO and TOOMPARK times into datetime objects
            zoo_time = datetime.strptime(row["ZOO"], "%H:%M:%S")  # type: ignore
            toompark_time = datetime.strptime(row["TOOMPARK"], "%H:%M:%S")  # type: ignore
            # Append data into list
            buses.append({
                "bus_id": row["Bus ID"],  # type: ignore
                "ZOO": zoo_time,
                "TOOMPARK": toompark_time
            })

    # Open the output CSV to save probabilities per minute
    with open("probabilities_by_minute.csv", "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["leave_home_at", "catches_bus", "ZOO", "TOOMPARK", "late"])

        # Simulate Rita leaving home every minute between 08:00–08:59
        for minute in range(60):
            leave_home_time = datetime.strptime(f"08:{minute:02d}:00", "%H:%M:%S")
            arrival_at_zoo = leave_home_time + timedelta(seconds=HOME_TO_STATION)

            # Check if there's any bus she can catch after she arrives at ZOO,
            # and that also gets her to TOOMPARK before the latest acceptable time.
            caught_bus = None
            for bus in buses:
                if bus["ZOO"] >= arrival_at_zoo and bus["TOOMPARK"] <= LATEST_ARRIVAL:
                    caught_bus = bus
                    break

            # If a bus is caught, write its data to the CSV file, else mark her as late
            if caught_bus:
                writer.writerow([
                    leave_home_time.strftime("%H:%M:%S"),
                    caught_bus["bus_id"],
                    caught_bus["ZOO"].strftime("%H:%M:%S"),
                    caught_bus["TOOMPARK"].strftime("%H:%M:%S"),
                    0  # 0 = not late
                ])
            else:
                writer.writerow([
                    leave_home_time.strftime("%H:%M:%S"),
                    "None", "", "", 1  # 1 = late
                ])


# Run the simulation
probability_by_minute()
