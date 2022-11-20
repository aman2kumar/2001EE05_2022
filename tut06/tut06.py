# Importing different modules
from platform import python_version
import jinja2

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

# DateTime module to measure the execution time of the program
import datetime
start_time = datetime.datetime.now()

# Python code to illustrate Sending mail with attachments from your Gmail account 
# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

consolidate_df = pd.DataFrame()
# Main function to find attendance report
def attendance_report():
    # Loop for each student
    for i in range(total_studs):
        # Temp dataframe for individual student in this
        roll_df = pd.DataFrame()
        df = att_df[att_df["Roll No"] == stud_df.at[i, "Roll No"]]
        consolidate_df.at[i, "Roll"] = stud_df.at[i, "Roll No"]
        consolidate_df.at[i, "Name"] = stud_df.at[i, "Name"]
        length = len(df.axes[0])
        total_attendance_count = []
        real = []
        duplicate = []
        invalid = []
        total_real = 0
        # absent = 1 if real = 0 else 0
        roll_df.at[0, "Date"] = None
        for j in range(len(lecture_dates)):
            roll_df.at[j + 1, "Date"] = lecture_dates[j]
            total_attendance_count.append(0)
            real.append(0)
            duplicate.append(0)
            invalid.append(0)
            for k in range(length):
                if df.loc[df.index[k], "Timestamp"].date() == lecture_dates[j]:
                    total_attendance_count[j] += 1
                    if(df.loc[df.index[k], "Timestamp"].time() >= class_start_time and df.loc[df.index[k], "Timestamp"].time() <= class_end_time):
                        if real[j] == 0:
                            real[j] = 1
                        else:
                            duplicate[j] += 1
                    else:
                        invalid[j] += 1
        roll_df.at[0, "Roll"] = stud_df.at[i, "Roll No"]
        roll_df.at[0, "Name"] = stud_df.at[i, "Name"]
        roll_df.at[0, "Total Attendance Count"] = None
        roll_df.at[0, "Real"] = None
        roll_df.at[0, "Duplicate"] = None
        roll_df.at[0, "Invalid"] = None
        roll_df.at[0, "Absent"] = None
        for j in range(len(lecture_dates)):
            total_real += real[j]
            roll_df.at[j + 1, "Total Attendance Count"] = total_attendance_count[j]
            roll_df.at[j + 1, "Real"] = real[j]
            roll_df.at[j + 1, "Duplicate"] = duplicate[j]
            roll_df.at[j + 1, "Invalid"] = invalid[j]
            if real[j] == 1:
                roll_df.at[j + 1, "Absent"] = 0
                consolidate_df.at[i, f"{lecture_dates[j]}"] = "P"
            else:
                roll_df.at[j + 1, "Absent"] = 1
                consolidate_df.at[i, f"{lecture_dates[j]}"] = "A"
        roll_df.to_excel(f'output/{stud_df.at[i, "Roll No"]}.xlsx', index = False)
        consolidate_df.at[i, "Actual Lecture Taken"] = len(lecture_dates)
        consolidate_df.at[i, "Total Real"] = total_real
        consolidate_df.at[i, "% Attendance"] = float("%.2f"%((total_real/len(lecture_dates))*100))
    consolidate_df.to_excel('output/attendance_report_consolidated.xlsx', index = False)

   
fromaddr = "EMAIL address of the sender" # Please change accordingly
toaddr = "EMAIL address of the reciever" # Please change accordingly
   
# instance of MIMEMultipart
msg = MIMEMultipart()
  
# storing the senders email address  
msg['From'] = fromaddr
  
# storing the receivers email address 
msg['To'] = toaddr
  
# storing the subject 
msg['Subject'] = "Subject of the Mail"
  
# string to store the body of the mail
body = "Body_of_the_mail"
  
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
  
# open the file to be sent 
filename = "attendance_report_consolidated.xlsx" # "File_name_with_extension"
attachment = open("output/attendance_report_consolidated.xlsx", "rb")
  
# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')
  
# To change the payload into encoded form
p.set_payload((attachment).read())
  
# encode into base64
encoders.encode_base64(p)
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  
# attach the instance 'p' to instance 'msg'
msg.attach(p)
  
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
s.starttls()
  
# Authentication
s.login(fromaddr, "Password_of_the_sender") # Please set the application level password according to sender's email
  
# Converts the Multipart msg into a string
text = msg.as_string()
  
# sending the mail
s.sendmail(fromaddr, toaddr, text)
  
# terminating the session
s.quit()
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

attendance_report()

#This shall be the last lines of the code.
end_time = datetime.datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
