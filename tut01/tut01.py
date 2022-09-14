# Importing different modules
from platform import python_version

# Pandas is used for working on datasets
# It is simpler and easy to use
import pandas as pd

def octact_identification(mod = 5000):
    # Loading input csv file into a dataframe (df)
    df = pd.read_csv('C:/Users/DELL/Desktop/Python Course/2001EE05_2022/tut01/octant_input.csv')

    # Calculating averages of U, V and W
    U_avg = df["U"].mean()
    V_avg = df["V"].mean()
    W_avg = df["W"].mean()

    # Done preprocessing by subtracting averages from original U, V and W
    df["U"] = df["U"] - U_avg
    df["V"] = df["V"] - V_avg
    df["W"] = df["W"] - W_avg


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000
octact_identification(mod)