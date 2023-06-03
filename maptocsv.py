# penis

import os, py_midicsv as pm

try:
    os.remove("./csv.txt")
except:
    print("oh no")

input_file = open("./output.txt", "r+")
output_file = open("./csv.txt", "w+")

output_file.write("0, 0, Header, 1, 1, 50\n")
output_file.write("1, 0, Start_track\n")

lines = input_file.readlines()

last_notes = []
current_notes = []
for line in range(1, len(lines)):
    notes = [*lines[line - 1].strip("\n")]
    try:
        next_notes = [*lines[line + 1].strip("\n")]
    except:
        next_notes = []
    for note in notes:
        if not (note in last_notes) and note != " ":
            output_file.write(
                "1, " + str(line) + ", Note_on_c, 1, " + str(ord(note)) + ", 81\n"
            )
        elif not (note in next_notes) and note != " ":
            output_file.write(
                "1, " + str(line) + ", Note_off_c, 1, " + str(ord(note)) + ", 0\n"
            )
    last_notes = notes


output_file.write("1, " + str(len(lines)) + ", End_track\n")
output_file.write("0, 0, End_of_file")
