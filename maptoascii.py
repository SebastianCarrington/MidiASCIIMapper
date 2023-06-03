# balls

import os, py_midicsv as pm
from operator import itemgetter


try:
    os.remove("./output.txt")
except:
    print("oh no")
output_file = open("./output.txt", "w+")

# iterates over every file in the folder and checks whether it is a *.mid file
directory = os.listdir("cum")
for file in directory:
    print("Currently processing file " + file)
    try:
        csv = pm.midi_to_csv("cum/" + file)
    except Exception:
        print("oops")

    events = []

    # iterates over each line in the csv and adds all of the events to a list
    for line in csv:
        if "Note" in line:
            line_split = line.split(", ")
            if line_split[2] == "Note_on_c":
                # note on events
                time = int(line_split[1])
                note = chr(int(line_split[4]))
                velocity = int(line_split[5])

                if velocity == 0:
                    events.append((0, time, note))
                else:
                    events.append((1, time, note))
            elif line_split[2] == "Note_off_c":
                # note off events
                time = int(line_split[1])
                note = chr(int(line_split[4]))

                events.append((0, time, note))

    # sorts all of the events by time
    # fixes issue of multi-track midi tiles not parsing properly
    # thank fuck for stackoverflow (<https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value>)
    events = sorted(events, key=itemgetter(1))

    current_notes = []
    last_time = 0
    line_break = 0

    for event in events:
        time = event[1]
        note = event[2]
        times = int(((time - last_time) + 1) / 5)

        for i in range(times):
            if len(current_notes) == 0:
                output_file.write(" ")
            for n in current_notes:
                output_file.write(n)
            output_file.write("\n")

        if event[0] == 1:
            if note not in current_notes:
                current_notes.append(note)
        elif event[0] == 0:
            if note in current_notes:
                current_notes.remove(note)

        line_break += 1
        last_time = time

        # print(current_notes)

    for i in range(0, 100):
        output_file.write("\n")
