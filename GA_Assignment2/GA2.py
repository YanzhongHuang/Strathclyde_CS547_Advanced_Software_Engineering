import numpy as np
import random as rd

POP_SIZE = 100
MAX_GENERATIONS = 2000

def Read_File(filename):
	try:
		file = open(filename, 'r')
		dataset = []
		for line in file.readlines():
			"""Remove 'txxx' and line break"""
			# 去掉头部test序号和尾部\n
			str_list = ((line[0:-1]).split(','))[1:]
			num_list = [int(i) for i in str_list]
			dataset.append(num_list)
	finally:
		if file:
			file.close()
	return dataset

# Get the fitness of an individual with APFD
# 用论文中的AFPD指标当作适应度值
def Get_Fitness(dataset, order):
	s = 0
	fault_num = len(dataset[0])
	test_num = len(dataset)
	for i in range(0, fault_num):
		for j in range(0, test_num):
			if dataset[order[j]][i] == 1:
				s += order[j]
				break
	return 1 - ( s / (fault_num * test_num)) + 1 / (2 * test_num)

# Get fitness of all individuals
# 获取种群中所有个体的适应度
def Get_Fitness_List(dataset, population):
	fitness_list = [0 for n in range(0, POP_SIZE)]
	for i in range(0, POP_SIZE):
		fitness_list[i] = Get_Fitness(dataset, population[i])
	return fitness_list

# Initialize the population randomly with function 'permutation' in numpy.random
# 用numpy模块中的permutation函数来生成随机排列，以此实现随机初始化种群
def Pop_Init(test_num):
	population = []
	test_order = np.arange(test_num)
	while len(population) < POP_SIZE:
		random_order = np.random.permutation(test_order)
		"""Change the type of list elements from np type to int"""
		# 将list元素的类型由numpy定义的类型转为int型，便于后面操作
		individual = [int(i) for i in random_order]
		population.append(individual)
	return population

# Chose parent with n-way tournament selection
# 用课件中的n路竞争选择法来选择父本
def Chose_Parent(fitness_list):
	parent = []
	for i in range(0, 2):
		"""n-way tournament selection"""
		n = int(POP_SIZE / 10)
		sample = rd.sample(range(0, POP_SIZE), n)
		max = 0
		for j in range(1, n):
			if fitness_list[sample[max]] < fitness_list[sample[j]]:
				max = j
		parent.append(sample[max])
	return parent

# Get next generation
# 交叉获取下一代
def Mate(population, fitness_list):
	new_population = []
	test_num = len(population[0])
	"""Loop until the size of new population is equal to the old one"""
	# 循环直至新种群规模和原种群一样
	while len(new_population) < POP_SIZE:
		parent = Chose_Parent(fitness_list)
		chosen_parent = [population[parent[0]], population[parent[1]]]
		"""Get the crossing position randomly"""
		# 随机获取交叉位置
		crossing_pos = rd.randrange(1, test_num - 1)
		"""Make sure we don’t introduce duplicate tests (only checked the recent two generations)"""
		# 按照课件中的方法，保证不引入重复测试
		tmp_parent0 = chosen_parent[1].copy()
		tmp_parent1 = chosen_parent[0].copy()
		for i in range(0, crossing_pos):
			tmp_parent0.remove(chosen_parent[0][i])
			tmp_parent1.remove(chosen_parent[1][i])

		child0 = chosen_parent[0][0:crossing_pos] + tmp_parent0
		child1 = chosen_parent[1][0:crossing_pos] + tmp_parent1
		
		new_population.append(child0)
		new_population.append(child1)

	population = new_population
	return population

# Mutate by a certain rate
# 按照一定概率变异
def Mutate(population):
	test_num = len(population[0])
	for i in range(0, POP_SIZE):
		for j in range(0, test_num):
			if rd.randrange(0, POP_SIZE) == i:
				""" Swap position of two randomly selected tests """
				# 变异方法为课件中的随机交换两个tests的位置
				switch_pos = rd.randrange(0, test_num)
				tmp = population[i][j]
				population[i][j] = population[i][switch_pos]
				population[i][switch_pos] = tmp
	return population

# Genetic Algorithm: put everything together
# 遗传算法整合函数
def Genetic_Algorithm(filename):
	print('---------Genetic Algorithm for '+ filename + ' begin---------')
	dataset = Read_File(filename)
	population = Pop_Init(len(dataset))
	fitness_list = Get_Fitness_List(dataset, population)
	
	generations = 0
	max_fitness = 0
	while generations < MAX_GENERATIONS:
		population = Mate(population, fitness_list)
		population = Mutate(population)
		fitness_list = Get_Fitness_List(dataset, population)
		generations += 1
		if max(fitness_list) > max_fitness:
			max_fitness = max(fitness_list)
			print('the APFD of the best permutation is ' + str(max_fitness) + ', first appearence is in generation ' + str(generations))
	print('best permutation is ' + str(population[np.argmax(fitness_list)]))	
	print('---------Genetic Algorithm for '+ filename + ' finished---------')
	print('')
	print('')
	print('')

	return population[np.argmax(fitness_list)]

# Hill_Climber Algorithm
# 爬山算法函数
def Hill_Climber(filename):
	print('---------Hill Climber for '+ filename + ' begin---------')
	dataset = Read_File(filename)
	"""Get the starting solution randomly with permutation in numpy"""
	# 随机获得初始解
	test_num = len(dataset)
	test_order = np.arange(test_num)
	random_order = np.random.permutation(test_order)
	starting_solution = [int(i) for i in random_order]

	best_solution = []
	best_fitness = 0
	current_solution = starting_solution
	first_solution = starting_solution
	
	"""If the set of all neighbouring solutions for n faults is defined as
	the set of all permutations that can be generated by swapping two
	adjacent tests, then there would be n − 1 neighbouring solutions"""
	# 对于有n个faults的优化问题，按照课件中的仅交换临近的两个test作为临近点，就会产生n-1个邻居

	while best_solution != first_solution:
		first_solution = best_solution
		for i in range(0, test_num - 1):
			next_solution = current_solution
			next_solution[i] = current_solution[i + 1]
			next_solution[i + 1] = current_solution[i]
		
			current_solution = next_solution
			current_fitness = Get_Fitness(dataset, current_solution) 
		
			if current_fitness > best_fitness:
				best_solution = current_solution
				best_fitness = current_fitness
		print('the APFD of the best solution is ' + str(best_fitness))
	print('best solution is ' + str(best_solution))	
	print('---------Hill Climber for '+ filename + ' finished---------')
	print('')
	print('')
	print('')
	return best_solution

big_set = 'bigfaultmatrix.txt'
small_set = 'smallfaultmatrix.txt'

ga_small = []
hc_small = []
ga_big = []
hc_big = []
for i in range(0, 10):
	ga_small.append(Genetic_Algorithm(small_set))
	hc_small.append(Hill_Climber(small_set))
	ga_big.append(Genetic_Algorithm(big_set))
	hc_big.append(Hill_Climber(big_set))
