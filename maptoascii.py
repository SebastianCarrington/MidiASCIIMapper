# balls 

import glob, py_midicsv as pm
from operator import itemgetter

output_file = open('output.txt', 'w+')

# iterates over every file in the folder and checks whether it is a *.mid file
for file in glob.glob('cum/*.mid'):
    print('Currently processing file ' + file)
    csv = pm.midi_to_csv(file)

    events = []

    # iterates over each line in the csv and adds all of the events to a list
    for line in csv:
        if 'Note' in line:
            line_split = line.split(', ')
            if line_split[2] == 'Note_on_c':
                # note on events
                time = int(line_split[1])
                note = chr(int(line_split[4]))
                velocity = int(line_split[5])

                if velocity == 0:
                    events.append((0, time, note))
                else:
                    events.append((1, time, note))
            elif line_split[2] == 'Note_off_c':
                # note off events
                time = int(line_split[1])
                note = chr(int(line_split[4]))

                events.append((0, time, note))

    # sorts all of the events by time
    # fixes issue of multi-track midi tiles not parsing properly
    # thank fuck for stackoverflow (<https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value>)
    events = sorted(events, key=itemgetter(1))

    current_notes = [' ']
    last_time = 0

    for event in events:
        time = event[1]
        note = event[2]
        times = (time - last_time) + 1

        if event[0] == 1:
            if note not in current_notes:
                current_notes.append(note)
        elif event[0] == 0:
            if note in current_notes:
                current_notes.remove(note)

        for i in range(times):
            for n in current_notes:
                output_file.write(n)

    for i in range(0, 500):
        output_file.write(' ')