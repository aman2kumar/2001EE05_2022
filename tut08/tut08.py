import pandas as pd
import re
from datetime import datetime
start_time = datetime.now()

ind_text = open("india_inns2.txt", "r").read()
pak_text = open("pak_inns1.txt", "r").read()

indPlayers = ["Rohit Sharma(c)", "KL Rahul", "Virat Kohli", "Suryakumar Yadav", "Dinesh Karthik(w)", "Hardik Pandya",
				"Ravindra Jadeja", "Bhuvneshwar Kumar", "Avesh Khan", "Yuzvendra Chahal", "Arshdeep Singh"]
pakPlayers = ["Babar Azam", "Mohammad Rizwan", "Fakhar Zaman", "Iftikhar Ahmed", "Khushdil Shah", "Asif Ali", "Shadab Khan",
				"Mohammad Nawaz", "Naseem Shah", "Haris Rauf", "Shahnawaz Dahani"]

ind_inns = []
pak_inns = []
for line in ind_text.split('\n'):
	if line != "":
		ind_inns.append(line)
for line in pak_text.split('\n'):
	if line != "":
		pak_inns.append(line)

total_balls_ind = len(ind_inns)
total_balls_pak = len(pak_inns)
line_ind = []
line_pak = []
for i in range(total_balls_ind):
	line_ind.append(ind_inns[i].split(','))
for i in range(total_balls_pak):
	line_pak.append(pak_inns[i].split(','))

for i in range(total_balls_ind):
	ball, commentary = line_ind[i][0].split(' ', 1)
	line_ind[i][0] = ball 
	line_ind[i].insert(1, commentary)
for i in range(total_balls_pak):
	ball, commentary = line_pak[i][0].split(' ', 1)
	line_pak[i][0] = ball 
	line_pak[i].insert(1, commentary)

indBatter = []
indBaller = []
pakBatter = []
pakBaller = []

for i in range(total_balls_ind):
	player = line_ind[i][1].split('to')
	line_ind[i][1] = player[0]
	line_ind[i].insert(2, player[1])
	indBatter.append(player[1])
	pakBaller.append(player[0])

for i in range(total_balls_pak):
	player = line_pak[i][1].split('to')
	line_pak[i][1] = player[0]
	line_pak[i].insert(2, player[1])
	pakBatter.append(player[1])
	indBaller.append(player[0])

indBatter = list(dict.fromkeys(indBatter))
indBaller = list(dict.fromkeys(indBaller))
pakBatter = list(dict.fromkeys(pakBatter))
pakBaller = list(dict.fromkeys(pakBaller))

indBatting = pd.DataFrame(0, indBatter, ["Status", "R", "B", "4s", "6s", "SR"])
indBalling = pd.DataFrame(0, indBaller, ["O", "M", "R", "W", "NB", "WD", "ECO"])
pakBatting = pd.DataFrame(0, pakBatter, ["Status", "R", "B", "4s", "6s", "SR"])
pakBalling = pd.DataFrame(0, pakBaller, ["O", "M", "R", "W", "NB", "WD", "ECO"])

indPowerplay_runs = 0
pakPowerplay_runs = 0

ind_score = 0
ind_wkts = 0
ind_extra = 0
ind_wide = 0
ind_noBall = 0
ind_bye = 0
ind_legBye = 0

pak_score = 0
pak_wkts = 0
pak_extra = 0
pak_wide = 0
pak_noBall = 0
pak_bye = 0
pak_legBye = 0

ind_fall_of_wkts = []
pak_fall_of_wkts = []

for i in range(total_balls_ind):
	batter = line_ind[i][2]
	baller = line_ind[i][1]
	line_ind[i][3] = line_ind[i][3].lower()
	if line_ind[i][0] == "6.1":
		pakPowerplay_runs = ind_score
	if "wide" in line_ind[i][3]:
		temp = re.findall("[0-9]", line_ind[i][3])
		if len(temp) == 0:
			ind_wide += 1
			ind_score += 1
			pakBalling.loc[baller, "R"] += 1
			pakBalling.loc[baller, "WD"] += 1
		else:
			ind_wide += int(temp[0])
			print(temp)
			ind_score += int(temp[0])
			pakBalling.loc[baller, "R"] += int(temp[0])
			pakBalling.loc[baller, "WD"] += int(temp[0])
		
	elif line_ind[i][3] == " no ball":
		ind_noBall += 1
		ind_score += 1
		pakBalling.loc[baller, "R"] += 1
		pakBalling.loc[baller, "NB"] += 1
	elif line_ind[i][3] == " four" or line_ind[i][3] == " 4" or line_ind[i][3] == " 4 runs":
		ind_score += 4
		indBatting.loc[batter, "R"] += 4
		indBatting.loc[batter, "B"] += 1
		indBatting.loc[batter, "4s"] += 1
		pakBalling.loc[baller, "R"] += 4
		pakBalling.loc[baller, "O"] += 1
	elif line_ind[i][3] == " six" or line_ind[i][3] == " 6" or line_ind[i][3] == " 6 runs":
		ind_score += 6
		indBatting.loc[batter, "R"] += 6
		indBatting.loc[batter, "B"] += 1
		indBatting.loc[batter, "6s"] += 1
		pakBalling.loc[baller, "R"] += 6
		pakBalling.loc[baller, "O"] += 1
	elif line_ind[i][3] == " three" or line_ind[i][3] == " 3" or line_ind[i][3] == " 3 runs":
		ind_score += 3
		indBatting.loc[batter, "R"] += 3
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 3
		pakBalling.loc[baller, "O"] += 1
	elif line_ind[i][3] == " two" or line_ind[i][3] == " 2" or line_ind[i][3] == " 2 runs":
		ind_score += 2
		indBatting.loc[batter, "R"] += 2
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 2
		pakBalling.loc[baller, "O"] += 1
	elif line_ind[i][3] == " one" or line_ind[i][3] == " 1" or line_ind[i][3] == " 1 run":
		ind_score += 1
		indBatting.loc[batter, "R"] += 1
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "R"] += 1
		pakBalling.loc[baller, "O"] += 1
	elif line_ind[i][3] == " no run":
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "O"] += 1
	elif "out" in line_ind[i][3]:
		ind_wkts += 1
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "W"] += 1
		pakBalling.loc[baller, "O"] += 1
		ind_fall_of_wkts.append(f"{ind_score}-{ind_wkts} ({batter}, {line_ind[i][0]})")
		if "caught" in line_ind[i][3] or "catch" in line_ind[i][3]:
			for pak_player in pakPlayers:
				if pak_player.lower() in line_ind[i][3]:
					indBatting.loc[batter, "Status"] = "c " + pak_player + "b " + baller
					break
		elif "lbw" in line_ind[i][3]:
			indBatting.loc[batter, "Status"] = "lbw b " + baller
		else:
			indBatting.loc[batter, "Status"] = "b " + baller
	elif "bye" in line_ind[i][3]:
		lb = 0
		indBatting.loc[batter, "B"] += 1
		pakBalling.loc[baller, "O"] += 1
		line_ind[i][4] = line_ind[i][4].lower()
		
		if line_ind[i][4] == " four" or line_ind[i][4] == " 4" or line_ind[i][4] == " 4 runs":
			ind_score += 4
			lb = 4
		elif line_ind[i][4] == " three" or line_ind[i][4] == " 3" or line_ind[i][4] == " 3 runs":
			ind_score += 3
			lb = 3
		elif line_ind[i][4] == " two" or line_ind[i][4] == " 2" or line_ind[i][4] == " 2 runs":
			ind_score += 2
			lb = 2
		elif line_ind[i][4] == " one" or line_ind[i][4] == " 1" or line_ind[i][4] == " 1 run":
			ind_score += 1
			lb = 1

		if "leg" in line_ind[i][3]:
			ind_legBye += lb
		else:
			ind_bye += lb

for i in range(total_balls_pak):
	batter = line_pak[i][2]
	baller = line_pak[i][1]
	line_pak[i][3] = line_pak[i][3].lower()
	if line_pak[i][0] == "6.1":
		indPowerplay_runs = pak_score
	if "wide" in line_pak[i][3]:
		temp = re.findall("[0-9]", line_pak[i][3])
		if len(temp) == 0:
			pak_wide += 1
			pak_score += 1
			indBalling.loc[baller, "R"] += 1
			indBalling.loc[baller, "WD"] += 1
		else:
			pak_wide += int(temp[0])
			print(temp)
			pak_score += int(temp[0])
			indBalling.loc[baller, "R"] += int(temp[0])
			indBalling.loc[baller, "WD"] += int(temp[0])
		
	elif line_pak[i][3] == " no ball":
		ind_noBall += 1
		pak_score += 1
		indBalling.loc[baller, "R"] += 1
		indBalling.loc[baller, "NB"] += 1
	elif line_pak[i][3] == " four" or line_pak[i][3] == " 4" or line_pak[i][3] == " 4 runs":
		pak_score += 4
		pakBatting.loc[batter, "R"] += 4
		pakBatting.loc[batter, "B"] += 1
		pakBatting.loc[batter, "4s"] += 1
		indBalling.loc[baller, "R"] += 4
		indBalling.loc[baller, "O"] += 1
	elif line_pak[i][3] == " six" or line_pak[i][3] == " 6" or line_pak[i][3] == " 6 runs":
		pak_score += 6
		pakBatting.loc[batter, "R"] += 6
		pakBatting.loc[batter, "B"] += 1
		pakBatting.loc[batter, "6s"] += 1
		indBalling.loc[baller, "R"] += 6
		indBalling.loc[baller, "O"] += 1
	elif line_pak[i][3] == " three" or line_pak[i][3] == " 3" or line_pak[i][3] == " 3 runs":
		pak_score += 3
		pakBatting.loc[batter, "R"] += 3
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "R"] += 3
		indBalling.loc[baller, "O"] += 1
	elif line_pak[i][3] == " two" or line_pak[i][3] == " 2" or line_pak[i][3] == " 2 runs":
		pak_score += 2
		pakBatting.loc[batter, "R"] += 2
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "R"] += 2
		indBalling.loc[baller, "O"] += 1
	elif line_pak[i][3] == " one" or line_pak[i][3] == " 1" or line_pak[i][3] == " 1 run":
		pak_score += 1
		pakBatting.loc[batter, "R"] += 1
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "R"] += 1
		indBalling.loc[baller, "O"] += 1
	elif line_pak[i][3] == " no run":
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "O"] += 1
	elif "out" in line_pak[i][3]:
		pak_wkts += 1
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "W"] += 1
		indBalling.loc[baller, "O"] += 1
		pak_fall_of_wkts.append(f"{pak_score}-{pak_wkts} ({batter}, {line_pak[i][0]})")
		if "caught" in line_pak[i][3] or "catch" in line_pak[i][3]:
			for ind_player in indPlayers:
				if ind_player.lower() in line_pak[i][3]:
					pakBatting.loc[batter, "Status"] = "c " + ind_player + "b " + baller
					break
		elif "lbw" in line_pak[i][3]:
			pakBatting.loc[batter, "Status"] = "lbw b " + baller
		else:
			pakBatting.loc[batter, "Status"] = "b " + baller
	elif "bye" in line_pak[i][3]:
		lb = 0
		pakBatting.loc[batter, "B"] += 1
		indBalling.loc[baller, "O"] += 1
		line_pak[i][4] = line_pak[i][4].lower()
		
		if line_pak[i][4] == " four" or line_pak[i][4] == " 4" or line_pak[i][4] == " 4 runs":
			pak_score += 4
			lb = 4
		elif line_pak[i][4] == " three" or line_pak[i][4] == " 3" or line_pak[i][4] == " 3 runs":
			pak_score += 3
			lb = 3
		elif line_pak[i][4] == " two" or line_pak[i][4] == " 2" or line_pak[i][4] == " 2 runs":
			pak_score += 2
			lb = 2
		elif line_pak[i][4] == " one" or line_pak[i][4] == " 1" or line_pak[i][4] == " 1 run":
			pak_score += 1
			lb = 1

		if "leg" in line_pak[i][3]:
			pak_legBye += lb
		else:
			pak_bye += lb

indBatting["SR"] = round(indBatting["R"]*100/indBatting["B"], 2)
pakBatting["SR"] = round(pakBatting["R"]*100/pakBatting["B"], 2)
for i in range(len(indBatter)):
	if indBatting.loc[indBatter[i], "Status"] == 0:
		indBatting.loc[indBatter[i], "Status"] = "not out"
for i in range(len(pakBatter)):
	if pakBatting.loc[pakBatter[i], "Status"] == 0:
		pakBatting.loc[pakBatter[i], "Status"] = "not out"
indBalling["O"] = indBalling["O"]//6 + (indBalling["O"]%6)/10
indBalling["ECO"] = round(indBalling["R"]/indBalling["O"], 2)
pakBalling["O"] = pakBalling["O"]//6 + (pakBalling["O"]%6)/10
pakBalling["ECO"] = round(pakBalling["R"]/pakBalling["O"], 2)

print(indBatting)
print(pakBalling)
print(ind_score, ind_legBye, ind_bye, ind_noBall, ind_wide)
print(ind_fall_of_wkts)

print(pakBatting)
print(indBalling)
print(pak_score, pak_legBye, pak_bye, pak_noBall, pak_wide)
print(pak_fall_of_wkts)
ind_extra = ind_bye + ind_legBye + ind_wide + ind_noBall
pak_extra = pak_bye + pak_legBye + pak_wide + pak_noBall

def scorecard():
	OUTPUT=open('Scorecard.txt','w')
	OUTPUT.write(' Pakistan Innings\n')
	OUTPUT.write(f"{pak_score : >50}-{pak_wkts} ({indBalling['O'].sum()} Ov)")
	OUTPUT.write('\n Batter\n')
	OUTPUT.write(str(pakBatting)) 
	OUTPUT.write('\n Extras\t\t\t\t\t\t\t\t\t   '+str(pak_extra)+' (b '+str(pak_bye)+', lb '+str(pak_legBye)+', w '+str(pak_wide)+', nb '+str(pak_noBall)+')') 
	OUTPUT.write('\n Total \t\t\t\t\t\t\t\t\t   '+str(pak_score)+' ('+str(pak_wkts)+' wkts, '+str(indBalling['O'].sum())+' Ov)\n') 
	OUTPUT.write('\n Fall of Wickets\n ')
	OUTPUT.write(', '.join(pak_fall_of_wkts))
	OUTPUT.write('\n\n')
	OUTPUT.write('Bowler\n')
	OUTPUT.write(str(indBalling))
	OUTPUT.write('\n')
	OUTPUT.write('\nPowerplays\t    '+'Overs\t\t\t    '+'Runs')
	OUTPUT.write('\nMandatory\t    '+'0.1-6\t\t\t\t'+str(indPowerplay_runs)+'\n')
	OUTPUT.write('\n\n\n')

	OUTPUT.write(' India Innings\n')
	OUTPUT.write(f"{ind_score : >50}-{ind_wkts} ({pakBalling['O'].sum()} Ov)")
	OUTPUT.write('\n Batter\n')
	OUTPUT.write(str(indBatting)) 
	OUTPUT.write('\n Extras\t\t\t\t\t\t\t\t\t\t   '+str(ind_extra)+' (b '+str(ind_bye)+', lb '+str(ind_legBye)+', w '+str(ind_wide)+', nb '+str(ind_noBall)+')') 
	OUTPUT.write('\n Total \t\t\t\t\t\t\t\t\t\t   '+str(ind_score)+' ('+str(ind_wkts)+' wkts, '+str(pakBalling['O'].sum())+' Ov)\n') 
	OUTPUT.write('\n Fall of Wickets\n ')
	OUTPUT.write(', '.join(ind_fall_of_wkts))
	OUTPUT.write('\n\n')
	OUTPUT.write('Bowler\n')
	OUTPUT.write(str(indBalling))
	OUTPUT.write('\n')
	OUTPUT.write('\nPowerplays\t    '+'Overs\t\t\t    '+'Runs')
	OUTPUT.write('\nMandatory\t    '+'0.1-6\t\t\t\t'+str(pakPowerplay_runs)+'\n')



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
