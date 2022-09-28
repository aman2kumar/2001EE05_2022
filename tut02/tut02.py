# Importing different modules
from platform import python_version
# A Python library to read/write Excel file
import openpyxl as op

# Loading the given input file in a Workbook
wb = op.load_workbook('input_octant_transition_identify.xlsx')

# Selecting the current active sheet
sheet = wb.active

sheet['E1'] = "U_Avg"  
sheet['F1'] = "V_Avg"
sheet['G1'] = "W_Avg"

# Total rows
row_count = sheet.max_row

# Calculating average by the formula
sheet['E2'] = '= AVERAGE(B2:B' + str(row_count) + ')'
sheet['F2'] = '= AVERAGE(C2:C' + str(row_count) + ')'
sheet['G2'] = '= AVERAGE(D2:D' + str(row_count) + ')'

sheet['H1'] = "U' = U - U_Avg"  
sheet['I1'] = "V' = V - V_Avg"
sheet['J1'] = "W' = W - W_Avg"

# Calculated respective velocities for entire data
for i in range(2, row_count + 1):
    sheet['H' + str(i)] = '= B' + str(i) + ' - E2'
    sheet['I' + str(i)] = '= C{} - F2'.format(i)
    sheet['J' + str(i)] = '= D{} - G2'.format(i)


def octant_transition_count(mod = 5000):
    wb.save("output_octant_transition_identify.xlsx")


ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

mod = 5000
octant_transition_count(mod)