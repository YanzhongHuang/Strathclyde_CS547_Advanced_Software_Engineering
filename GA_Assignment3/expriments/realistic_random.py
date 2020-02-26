import random
import numpy as np
from deap import base, creator, tools, algorithms

# 读取nrp数据，获取cost列表和customer列表
# read data from nrp file, get the cost list and customer list
def Read_File():
	with open('realistic_nrp3_fixed.txt', 'r') as f:
		dataset = f.readlines()
		customer_list = []
		cost_list = [int(i) for i in dataset[0][0:-1].split(' ')]
		N_customers = int(dataset[1])
		for i in range(2, N_customers + 2):
			customer = [int(j) for j in dataset[i][0:-1].split(' ')]
			customer_list.append(customer)
	return cost_list, customer_list

# 评估函数，返回当前个体的总cost和总profit
# evaluate individuals, get the total cost and total profit of this individual
def evaluate(individual):
	profit_total = 0
	cost_total = 0
	for i in range(0, GENE_LENGTH):
		for j in range(0, customer_list[i][1]):
			cost_total += individual[i] * cost_list[customer_list[i][j + 2] - 1]
		profit_total += individual[i] * customer_list[i][0]
	return cost_total, profit_total

lists = Read_File()
cost_list = lists[0]
customer_list = lists[1]

# 使用deap中的工具来产生随机个体
# use tools in deap to generate random individuals
creator.create('FitnessMulti', base.Fitness, weights=(-1.0, 1.0))
creator.create('Individual', list, fitness = creator.FitnessMulti)

GENE_LENGTH = len(customer_list)

toolbox = base.Toolbox()
toolbox.register('Binary', random.randint, 0, 1)
toolbox.register('Individual', tools.initRepeat, creator.Individual, toolbox.Binary, n = GENE_LENGTH)

# 生成5000个随机样本，将结果写入文件以便分析
# generate 5000 random samples and write the result into file for analysis
with open('realistic_random.txt', 'w') as wf:
	for i in range(0, 5000):
		ind = toolbox.Individual()
		result = evaluate(ind)
		wf.write(str(int(result[0])) + ' ' + str(int(result[1])) + '\n')
		