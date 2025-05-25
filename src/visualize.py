import csv
import matplotlib.pyplot as plt
import os


def make_visualization():
    """
    Make visual chart in JPG format of the time Rita has to leave to make the meeting in time.
    :return: None
    """
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "probabilities_by_minute.csv")
    # Load data
    minutes = []
    late_probability = []

    # Open CSV file to read
    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_str = row["leave_home_at"]  # type: ignore
            minute = int(time_str.split(":")[1])  # Extract just the minute part
            minutes.append(minute)
            late_probability.append(int(row["late"]))  # type: ignore  # 0 = on time, 1 = late

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(minutes, late_probability, drawstyle="steps-post", marker="o", color="darkred")

    # Beautify the chart
    plt.title("Probability of Rita Being Late vs. Departure Minute")
    plt.xlabel("Minute after 08:00")
    plt.ylabel("Late (1 = Late, 0 = On Time)")
    plt.xticks(range(0, 60, 2))  # Show every 2nd minute for clarity
    plt.yticks([0, 1], ["On Time", "Late"])
    plt.grid(True)

    # Save as JPG
    plt.tight_layout()
    plt.savefig("rita_lateness_chart.jpg", format="jpg", dpi=300)


