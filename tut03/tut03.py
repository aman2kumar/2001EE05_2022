# Importing different modules
from platform import python_version

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

# DateTime module to measure the execution time of the program
from datetime import datetime
start_time = datetime.now()


# Loading input csv file into a dataframe (df)
file = "input_octant_longest_subsequence.xlsx"
df = pd.read_excel(file)

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


def octant_longest_subsequence_count():
    print("Thinking what to code")
    # code
    # Printing dataframe df
    print(df)

    # Forming csv file from the dataframe
    df.to_excel("output_octant_longest_subsequence.xlsx", index = False)

ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


octant_longest_subsequence_count()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))