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
    # Loading input csv file into a dataframe (df)
    file = "input_octant_longest_subsequence.xlsx"
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

# Constructing a new column of Octant and applying logic given below
# Using lambda function on a particular row to find its octant via pre defined function (label_octant())
df["Octant"] = df.apply(lambda row: label_octant(row), axis = 1)

# Adding an empty column as shown in the given output file
df[""] = ""

# Calculating total rows
total_rows = len(df.axes[0])

# Original function to find octant longest subsequence count
def octant_longest_subsequence_count():
    # Defining Lists for different values of subsequence length for their respective octant values
    octant_values = [+1, -1, +2, -2, +3, -3, +4, -4]
    subsequence_length = [0, 0, 0, 0, 0, 0, 0, 0]
    max_subsequence_length = [-1, -1, -1, -1, -1, -1, -1, -1]
    temp_subsequence_length = [0, 0, 0, 0, 0, 0, 0, 0]
    max_subsequence_count = [0, 0, 0, 0, 0, 0, 0, 0]

    # Iteration for each row
    for i in range(total_rows - 1):

        # Iteration for each octant values
        for j in range(8):

            # If the value of Octant at index i == any octant values in the List
            if(df.loc[df.index[i], 'Octant'] == octant_values[j]):
                # Then check for next octant value
                if(df.loc[df.index[i + 1], 'Octant'] == octant_values[j] and i != total_rows - 2):
                    # if it is equal to previous octant value
                    # increment subsequence length by 1
                    subsequence_length[j] += 1
                else:
                    # else set subsequence length to 0
                    subsequence_length[j] = 0

                # define max subseq length as the maximum of the two
                max_subsequence_length[j] = max(max_subsequence_length[j], subsequence_length[j])
                break

    # Repeating the same loop this time to find the count of max subsequence length in the entire dataframe
    for i in range(total_rows - 1):
        for j in range(8):
            if(df.loc[df.index[i], 'Octant'] == octant_values[j]):
                if(df.loc[df.index[i + 1], 'Octant'] == octant_values[j] and i != total_rows - 2):
                    # This time storing the suseq length in temp_subsequence_length
                    temp_subsequence_length[j] += 1
                else:
                    # This time comparing the temp subseq length with the max subseq length
                    if(temp_subsequence_length[j] == max_subsequence_length[j]):
                        # If equals then, incrementing the count 
                        max_subsequence_count[j] += 1
                    temp_subsequence_length[j] = 0
                break


    # Printing the calculated max suseq length and its count in the respective cells
    for i in range(8):
        df.loc[df.index[i], 'Octant No'] = str(octant_values[i])
        # Added 1 to the value because a single occurence also has the length 1
        df.loc[df.index[i], 'Longest Subsequence Length'] = max_subsequence_length[i] + 1
        df.loc[df.index[i], 'Count'] = max_subsequence_count[i]

    # Printing dataframe df
    print(df)

    try:
        # Forming csv file from the dataframe
        df.to_excel("output_octant_longest_subsequence.xlsx", index = False)
        # Above line can have error if the workbook has already been saved

    except Exception as e:  # Exception
        print("There was some error due to " + str(e))

ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))