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
    file = "octant_input.xlsx"
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

octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", 
"3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}

# Original function for octant identification
def octant_range_names(mod = 5000):

    # Adding Column of User Input at respective value of row and column
    df.at[2, ''] = 'User Input'

    # Adding value of mod at respective row and column
    df.at[2, 'Octant ID'] = 'Mod ' + str(mod)

    # Calculated total rows in dataframe to get the iteration of the for loop
    total_rows = len(df.axes[0])
    iteration = int(total_rows/mod)

    octant = [1, -1, 2, -2, 3, -3, 4, -4]
    overall_count = []

    # Added the total count of different octant values in their respective columns
    # ex- count_1 = len of dataframe df_range whose Octant value == 1
    # axes[0] => 0 corresponds to rows
    df.at[1, 'Octant ID'] = 'Overall Count'
    for i in range(8):
        count = len((df[df["Octant"] == octant[i]]).axes[0])
        df.at[1, str(octant[i])] = count
        overall_count.append([count, i + 1])

    for i in range(8):
        df.at[0, 'Rank ' + str(i + 1)] = octant[i]

    overall_count.sort(reverse = True)
    for i in range(8):
        for j in range(8):
            if overall_count[j][1] == i + 1:
                df.at[1, 'Rank ' + str(i + 1)] = j + 1
                df.at[1, 'Rank 1 Octant ID'] = octant[overall_count[0][1] - 1]
                df.at[1, 'Rank 1 Octant Name'] = octant_name_id_mapping.get(str(octant[overall_count[0][1] - 1]))
                break

    # For loop to give the count of octants in the ranges of given mod value
    for i in range(iteration + 1):

        # Divided original dataframe in range based on no. of loops
        # ex- for loop1 range = 0 to 5000, loop2 range = 5001 to 10000 and so on..
        df_range = df[i*mod: (i + 1)*mod - 1]
        mod_count = []

        for j in range(8):
            count_mod = len((df_range[df_range["Octant"] == octant[j]]).axes[0])
            df.at[i + 3, str(octant[j])] = count_mod
            mod_count.append([count_mod, j + 1])

        mod_count.sort(reverse = True)
        for j in range(8):
            for k in range(8):
                if mod_count[k][1] == j + 1:
                    df.at[i + 3, 'Rank ' + str(j + 1)] = k + 1
                    df.at[i + 3, 'Rank 1 Octant ID'] = octant[mod_count[0][1] - 1]
                    df.at[i + 3, 'Rank 1 Octant Name'] = octant_name_id_mapping.get(str(octant[mod_count[0][1] - 1]))   
                    break
    
        # Defined range based on loop value
        # For last loop range = i*mod to total_rows else shown below
        if i != int(iteration):
            df.at[i + 3, 'Octant ID'] = str(i*mod) + ' - ' + str((i+1)*mod - 1)
        else:
            df.at[i + 3, 'Octant ID'] = str(i*mod) + ' - ' + str(total_rows)

    df.at[iteration + 7, '1'] = 'Octant ID'
    df.at[iteration + 7, '-1'] = 'Octant Name'
    df.at[iteration + 7, '2'] = 'Count of Rank 1 Mod Values'
    for i in range(8):
        df.at[iteration + 8 + i, '1'] = octant[i]
        df.at[iteration + 8 + i, '-1'] = octant_name_id_mapping.get(str(octant[i]))
        if(i == 2):
            df.at[iteration + 8 + i, '2'] = len((df[df["Rank 1 Octant ID"] == octant[i]]).axes[0]) - 1
        else:
            df.at[iteration + 8 + i, '2'] = len((df[df["Rank 1 Octant ID"] == octant[i]]).axes[0])


    try:
        # Forming excel file from the dataframe
        df.to_excel("octant_output_ranking_excel.xlsx", index = False)
        # Above line can have error if the workbook has already been saved

    except Exception as e:  # Exception
        print("There was some error due to " + str(e))
    

ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


mod = 5000 
octant_range_names(mod)



# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
