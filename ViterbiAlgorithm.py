#!/usr/bin/env python3

'''
Eric Vogel
Principle of Bioinformatics
Module 6 Assignment

This program is an implementation of the Viterbi algorithm to 
calculate the most likely state path that generates an
observed sequence.
'''

def viterbi(obs_seq, states, start_prob, trans_prob, emis_prob):
	V = [{}]
	
	for st in states:
		# Find the highest probability of the hidden start state with the emission probability of the first observation
		V[0][st] = {"probability": start_prob[st] * emis_prob[st][obs_seq[0]], "predecessor": None}
	
	# Continue when there are more states
	for t in range(1, len(obs_seq)):
		# Add new slot for each possible hidden state in the observation sequence
		V.append({})
		for st in states:
			# Find the highest probability of hidden state multiplied by it transition probability
			max_tran_prob = 0
			for prev_st in states:
				temp = V[t-1][prev_st]["probability"] * trans_prob[prev_st][st]
				if (temp > max_tran_prob):
					max_tran_prob = temp	
			for prev_st in states:
				if(V[t-1][prev_st]["probability"] * trans_prob[prev_st][st] == max_tran_prob):
					max_prob = max_tran_prob * emis_prob[st][obs_seq[t]]
					V[t][st] = {"probability": max_prob, "predecessor": prev_st}

	# Print DP Table
	# Number of observations in sequence
	obs_num = '       '
	for i in range(len(V)):
		obs_num = obs_num + str(i) + '        '

	print(obs_num)

	# Print out probabilities in DP Table
	for state in V[0]:
		print("%s: " % state + " ".join("%.7s" % ("%f" % st[state]["probability"]) for st in V))

	# Stores the optimal path
	optimal = []
	predecessor = None 
	max_prob = 0
	# The highest probability of possible paths
	for prob in V[len(V)-1].values():
		temp = prob["probability"]
		if (temp > max_prob):
			max_prob = temp

	# Find last state in optimal path
	for st, probabilities in V[len(V)-1].items():
		if(probabilities["probability"] == max_prob):
			optimal.append(st)
			predecessor = st

	# Trace-back for optimal path determination
	for t in range(len(V) - 2, -1, -1):
		optimal.insert(0, V[t + 1][predecessor]["predecessor"])
		predecessor = V[t + 1][predecessor]["predecessor"]

	print('\nThe most likely state path is ' + ', '.join(optimal) + '\nThe probability of the sequence %s: %s\n' % (str(obs_seq)[1:-1], max_prob))

# Observation sequence
obs_seq = ('walked', 'shopped', 'cleaned')
# Hidden states
states = ('Rainy', 'Sunny')
# Start probabilities
start_prob = {'Rainy': 0.6, 'Sunny': 0.4}
# Transition probability matrix
trans_prob = {'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3}, 'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6}}
# Emission probabilities
emis_prob = {'Rainy' : {'walked': 0.1, 'shopped': 0.4, 'cleaned': 0.5}, 'Sunny' : {'walked': 0.6, 'shopped': 0.3, 'cleaned': 0.1}}

viterbi(obs_seq, states, start_prob, trans_prob, emis_prob)






