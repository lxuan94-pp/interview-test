import db_table as db
import xlrd
import sys

sessionTable = db.db_table("Session",
                           {"id": "text PRIMARY KEY", "date": "text", "time_start": "text", "time_end": "text",
                            "type": "text", "title": "text", "location": "text", "description": "text",
                            "speaker": "text"})
subTable = db.db_table("Sub",
                       {"id": "text PRIMARY KEY", "session_id": "text", "date": "text", "time_start": "text",
                        "time_end": "text", "type": "text", "title": "text", "location": "text", "description": "text",
                        "speaker": "text"})

if __name__ == '__main__':

    # read the excel file
    if len(sys.argv) == 2:
        fileName = str(sys.argv[1])
    else:
        print("Invalid command, run your program as follow: $> ./import_agenda.py agenda.xls")
        sys.exit(1)

    # open the file
    workbook = xlrd.open_workbook(fileName)
    worksheet = workbook.sheet_by_index(0)

    # to prevent the repeat data when run import_agenda.py for more than one time
    sessionTable.drop()
    subTable.drop()

    # create the table to load new data/ create the table
    sessionTable = db.db_table("Session",
                               {"id": "text PRIMARY KEY", "date": "text", "time_start": "text", "time_end": "text",
                                "type": "text", "title": "text", "location": "text", "description": "text",
                                "speaker": "text"})
    subTable = db.db_table("Sub",
                           {"id": "text PRIMARY KEY", "session_id": "text", "date": "text", "time_start": "text",
                            "time_end": "text", "type": "text", "title": "text", "location": "text",
                            "description": "text",
                            "speaker": "text"})

    rows = worksheet.nrows
    cols = worksheet.ncols
    # define the variable as follows: {date, time_start, time_end, title, location, description, speaker}
    # s_id, sub_id are defined as auto_increment primary key in db, s_type used to differ session and sub
    s_id = '0'
    sub_id = '0'
    date = ''
    time_start = ''
    time_end = ''
    s_type = ''
    title = ''
    location = ''
    description = ''
    speaker = ''

    # check the input and insert the data into different tables
    for y in range(15, rows):
        dates = worksheet.cell_value(y, 0)
        time_start = worksheet.cell_value(y, 1)
        time_end = worksheet.cell_value(y, 2)
        s_type = worksheet.cell_value(y, 3)
        title = worksheet.cell_value(y, 4)
        title = title.replace("'", "")
        rooms = worksheet.cell_value(y, 5)
        description = worksheet.cell_value(y, 6)
        description = description.replace("'", "")
        speaker = worksheet.cell_value(y, 7)
        speaker = speaker.replace("'", "")
        if s_type == "Session":
            sub_id = '0'
            s_id = str(int(s_id) + 1)
            sessionTable.insert(
                {"id": s_id, "date": dates, "time_start": time_start, "time_end": time_end, "type": s_type,
                 "title": title, "location": rooms, "description": description, "speaker": speaker})

        else:
            sub_id = str(int(sub_id) + 1)
            cur = s_id + '-' + sub_id
            # the primary key looks like '1-1','1-2','2-1'
            subTable.insert({"id": cur, "session_id": s_id, "date": dates, "time_start": time_start,
                             "time_end": time_end, "type": s_type, "title": title, "location": rooms,
                             "description": description, "speaker": speaker})
    print("Import the agenda successfully")
