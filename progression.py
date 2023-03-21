import os
import csv
from collections import defaultdict

def read_lif_files(directory):
    lif_data = defaultdict(list)

    for filename in os.listdir(directory):
        if filename.endswith(".lif"):
            with open(os.path.join(directory, filename), "r") as file:
                reader = csv.reader(file)
                row = next(reader)
                event, round_type, heat, *_ = row
                event_heat = (event, heat)
                for row in reader:
                    if row and row[0].isdigit():
                        lif_data[event_heat].append(row)

    return lif_data


def assign_lanes(participants):
    def get_time(participant):
        try:
            return float(participant[5])
        except ValueError:
            return float('inf')

    participants.sort(key=get_time)
    lane_order = [3, 4, 2, 5, 1, 6, 7]
    assigned_lanes = []

    for i, participant in enumerate(participants):
        assigned_lanes.append((lane_order[i], participant))

    return assigned_lanes


def process_race_progression(lif_data):
    progression = defaultdict(lambda: defaultdict(list))

    event_participants = defaultdict(list)
    for event_heat, participants in lif_data.items():
        event, heat = event_heat
        event_participants[event].extend(participants)

    for event_heat, participants in lif_data.items():
        event, heat = event_heat
        num_entries = len(event_participants[event])

        if 8 <= num_entries <= 12:
            top_3 = participants[:3]
            remaining = participants[3:]
        elif 13 <= num_entries <= 14:
            top_3 = participants[:3]
            remaining = participants[3:6]
        elif 15 <= num_entries <= 18:
            top_3 = participants[:2]
            remaining = participants[2:4]
        else:
            top_3 = []
            remaining = []

        progression[event]["final"] += top_3
        progression[event]["petite_final"] += remaining

    return progression


def main():
    directory = "/Users/sevdeneergaard/Venue/LLOP/LYNXOUTPUT"
    lif_data = read_lif_files(directory)
    progression = process_race_progression(lif_data)

    for event, stages in progression.items():
        for stage, participants in stages.items():
            print(f"Event: {event}, {stage}")
            assigned_lanes = assign_lanes(participants)
            for lane, participant in assigned_lanes:
                print(f"ID: {participant[1]}, Lane: {lane}, Last Name: {participant[3]}, First Name: {participant[4]}, Affiliation: {participant[5]}, Time: {participant[6]}")


if __name__ == "__main__":
    main()
