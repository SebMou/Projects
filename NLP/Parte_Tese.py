# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:37:20 2019

@author: sebmo
"""

import numpy as np
import matplotlib
import pandas
import matplotlib.pyplot as plt
from hmmlearn import hmm
import random


dataset_washer = pandas.read_excel('Dataset_grande_junto.xlsx', sheet_name='Washer')
dataset_dishwasher = pandas.read_excel('Dataset_grande_junto.xlsx', sheet_name='Dishwasher')
dataset_rest = pandas.read_excel('Dataset_grande_junto.xlsx', sheet_name='Rest')

dataset_washer = dataset_washer.drop(columns='Hora')
dataset_dishwasher = dataset_dishwasher.drop(columns='Hora')
dataset_rest = dataset_rest.drop(columns='Hora')

washer_trset = [[0] * 96 for i in range(len(dataset_washer))]
dishwasher_trset = [[0] * 96 for i in range(len(dataset_dishwasher))]
rest_trset = [[0] * 96 for i in range(len(dataset_rest))]

for i in range(len(dataset_rest)):
    for j in range(len(dataset_rest.columns)):
        if dataset_washer.iloc[i,j] == 0:
            washer_trset[i][j] = 0 
            
        if dataset_washer.iloc[i,j] > 0:
            washer_trset[i][j] = 1 
            
        if dataset_dishwasher.iloc[i,j] == 0:
            dishwasher_trset[i][j] = 0
            
        if dataset_dishwasher.iloc[i,j] > 0:
            dishwasher_trset[i][j] = 1 
            
        if dataset_rest.iloc[i,j] == 0:
            rest_trset[i][j] = 0
            
        if dataset_rest.iloc[i,j] > 0:
            rest_trset[i][j] = 1 


washer_validation = []
dishwasher_validation = []
rest_validation = []

for i in range(10):
    x = random.randint(0, len(washer_trset))
    
    washer_validation.append(washer_trset[x])
    dishwasher_validation.append(dishwasher_trset[x])
    rest_validation.append(rest_trset[x])

    del washer_trset[x]
    del dishwasher_trset[x]
    del rest_trset[x]



num_samples = 100

ticks = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72,
         76, 80, 84, 88, 92, 96]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
          20, 21, 22, 23, 24]


    
plt.figure(1)
plt.title('Washing Machine Model and Validation')
plt.xticks(ticks, labels)
plt.xlabel('Hour')
plt.ylabel('Approximate Probability')
washer_mod = hmm.GaussianHMM(n_components=2)
washer_mod.startprob_ = np.array([1.0, 0.0])
washer_mod.transmat_ = np.array([[0.5, 0.5],
                                 [0.5, 0,5]])
    
print('Initial Washing Machine Transition Matrix\n')
print(washer_mod.transmat_)
print('\n')
    
washer_mod.fit(washer_trset)

print('Washing Machine Transition Matrix\n')
print(washer_mod.transmat_)
print('\n')

avgcalc = []
avg = []


for i in range(num_samples):
    avgcalc.append(washer_mod.sample()[0][0].tolist())
    
for i in range(96):
    med = 0.0
    
    for j in range(num_samples):
        med = avgcalc[j][i] + med
        
    avg.append(med/num_samples)

    
plt.plot(avg, color='blue')


avg = []

for i in range(96):
    med = 0.0
    
    for j in range(10):
        med = washer_validation[j][i] + med
        
    avg.append(med/10)

plt.plot(avg, color='green')
    
    
plt.figure(2)
plt.title('Dishwasher Model and Validation')
plt.xticks(ticks, labels)
plt.xlabel('Hour')
plt.ylabel('Approximate Probability')
dishwasher_mod = hmm.GaussianHMM(n_components=2)
dishwasher_mod.startprob_ = np.array([1.0, 0.0])
dishwasher_mod.transmat_ = np.array([[0.1, 0.9],
                                     [0.1, 0,9]])
    
print('Initial Dishwasher Transition Matrix\n')
print(dishwasher_mod.transmat_)
print('\n')
    
dishwasher_mod.fit(dishwasher_trset)

print('Dishwasher Transition Matrix\n')
print(dishwasher_mod.transmat_)
print('\n')

avgcalc = []
avg = []


for i in range(num_samples):
    avgcalc.append(dishwasher_mod.sample()[0][0].tolist())
    
for i in range(96):
    med = 0.0
    
    for j in range(num_samples):
        med = avgcalc[j][i] + med
        
    avg.append(med/num_samples)

    
plt.plot(avg, color='blue')


avg = []

for i in range(96):
    med = 0.0
    
    for j in range(10):
        med = dishwasher_validation[j][i] + med
        
    avg.append(med/10)

plt.plot(avg, color='green')
    
    
    
plt.figure(3)
plt.title('Rest Model and Validation')
plt.xticks(ticks, labels)
plt.xlabel('Hour')
plt.ylabel('Approximate Probability')
rest_mod = hmm.GaussianHMM(n_components=2)
rest_mod.startprob_ = np.array([1.0, 0.0])
rest_mod.transmat_ = np.array([[0.5, 0.5],
                               [0.5, 0,5]])
    
print('Initial Rest Transition Matrix\n')
print(rest_mod.transmat_)
print('\n')
    
rest_mod.fit(rest_trset)

print('Rest Transition Matrix\n')
print(rest_mod.transmat_)
print('\n')

avgcalc = []
avg = []


for i in range(num_samples):
    avgcalc.append(rest_mod.sample()[0][0].tolist())
    
for i in range(96):
    med = 0.0
    
    for j in range(num_samples):
        med = avgcalc[j][i] + med
        
    avg.append(med/num_samples)

    
plt.plot(avg, color='blue')


avg = []

for i in range(96):
    med = 0.0
    
    for j in range(10):
        med = rest_validation[j][i] + med
        
    avg.append(med/10)

plt.plot(avg, color='green')
