import random
from deap import base, creator, tools, algorithms
import numpy as np

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

# 多目标优化，最大化profit，最小化cost
# multi-objective nrp, maximize profit and minmize cost at the same time
creator.create('FitnessMulti', base.Fitness, weights=(-1.0, 1.0))
creator.create('Individual', list, fitness = creator.FitnessMulti)

# 个体基因长度为顾客数量
# the length of gene is equal to the number of customers
GENE_LENGTH = len(customer_list)

toolbox = base.Toolbox()
toolbox.register('Binary', random.randint, 0, 1)
toolbox.register('Individual', tools.initRepeat, creator.Individual, toolbox.Binary, n = GENE_LENGTH)

# 生成初始种群
# initialize the population
POP_SIZE = 20
toolbox.register('Population', tools.initRepeat, list, toolbox.Individual)
pop = toolbox.Population(n = POP_SIZE)

# 使用内置进化算法
# use the build-in evolutionary algorithm in deap
toolbox.register('evaluate', evaluate)
toolbox.register('select', tools.selTournament, tournsize = 2)
toolbox.register('mate', tools.cxUniform, indpb = 0.5)
toolbox.register('mutate', tools.mutFlipBit, indpb = 0.5)

stats = tools.Statistics(key=lambda ind: ind.fitness.values)

# 重复50次实验，生成实验结果写入文件
# repeat 50 times, and write the results into result file for analysis
with open('realistic_multi_obj.txt', 'w') as wf:
	for i in range(0, 50):
		resultPop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=500, stats = stats, verbose = False)
		index = np.argmax([ind.fitness for ind in resultPop])
		result = resultPop[index].fitness.values
		wf.write(str(int(result[0])) + ' ' + str(int(result[1])) + '\n')