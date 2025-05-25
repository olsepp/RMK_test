# RMK_test
My solution to RMK data team intern test challenge.

# Problem description

Rita works at RMK's Tallinn office and takes city bus number 8 (heading towards Äigrumäe) from the "ZOO" stop to the "TOOMPARK" stop to get to work.
She has a meeting every weekday at 09:05 sharp.

# Goal

Plot the probability of Rita being late depending on what time she leaves home between 08:00 and 09:00.

# Solving steps

NOTE: Data was collected on 23 of May between 08:00 and 09:00, so solution is based on data collected in that time.

1. Fetched live GPS data from https://transport.tallinn.ee/gps.txt, filtering for:
  - bus number 8
  - direction Äigrumäe
  - timeframe 08:00 - 09:00

2. Data Logging Script
   
Created a script that:
  - Checks each bus's coordinates
  - Logs arrival times near "ZOO" and "TOOMPARK" using the Haversine formula to check proximity
  - Writes valid detections to a CSV file

3. Filtering Viable Trips

From the raw data, filtered only those buses that:
  - Departed from ZOO after Rita could reach the stop
  - Arrived at TOOMPARK before 09:01 (latest arrival time considering her 4-minute walk)
  - Wrote this filtered list to a new CSV file

4. Probability Analysis

For every minute between 08:00 and 08:59:
  - Simulated Rita leaving home
  - Checked if there was any bus she could catch and still make it on time
  - Wrote the outcome to a CSV file (probabilities_by_minute.csv), including:
  - Time she left
  - Whether she caught a bus
  - Whether she would be late

5. Visualization

Created a simple graph using matplotlib showing:
  - X-axis: minute after 08:00
  - Y-axis: 0 = on time, 1 = late
  - Exported the graph in JPG format

# Usage

To get the visual chart run main.py.
Used each file to perform steps in process in order to achieve my goal.
Running:
  - get_data.py, get current data for all buses that are number 8 and that are heading towards Äigrumäe.
  - make_schedule.py, waits for time to be 08:00 and runs until 09:00, calls get_data.py to get data for buses and then checks if bus is near one of the stops(ZOO or TOOMPARK). If it is, logs it to CSV file bus_schedule.csv.
  - filter_schedule.py, leaves only bus data where bus was at both stop in the timeframe, also cleans up timestamp making them more readable.
  - data_processing.py, uses filtered schedule to calculate for every minute in timeframe where Rita could leave if she will be late or not. Also calculate which bus Rita could catch for every minute she could leave home. Result are witten in probabilities_by_minute.csv.
  - visualize.py, make a chart to visualize the time Rita leaves her home and probability of her being late or not. Chart is in JPG format.
