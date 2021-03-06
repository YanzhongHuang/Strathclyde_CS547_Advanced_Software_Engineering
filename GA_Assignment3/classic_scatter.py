import matplotlib.pyplot as plt
import numpy as np

def Read_File(filename):
	cost = []
	profit = []
	with open(filename, 'r') as f:
		for line in f.readlines():
			data = [int(i) for i in line[0:-1].split(' ')]
			cost.append(-data[0])
			profit.append(data[1])
	return cost, profit

classic_multi_obj = Read_File('./expriments/classic_multi_obj.txt')
classic_single_obj = Read_File('./expriments/classic_single_obj.txt')
classic_random = Read_File('./expriments/classic_random.txt')

cost_multi = classic_multi_obj[0]
profit_multi = classic_multi_obj[1]

cost_single = classic_single_obj[0]
profit_single = classic_single_obj[1]

cost_random = classic_random[0]
profit_random = classic_random[1]


plt.scatter(cost_multi, profit_multi, s=15, marker = '>', c = 'r')
plt.scatter(cost_single, profit_single, s=15, marker = '<', c = 'b')
plt.scatter(cost_random, profit_random, s=1, marker = '.', c = 'g')

plt.xlabel('Total Cost')
plt.ylabel('Total Profit')

plt.show()