# Whova technical test


### import_agenda.py
The function of this file:
1. Open the Agenda excel file
2. Design two SQLite Database table schemas. sessionTable and subTable, which store agenda information based on type
3. Parse the content of the excel file and store the content in the table

Command:
$> python import_agenda.py agenda.xls

Output:
If the command is invalid, the program will print out "Invalid command, run your program as follow: $> ./import_agenda.py agenda.xls"
Once import the agenda successfully, the program print out "Import the agenda successfully"


### lookup_agenda.py
The function of this file:
1. Parse the command line arguments to retrieve the conditions.
2. Lookup the data you imported for the matching records
3. If you are searching for "speaker", it will return all sessions and sub where we can find this speaker
   If you are searching for onr of "date, time_start, time_end, title, location and description", return exact match
4. Print the result onto the screen

Command:
$> python lookup_agenda column value

Column,Value:
* column can be one of {date, time_start, time_end, title, location, description, speaker}
* value is the expected value for that field  

  
  
### db_table.py
Modification of the file: provide two more features:
* drop
* like

Operation drop used to prevent repeated information when running the import_agenda more than one time
Operation like used for fuzzy search, in this test, used for searching speaker particularly

This can be used as follow:  
from db_table import db_table  
users = db_table("users", { "id": "integer PRIMARY KEY", "speaker": "text", "email": "text NOT NULL UNIQUE" })  
users.like("speaker","John")  
users.drop()  
users.close()  


### What I have done?
* Use library xlrd, copy
* Create two database tables, one for sessions, one for subsessions, 
each subsession has a foreign key session_id to indicate which session it belongs to
* Add two more operations, drop and like
* Filter the input, replace some ' to space as it will cause compile error
* Output all the records as dictionary format and return the number of records which have been found


### Please note:
* The value of description in excel file contains ""(quotation mark), which will cause the compiler to read the 
description as more than one argument, for example:  
The description  "style="color: rgb(34, 34, 34)"; font"  will take "style=" as the first argument instead of the complete sentence.  To solve this you should put a \'\\\' before each " :    

   $> python lookup_agenda.py description "style=\\"color: rgb(34, 34, 34)\\"; font"   

* If the value contains space ‘ ’， for example 'Breakfast ', this is different from 'Breakfast',   
for the provided feature searched on exact match, simply replace the space will cause 'Room 201' to become 'Room201', 
so I didn't make such changes. 
* If the value contains more than one word, for example 'Room 201' and 'Coral Lounge', when searching for these values, 
you should use "value" instead of value
* I have already filter the result which will not contain the repeated records for following situations:  
$> python lookup_agenda.py speaker John    
Title	       Location 	  		    Type                 Speaker   
===========================================================================  
Breakfast    Lounge	            Session              John;Alex  # Returned because its speaker contains John  
Hangout	     Beach	  	        Sub                  John       # Returned because its speaker is John  
Lunch	     Price Center    	Session              John       # Returned because its speaker is John  

### Resources
* [Python SQLite3 documentation](https://docs.python.org/2/library/sqlite3.html)
* [Python Excel parsing](https://github.com/python-excel/xlrd)
