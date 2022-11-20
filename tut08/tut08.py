import pandas as pd
import re
from datetime import datetime
start_time = datetime.now()

text = open("india_inns2.txt", "r").read()

ind_inns = []
for line in text.split('\n'):
	if line != "":
		ind_inns.append(line)

total_balls = len(ind_inns)
line = []
for i in range(total_balls):
	line.append(ind_inns[i].split(','))

for i in range(total_balls):
	ball, commentary = line[i][0].split(' ', 1)
	line[i][0] = ball 
	line[i].insert(1, commentary)

indBatter = []
pakBaller = []
for i in range(total_balls):
	player = line[i][1].split('to')
	line[i][1] = player[0]
	line[i].insert(2, player[1])
	indBatter.append(player[1])
	pakBaller.append(player[0])

indBatter = list(dict.fromkeys(indBatter))
pakBaller = list(dict.fromkeys(pakBaller))
indBatting = pd.DataFrame(0, indBatter, ["Status", "R", "B", "4s", "6s", "SR"])
pakBalling = pd.DataFrame(0, pakBaller, ["O", "M", "R", "W", "NB", "WD", "ECO"])

extra = 0
wide = 0
score = 0
wkts = 0
noBall = 0
bye = 0
legBye = 0

for i in range(total_balls):
	batter = line[i][2]
	baller = line[i][1]
	line[i][3] = line[i][3].lower()
	if "wide" in line[i][3]:
		temp = re.findall("[0-9]", line[i][3])
		if len(temp) == 0:
			wide += 1
			score += 1
			pakBalling.loc[baller, "R"] += 1
			pakBalling.loc[baller, "WD"] += 1
		else:
			wide += int(temp[0])
			print(temp)
			score += int(temp[0])
			pakBalling.loc[baller, "R"] += int(temp[0])
			pakBalling.loc[baller, "WD"] += int(temp[0])
		
	elif line[i][3] == " no ball":
		noBall += 1
		score += 1
		pakBalling.loc[baller, "R"] += 1
		pakBalling.loc[baller, "NB"] += 1
	elif line[i][3] == " four" or line[i][3] == " 4" or line[i][3] == " 4 runs":
		score += 4
		indBatting.loc[batter, "R"] += 4
		indBatting.loc[batter, "B"] += 1
		indBatting.loc[batter, "4s"] += 1
		pakBalling.loc[baller, "R"] += 4
		pakBalling.loc[baller, "O"] += 1
	elif line[i][3] == " six" or line[i][3] == " 6" or line[i][3] == " 6 runs":
		score += 6
		indBatting.loc[batter, "R"] += 6
		indBatting.loc[batter, "B"] += 1
		indBatting.loc[batter, "6s"] += 1
		pakBalling.loc[baller, "R"] += 6
		pakBalling.loc[baller, "O"] += 1
	elif line[i][3] == " three" or line[i][3] == " 3" or line[i][3] == " 3 runs":
		score += 3
		indBatting.loc[batter, "R"] += 3
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 3
		pakBalling.loc[baller, "O"] += 1
	elif line[i][3] == " two" or line[i][3] == " 2" or line[i][3] == " 2 runs":
		score += 2
		indBatting.loc[batter, "R"] += 2
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 2
		pakBalling.loc[baller, "O"] += 1
	elif line[i][3] == " one" or line[i][3] == " 1" or line[i][3] == " 1 run":
		score += 1
		indBatting.loc[batter, "R"] += 1
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 1
		pakBalling.loc[baller, "O"] += 1
	elif line[i][3] == " no run":
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "O"] += 1
	elif "out" in line[i][3]:
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "W"] += 1
		pakBalling.loc[baller, "O"] += 1
		if "caught" in line[i][3] or "catch" in line[i][3]:
			indBatting.loc[batter, "Status"] = "b " + baller
		else:
			indBatting.loc[batter, "Status"] = "b " + baller
	elif "bye" in line[i][3]:
		lb = 0
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "O"] += 1
		line[i][4] = line[i][4].lower()
		
		if line[i][4] == " four" or line[i][4] == " 4" or line[i][4] == " 4 runs":
			score += 4
			lb = 4
		elif line[i][4] == " three" or line[i][4] == " 3" or line[i][4] == " 3 runs":
			score += 3
			lb = 3
		elif line[i][4] == " two" or line[i][4] == " 2" or line[i][4] == " 2 runs":
			score += 2
			lb = 2
		elif line[i][4] == " one" or line[i][4] == " 1" or line[i][4] == " 1 run":
			score += 1
			lb = 1

		if "leg" in line[i][3]:
			legBye += lb
		else:
			bye += lb

indBatting["SR"] = round(indBatting["R"]*100/indBatting["B"], 2)
pakBalling["O"] = pakBalling["O"]//6 + (pakBalling["O"]%6)/10
pakBalling["ECO"] = round(pakBalling["R"]/pakBalling["O"], 2)
print(indBatting)
print(pakBalling)
print(score, legBye, bye, noBall, wide)
def scorecard():
	pass


###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


scorecard()






#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
