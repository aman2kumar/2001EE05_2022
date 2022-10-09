# Importing different modules
from platform import python_version

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

# DateTime module to measure the execution time of the program
from datetime import datetime
start_time = datetime.now()

# Function to find the octant value and label it for a particular row
# taken row as an input
def label_octant (row):
    if row["U' = U - U_avg"] >= 0 and row["V' = V - V_avg"] >= 0 and row["W' = W - W_avg"] >= 0:
        return 1
    elif row["U' = U - U_avg"] < 0 and row["V' = V - V_avg"] >= 0 and row["W' = W - W_avg"] >= 0:
        return 2
    elif row["U' = U - U_avg"] < 0 and row["V' = V - V_avg"] < 0 and row["W' = W - W_avg"] >= 0:
        return 3
    elif row["U' = U - U_avg"] >= 0 and row["V' = V - V_avg"] < 0 and row["W' = W - W_avg"] >= 0:
        return 4
    elif row["U' = U - U_avg"] >= 0 and row["V' = V - V_avg"] >= 0 and row["W' = W - W_avg"] < 0:
        return -1
    elif row["U' = U - U_avg"] < 0 and row["V' = V - V_avg"] >= 0 and row["W' = W - W_avg"] < 0:
        return -2
    elif row["U' = U - U_avg"] < 0 and row["V' = V - V_avg"] < 0 and row["W' = W - W_avg"] < 0:
        return -3
    elif row["U' = U - U_avg"] >= 0 and row["V' = V - V_avg"] < 0 and row["W' = W - W_avg"] < 0:
        return -4

try:
    # Loading input file into a dataframe (df)
    file = "input_octant_longest_subsequence_with_range.xlsx"
    df = pd.read_excel(file)
    # Above line can have error if input file has wrong format
    # other than .xlsx

except Exception as e:  # Exception = openpyxl.utils.exceptions.InvalidFileException
    print("There was some error due to " + str(e))

# Calculating averages of U, V and W
U_avg = df["U"].mean()
V_avg = df["V"].mean()
W_avg = df["W"].mean()

# Adding Columns of respective averages calculated above in first row
df.loc[df.index[0], 'U Avg'] = U_avg
df.loc[df.index[0], 'V Avg'] = V_avg
df.loc[df.index[0], 'W Avg'] = W_avg

# Done preprocessing by subtracting averages from original U, V and W
# and forming new columns respectively
df["U' = U - U_avg"] = df["U"] - U_avg
df["V' = V - V_avg"] = df["V"] - V_avg
df["W' = W - W_avg"] = df["W"] - W_avg

def octant_longest_subsequence_count_with_range():
    # Printing dataframe df
    print(df)

    try:
        # Forming excel file from the dataframe
        df.to_excel("output_octant_longest_subsequence_with_range.xlsx", index = False)
        # Above line can have error if the workbook has already been saved

    except Exception as e:  # Exception
        print("There was some error due to " + str(e))


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count_with_range()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
