# Importing different modules
from platform import python_version

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

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

# Original function for octant identification
def octact_identification(mod = 5000):
    # Loading input csv file into a dataframe (df)
    df = pd.read_csv('C:/Users/DELL/Desktop/Python Course/2001EE05_2022/tut01/octant_input.csv')

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

    # Adding Column of User Input
    df.at[1, 11] = 'User Input'

    # Calculated total rows in dataframe to get the iteration of the for loop
    total_rows = len(df.axes[0])
    iteration = total_rows/mod

    # For loop to give the count of octants in the ranges of given mod value
    for i in range(int(iteration) + 1):

        # Divided original dataframe in range based on no. of loops
        # ex- for loop1 range = 0 to 5000, loop2 range = 5001 to 10000 and so on..
        df_range = df[i*mod: (i + 1)*mod]

        # Calculated counts of different octant values for particular range
        count_1 = len((df_range[df_range["Octant"] == 1]).axes[0])
        count_neg1 = len((df_range[df_range["Octant"] == -1]).axes[0])
        count_2 = len((df_range[df_range["Octant"] == 2]).axes[0])
        count_neg2 = len((df_range[df_range["Octant"] == -2]).axes[0])
        count_3 = len((df_range[df_range["Octant"] == 3]).axes[0])
        count_neg3 = len((df_range[df_range["Octant"] == -3]).axes[0])
        count_4 = len((df_range[df_range["Octant"] == 4]).axes[0])
        count_neg4 = len((df_range[df_range["Octant"] == -4]).axes[0])

        # Added the value of counts in respective rows and columns 
        df.at[i + 2, 'Octant ID'] = str(i*mod) + ' - ' + str((i+1)*mod)
        df.at[i + 2, '1'] = count_1
        df.at[i + 2, '-1'] = count_neg1
        df.at[i + 2, '2'] = count_2
        df.at[i + 2, '-2'] = count_neg2
        df.at[i + 2, '3'] = count_3
        df.at[i + 2, '-3'] = count_neg3
        df.at[i + 2, '4'] = count_4
        df.at[i + 2,'-4'] = count_neg4

    # Printing dataframe df
    print(df)

    # Forming csv file from the dataframe
    df.to_csv('octant_output.csv', index = False)


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000
octact_identification(mod)