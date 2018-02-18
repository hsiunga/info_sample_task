#!/usr/bin/env python2

# creating optimal model using sequential probability ratio test for info sampling task

# created 02/18/2018 by AH lasted edited 02/18/2018 by AH

import pprint
from operator import itemgetter
import numpy as np
import math

# variables for SPRT
alpha = 0.05
beta = 0.20 # Power = 0.80
prob_1 = 0.60 # number 0 (indoor)
prob_2 = 0.40 # number 1 (outdoor)


# create sequence of random samples
def gen_rand_int():
    ind_sample = np.random.choice(2, 1, p=[0.6, 0.4])
    return ind_sample


# define boundaries
alpha_bound = math.log((1 - beta) / alpha)
beta_bound = math.log(beta / (1 - alpha))

print alpha_bound
print beta_bound

# define weighted evidence per sample
evidence_accumulated = 0
num_of_0s = 0 # indoor scenes
num_of_1s = 0 # outdoor scenes
no = 1
winner = None
table = []

for run in range(100):
    while beta_bound < evidence_accumulated < alpha_bound:
        gen_rand_int()
        if gen_rand_int() == 0:
            weighted_evi = math.log(0.60 / 0.40)
            evidence_accumulated = evidence_accumulated + weighted_evi
            num_of_0s = num_of_0s + 1
            # print('Sample ' + str(no) + ' was a Indoor, ' + str(beta_bound) + ' < ' + str(evidence_accumulated) + ' < ' + str(
            #     alpha_bound))
        else:  # if gen_rand_int() == 1:
            weighted_evi = math.log(0.40 / 0.60)
            evidence_accumulated = evidence_accumulated + weighted_evi
            # print('Sample ' + str(no) + ' was a Outdoor, ' + str(beta_bound) + ' < ' + str(evidence_accumulated) + ' < ' + str(
            #     alpha_bound))
            num_of_1s = num_of_1s + 1
        no = no + 1
        if evidence_accumulated < beta_bound:
            winner = 'Outdoor'
            break
            #print('Accept Outdoor as Majority')
        elif evidence_accumulated > alpha_bound:
            winner = 'Indoor'
            break
            #print('Accept Indoor as Majority')
        else:
            continue
    table.append((run, winner, num_of_0s, num_of_1s))
    # print('Run: ' + str(run) + ' Accepted ' + winner + ' as majority with Number of indoor images: ' +
    #       str(num_of_0s) + ' and Number of outdoor images: ' + str(num_of_1s))
    evidence_accumulated = 0
    num_of_0s = 0  # indoor scenes
    num_of_1s = 0  # outdoor scenes
    no = 1


t2 = sorted(table, key=itemgetter(2))
pprint.pprint(t2)
# decision_plot(no, evidence_accumulated, num_of_1s, num_of_0s)

#print('Number of indoor images: ' + str(num_of_0s))
#print('Number of outdoor images: ' + str(num_of_1s))
