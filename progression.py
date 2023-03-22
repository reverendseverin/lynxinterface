import os
import csv
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, ttk

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

        progression[event]["final"] += [(heat, participant) for participant in top_3]
        progression[event]["petite_final"] += [(heat, participant) for participant in remaining]

    return progression

def main(directory, notebook):
    lif_data = read_lif_files(directory)
    progression = process_race_progression(lif_data)

    sorted_events = sorted(progression.items(), key=lambda x: int(x[0].split(" ")[-1]))

    for event, stages in sorted_events:
        if not stages["final"] and not stages["petite_final"]:
            continue

        event_tab = ttk.Frame(notebook)
        notebook.add(event_tab, text=f"Event {event}")

        for index, (stage, participants) in enumerate(stages.items()):
            tree = ttk.Treeview(event_tab, columns=("ID", "Lane", "Last Name", "First Name", "Affiliation", "Time", "Original Heat"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Lane", text="Lane")
            tree.heading("Last Name", text="Last Name")
            tree.heading("First Name", text="First Name")
            tree.heading("Affiliation", text="Affiliation")
            tree.heading("Time", text="Time")
            tree.heading("Original Heat", text="Original Heat")
            tree.grid(row=index, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

            race_type_label = tk.Label(event_tab, text=f"{stage.capitalize()} ({event})", font=("Helvetica", 12, "bold"))
            race_type_label.grid(row=index, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")

            assigned_lanes = assign_lanes([p for _, p in participants])

            for (lane, participant), (original_heat, _) in zip(sorted(assigned_lanes, key=lambda x: x[0]), participants):
                tree.insert("", tk.END, values=(participant[1], lane, participant[3], participant[4], participant[5], participant[6], original_heat))


def browse_button_callback(notebook):
    directory = filedialog.askdirectory()
    main(directory, notebook)


def create_app_window():
    app = tk.Tk()
    app.title("Race Progression Analyzer")

    browse_button = tk.Button(app, text="Select Directory", command=lambda: browse_button_callback(notebook))
    browse_button.pack()

    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill=tk.BOTH)

    app.mainloop()


if __name__ == "__main__":
    create_app_window()