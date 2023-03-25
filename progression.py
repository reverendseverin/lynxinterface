import os
import csv
import logging
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog, ttk

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    lane_order = [3, 4, 2, 5, 1, 6]
    assigned_lanes = []

    for index, participant in enumerate(participants):
        lane = lane_order[index % len(lane_order)]
        assigned_lanes.append((*participant, lane))

    return assigned_lanes


def copy_to_clipboard(tree, app):
    rows = tree.get_children()
    data = []

    for row in rows:
        values = tree.item(row)["values"]
        data.append(",".join(str(v) for v in values))

    csv_data = "\n".join(data)
    app.clipboard_clear()
    app.clipboard_append(csv_data)
    print("Table data copied to clipboard")

def create_copy_button(event, event_tab, app):
    tree = None
    for child in event_tab.winfo_children():
        if isinstance(child, ttk.Treeview):
            tree = child
            break

    if tree is not None:
        copy_button = tk.Button(event_tab, text="Copy to Clipboard", command=lambda: copy_to_clipboard(tree, app))
        copy_button.pack(pady=(0, 10))


def process_race_progression(lif_data):
    progression = defaultdict(lambda: defaultdict(list))

    event_participants = defaultdict(list)
    for event_heat, participants in lif_data.items():
        event, heat = event_heat
        for participant in participants:  # Add this loop
            participant.append(heat)  # Add heat number to each participant
        event_participants[event].extend(participants)

    for event, all_participants in event_participants.items():
        # Combine and sort participants from all heats of the event
        combined_participants = sorted(all_participants, key=lambda x: (x[-1], int(x[0])))  # Sort by heat and place

        
        num_entries = len(combined_participants)

        if 8 <= num_entries <= 12:
            final_participants = combined_participants[:6]
            petite_final_participants = combined_participants[6:]
        elif 13 <= num_entries <= 14:
            final_participants = combined_participants[:6]
            petite_final_participants = combined_participants[6:12]
        elif 15 <= num_entries <= 18:
            final_participants = combined_participants[:6]
            petite_final_participants = combined_participants[6:12]
        else:
            final_participants = []
            petite_final_participants = []

        # Assign lanes for final and petite final participants
        assigned_final_lanes = assign_lanes(final_participants)
        assigned_petite_final_lanes = assign_lanes(petite_final_participants)

        progression[event]["final"] += assigned_final_lanes
        progression[event]["petite_final"] += assigned_petite_final_lanes

    return progression



def main(directory, notebook, app):
    lif_data = read_lif_files(directory)
    progression = process_race_progression(lif_data)

    sorted_events = sorted(progression.items(), key=lambda x: int(x[0].split(" ")[-1]))

    for event, stages in sorted_events:
        if not stages["final"] and not stages["petite_final"]:
            continue

        event_tab = ttk.Frame(notebook)
        notebook.add(event_tab, text=f"Event {event}")

        for stage, participants in stages.items():
            tree = ttk.Treeview(event_tab, columns=("ID", "Lane", "Last Name", "First Name", "Affiliation", "Time", "Heat"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Lane", text="Lane")
            tree.heading("Last Name", text="Last Name")
            tree.heading("First Name", text="First Name")
            tree.heading("Affiliation", text="Affiliation")
            tree.heading("Time", text="Time")
            tree.heading("Heat", text="Heat")
            race_type_label = tk.Label(event_tab, text=f"{stage.capitalize()} ({event})", font=("Helvetica", 12, "bold"))
            race_type_label.pack(padx=(10, 0), pady=(0, 10))
            tree.pack(padx=(10, 0), pady=(10, 0), fill=tk.BOTH, expand=True)
            tree._name = event + "_tree"  # Assign a unique name to the tree

            for participant in sorted(participants, key=lambda x: x[-1]):
                tree.insert("", tk.END, values=(participant[1], participant[-1], participant[3], participant[4], participant[5], participant[6], participant[-2]))  # Use participant[-2] for Original Heat


            create_copy_button(event, event_tab, app)

def browse_button_callback(notebook, app):
    directory = filedialog.askdirectory()
    main(directory, notebook, app)


def create_app_window():
    app = tk.Tk()
    app.title("Race Progression Analyzer")

    browse_button = tk.Button(app, text="Select Directory", command=lambda: browse_button_callback(notebook, app))
    browse_button.pack()

    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill=tk.BOTH)

    app.mainloop()


if __name__ == "__main__":
    create_app_window()