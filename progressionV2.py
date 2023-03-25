import os
import csv
from tkinter import *


def read_lif_files(directory):
    lif_data = []
    for file in os.listdir(directory):
        if file.endswith('.lif'):
            with open(os.path.join(directory, file), 'r') as lif_file:
                reader = csv.reader(lif_file)
                lif_data.extend([row for row in reader if row])
    return lif_data



def define_race_progression(lif_data):
    heats = {}
    for row in lif_data:
        if row[0].isdigit() and row[2]:
            heat = int(row[2].strip())
            if heat not in heats:
                heats[heat] = []
            heats[heat].append(row)

    num_entries = sum(len(entries) for entries in heats.values())

    final = []
    petite_final = []

    if 8 <= num_entries <= 12:
        for heat_entries in heats.values():
            final.extend(heat_entries[:3])
            petite_final.extend(heat_entries[3:])
    elif 13 <= num_entries <= 14:
        for heat_entries in heats.values():
            final.extend(heat_entries[:3])
            petite_final.extend(heat_entries[3:6])
    elif 15 <= num_entries <= 18:
        for heat_entries in heats.values():
            final.extend(heat_entries[:2])
            petite_final.extend(heat_entries[2:4])

    return final, petite_final




def output_to_table(final, petite_final):
    root = Tk()
    root.title("Race Progression")
    
    header = ["Place", "ID", "Lane", "Last Name", "First Name", "Affiliation", "Time", "License", "Delta Time", "ReacTime", "Splits", "Time Trial Start Time", "User 1", "User 2", "User 3"]
    
    for idx, entry in enumerate([header] + final + petite_final, 1):
        for j, value in enumerate(entry):
            cell = Label(root, text=value, borderwidth=1, relief="solid", padx=5, pady=5)
            cell.grid(row=idx, column=j)

    root.mainloop()



if __name__ == "__main__":
    lif_directory = "/Users/sevdeneergaard/Venue/LLOP/LYNXOUTPUT"
    lif_data = read_lif_files(lif_directory)
    final, petite_final = define_race_progression(lif_data)
    output_to_table(final, petite_final)
