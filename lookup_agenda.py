import sys
import import_agenda
import copy

valid_columns = ["date", "time_start", "time_end", "type", "title", "location", "description", "speaker"]

# checks for proper input
if len(sys.argv) == 3:
    column = str(sys.argv[1])
    value = str(sys.argv[2])
else:
    print("Invalid command, run your program as follow: ./lookup_agenda.py column value")
    sys.exit(1)

# check the input
if column not in valid_columns:
    print("Invalid column, it must be one of the [date, time_start, time_end, title, location, description, speaker]")
    sys.exit(1)

# check the input
value = value.replace("'", "")

# if look up for speaker,
if column == "speaker":
    selected = import_agenda.sessionTable.like(col=column, val=value)
    all_session = copy.deepcopy(selected)
    allsubs = []
    for x in all_session:
        allsubs.extend(import_agenda.subTable.select(where={"session_id": x["id"]}))

    sub = import_agenda.subTable.like(col=column, val=value)
    for i in sub:
        if i not in allsubs:
            allsubs.append(i)
    selected.extend(allsubs)
else:
    selected = import_agenda.sessionTable.select(where={column: value})
    all_sessions = copy.deepcopy(selected)
    allsubs = []
    for x in all_sessions:
        allsubs.extend(import_agenda.subTable.select(where={"session_id": x["id"]}))
    sub = import_agenda.subTable.select(where={column: value})
    for i in sub:
        if i not in allsubs:
            allsubs.append(i)
    selected.extend(allsubs)

for x in selected:
    print(x)
    print("---------------------")

# show the count of records being found
print("%d results found." % len(selected))

