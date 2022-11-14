# Importing different modules
from platform import python_version
import jinja2

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

# DateTime module to measure the execution time of the program
import datetime
start_time = datetime.datetime.now()

try:
    # Loading input file into a dataframe (df)
    att_df = pd.read_csv("input_attendance.csv")
    stud_df = pd.read_csv("input_registered_students.csv")
    # Above line can have error if input file has wrong format
    # other than .csv

except Exception as e: 
    print("There was some error due to " + str(e))

# os.mkdir('output')
# Finding the total rows in each dataframe
total_studs = len(stud_df.axes[0])
total_attendance = len(att_df.axes[0])

# Making an empty list of containing all the valid lecture dates
lecture_dates = []

# Converting the original df's timestamp to datetime in appropriate format
att_df["Timestamp"] = pd.to_datetime(att_df["Timestamp"], format = '%d-%m-%Y %H:%M')

# Initialising start and end date with some garbage value
start_date = datetime.datetime.strptime("01/01/2017", '%d/%m/%Y')
end_date    = datetime.datetime.strptime("01/01/2017", '%d/%m/%Y')

# Storing first valid date from df to start date
for i in range(total_attendance):
    if att_df.at[i, "Timestamp"].weekday() == 0 or att_df.at[i, "Timestamp"].weekday() == 3:
        start_date = att_df.at[i, "Timestamp"].date()
        break

# Storing last valid date from df to end date  
for i in range(total_attendance):
    if att_df.at[total_attendance - i - 1, "Timestamp"].weekday() == 0 or att_df.at[total_attendance - i - 1, "Timestamp"].weekday() == 3:
        end_date = att_df.at[total_attendance - i - 1, "Timestamp"].date()
        break

# Now below code is to store all valid dates starting from start to end date in the list
if start_date.weekday() == 0:
    mon = start_date
    thur = start_date + datetime.timedelta(days = 3)
else:
    mon = start_date + datetime.timedelta(days = 4)
    thur = start_date

while mon <= end_date:
    lecture_dates.append(mon)
    mon += datetime.timedelta(days = 7)

while thur <= end_date:
    lecture_dates.append(thur)
    thur += datetime.timedelta(days = 7)


# Splitting one column of attendance dataframe to separate names and roll numbers and storing them in 2 diff columns
student = att_df["Attendance"].str.split(" ", n = 1, expand = True)
att_df["Roll No"] = student[0]
att_df["Name"] = student[1]

# Defining class start and end time
class_start_time = datetime.datetime.strptime('14:00', '%H:%M').time()
class_end_time = datetime.datetime.strptime('15:00', '%H:%M').time()

# Sorting lecture dates list
lecture_dates.sort()

# Main function to find attendance report
def attendance_report():
    pass

ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

attendance_report()

#This shall be the last lines of the code.
end_time = datetime.datetime.now()
print('Duration of Program Execution: {}'.format(start_time - end_time))
