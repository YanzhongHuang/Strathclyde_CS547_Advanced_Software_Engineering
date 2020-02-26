# Random moudle
# 随机模块
import random as rd

# The target string
# 目标字符串
TARGET = "Welcome to CS547!"

# Get the length of the target string.
# 计算目标字符串长度
STR_LENGTH = len(TARGET)

# Encode target string in ASCII
# 将目标字符串转换成ASCII编码
ENCODED_TARGET = [ord(TARGET[i]) for i in range(0, STR_LENGTH)]

# Population size
# 种群规模
POP_SIZE = 400

# Set the max generations in one simulation
# 设置一次模拟的最大进化代数
MAX_GENS = 4000

# Define the string population list
# 定义种群字符串list
individual_list = [[] for n in range(0, POP_SIZE)]

# Define the fitness list
# 定义适应度list
fitness_list = [0 for n in range(0, POP_SIZE)]

# Generate the initial population randomly
# 随机生成初始种群
def init():
	global individual_list
	for i in range(0, POP_SIZE):
		for j in range(0, STR_LENGTH):
			# This population is encoded in ASCII
			# So the random range is from 0 to 128
			# 种群字符串以二进制编码，随机范围为0到128
			individual_list[i].append(rd.randrange(0, 128))
	#print(individual_list)

# Calculate the fitness for all individuals in present population
# 计算当前种群中所有个体的适应度
def get_fitness():
	global individual_list
	global fitness_list
	for i in range(0, POP_SIZE):
		fitness = 0
		for j in range(0, STR_LENGTH):
			# Compare each element of this individual with target string
			# The more they are commmon, the higher the fitness is
			# 比较每个个体每个位置的字符和目标字符串的相似度，越相似适应度越高
			fitness += (individual_list[i][j] == ENCODED_TARGET[j])
		fitness_list[i] = fitness
		#print(fitness)
	#print(individual_list)

# Check if there is any individual's fitness is high enough to end evolution
# 1 to continue evolve, 0 to stop
# 检查是否有个体已达到进化终止条件,返回1则继续进化，返回0则停止进化
def check():
	global individual_list
	global fitness_list
	for i in range(0, POP_SIZE):
		# When the fitness of an individual is equal to the length of target string
		# It means they are exactly the same, the fitness is then enough
		# 如果一个个体的适应度达到了目标字符串长度也就是最大值，那说明它和目标字符串完全一样，可以终止进化
		if fitness_list[i] == STR_LENGTH:
			# 
			the_one = [[chr(individual_list[i][j]) for j in range(0, STR_LENGTH)]]
			print("We have evolved the target individual:")
			print(the_one)
			return 0
	return 1

# Chose parent individuals according to the fitness, then get the next generation
# 依据个体适应度从当代个体中选择合适的父本交叉得到下一代
def mate():
	global individual_list
	global fitness_list
	# Define the effective parent string and fitness list and total fitness
	# 定义有效父本及其适应度list，总适应度量（总适应度量用于后面的轮盘赌操作）
	parent_list = []
	parent_fitness_list = []
	total_fitness = 0
	for i in range(0, POP_SIZE):
		# Only chose individuals whose fitness are not 0
		# 仅选取适应度大于0的个体作为父本
		if fitness_list[i] > 0:
			parent_list.append(individual_list[i])
			parent_fitness_list.append(fitness_list[i])
			total_fitness += fitness_list[i]
	# Chose 2 individuals from the effective parent list we get above using roulette
	# To get the same population size, there should be POP_SIZE/2 loops
	# 开始交叉，每次用轮盘赌的方法从上一步得到的有效父本中选择2个个体进行交叉
	# 要达到和原来相同的种群规模，需重复POP_SIZE/2次
	for i in range(0, int(POP_SIZE / 2)):
		chosen_parent = []
		for j in range(0, 2):
			# 
			# 建立一个长度为total_fitness的区间，每个个体的适应度在区间中占有相应的长度
			# 随机在这个区间取一个数，由几何概率知取到每个个体的概率和它的适应度相关
			roulette = rd.randrange(1, total_fitness)
			left = 0
			for k in range(0, len(parent_list)):
				left += parent_fitness_list[k]
				if left > roulette:
					chosen_parent.append(parent_list[k])
		# Get the crossing position randomly
		# 随机获取交叉位置
		crossing_pos = rd.randrange(1, STR_LENGTH - 1)
		child1 = chosen_parent[0][0:crossing_pos] + chosen_parent[1][crossing_pos:STR_LENGTH]
		child2 = chosen_parent[1][0:crossing_pos] + chosen_parent[0][crossing_pos:STR_LENGTH]
		individual_list[2 * i] = child1
		individual_list[2 * i + 1] = child2
#		print(child1)
#		print(child2)

# Mutate by the rate of 1/POP_SIZE
# 依概率变异
def mutate():
	global individual_list
	for i in range(0, POP_SIZE):
		for j in range(0, STR_LENGTH):
			if rd.randrange(0, POP_SIZE) == i:
				individual_list[i][j] = rd.randrange(0, 128)
def main():
	flag = 1
	# Check if we get the target individual
	# 外层循环，仅检查是否得到目标个体
	while(flag):
		generations = 0
		init()
		get_fitness()
		# Check if we get the target individual and the generations is below maximum
		# 内层循环，检查是否得到目标个体以及本次模拟是否超过最大代数，若超过则重新模拟
		while(flag and (generations < MAX_GENS)):
			mate()
			mutate()
			get_fitness()
			generations += 1
			# 输出当前种群中第一个个体的适应度和当前代数
			print("the first individual's fitness of generation " + str(generations) + " is " + str(fitness_list[0]))
			flag = check()
    		
if __name__ == '__main__':
    main()
