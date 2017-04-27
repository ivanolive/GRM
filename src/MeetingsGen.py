try:
    import matplotlib.pyplot as plt
except:
    raise

import numpy.random as rd
import numpy as np
import HeavyTail as pl

def generateGroupMeetingTimes(first_meeting_time,group_duration,beta,traceDur):	
#Parameters: <first_meeting time in hours> <period throughout which the group will meet regularly in hours> <average re-meeting period in hours>
#Generates group meeting times according to a poisson process
	beta = beta*3600
	traceDur = traceDur*24*3600
	sdev = 3*3600
	group_duration = group_duration*24*3600
	group_meeting_intervals = rd.normal(beta,sdev,group_duration/beta)
	for i in range(len(group_meeting_intervals)):
		if group_meeting_intervals[i] < 0:
			group_meeting_intervals[i] = 0;
	#group_meeting_intervals = [first_meeting_time]+group_meeting_intervals
	group_meeting_times = []
	cumsum = 0
	for i in range(len(group_meeting_intervals)):
		coin = rd.exponential(2*group_duration*beta/(3600*24))
		if(coin > cumsum and cumsum < traceDur):
			group_meeting_times = group_meeting_times + [cumsum]
		cumsum += group_meeting_intervals[i]
	for i in range(len(group_meeting_times)):
		print(int(group_meeting_times[i]/3600))
	for i in range(len(group_meeting_times)):
		group_meeting_times[i] = (first_meeting_time + group_meeting_times[i]) #converting to seconds
	return group_meeting_times

def readRegularityDistro():
	f = open("RegDistro.csv")
	groupsRegDistro = []
	n_groups = 0 
	for line in f:
		pair = line.split(" ")
		i = int(pair[0])
		j = int(pair[1])
		n_groups += i
		groupsRegDistro = groupsRegDistro + [[i,j]]
	return (n_groups,groupsRegDistro)

def generateRegularityDistro(n_groups, alpha):
	groupsRegDistro = []
	for i in range(n_groups):
		sample = int(pl.randht(1,'powerlaw',alpha)[0]);
		sample = sample*4#*24
		groupsRegDistro = groupsRegDistro + [[1,sample]]
	return (groupsRegDistro)


def generateGroupSet(n_groups, alpha,groupsRegDistro, g_dur, sim_dur,pathTime):
	groupSet = []
	for i in groupsRegDistro:
		for j in range(i[0]):
			beta = int(pl.randht(1,'powerlaw',alpha)[0]);
			beta = beta*i[1];
			firstMeeting1 = int(np.random.exponential(24*3600))+pathTime		#Avoiding slow start
			firstMeeting2 = np.random.randint(pathTime,sim_dur*24*3600)	
			coin = np.random.randint(0,100)
			if coin < 10:
				firstMeeting = firstMeeting1
			else:
				firstMeeting = firstMeeting2

			newGroup = generateGroupMeetingTimes(firstMeeting,g_dur,beta,sim_dur);
			groupSet = groupSet + [newGroup]
	return groupSet

def generateMeetingDur(n_groups,meetingTimes, dur_alpha, dur_beta,pathTime):
	meetingsAvgDur = pl.randht(n_groups,'cutoff',600,dur_alpha,1.0/(dur_beta*3600));	#duration in seconds
	#meetingsAvgDur = pl.randht(n_groups,'powerlaw',600,3);	#duration in seconds
	endTimes = []
	durations = []
	for groupEnc in range(len(meetingTimes)):
		endTime = []
		#for i in range(len(meetingTimes[groupEnc])):
		#	durations = durations + [meetingsAvgDur[groupEnc]]
		durations = rd.normal(meetingsAvgDur[groupEnc],300,len(meetingTimes[groupEnc]))
		for i in range(len(durations)):
			if durations[i] < 0:
				durations[i] = 0
		for i in range(len(durations)-1):
			if durations[i] + meetingTimes[groupEnc][i] > meetingTimes[groupEnc][i+1]:
				durations[i] = (meetingTimes[groupEnc][i+1] - meetingTimes[groupEnc][i]) - pathTime
		for i in range(len(durations)):
			endTime = endTime + [meetingTimes[groupEnc][i] + durations[i]]
		endTimes = endTimes+[endTime]
		#durations = [] # adicionei esta linha para atualizar valor de durations do groupEnc atual
	return endTimes

n_groups,groupsRegDistro = readRegularityDistro()

meetings = generateGroupSet(n_groups,2.0,groupsRegDistro,60,60,300)

