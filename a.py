from deap import base, creator, gp, tools, algorithms
import math
import sys
import numpy
from sklearn import model_selection
from sklearn import metrics
from sklearn.linear_model import LinearRegression

min_tree_depth = 3
max_tree_depth = 5
# The number K for k-fold cross validation
number_splits = 10

input_names = []
input_sets = []
actual_costs = []


def read_file():
    global max_cost,min_cost,input_sets,actual_costs,input_names
    with open(sys.argv[1]) as data:
        for line in data:
            if line[0] != "%" and line[0:9] != "@relation" and line[0:5] != "@data" and line != "\n":
                if line[0:10] == "@attribute":
                    if line.split()[1] != "Effort" and line.split()[1] != "EffortMM" and line.split()[1] != "MM":
                        input_names.append(line.split()[1])
                else:
                    new_inputs = line.split(',')[:-1]
                    for i in range(len(new_inputs)):
                        new_inputs[i] = float(new_inputs[i])
                    input_sets.append(new_inputs)
                    actual_costs.append(float(line.split(',')[-1:][0].split('\n')[0]))

    number_inputs = len(input_names)
    # max_cost = max(actual_costs)
    # min_cost = min(actual_costs)

# split input data into train set and test set
def split_dataset():
    for train_indices, test_indices in model_selection.KFold(number_splits).split(input_sets):
    input_set_train = []
    input_set_test = []
    cost_train = []
    cost_test = []
    for index in train_indices:
        input_set_train.append(input_sets[index])
        cost_train.append(actual_costs[index])
    for index in test_indices:
        input_set_test.append(input_sets[index])
        cost_test.append(actual_costs[index])

    return [input_set_train,input_set_test,cost_train,cost_test]



# some operator between two number (node)
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        return 1
def neg(a):
    return -a

def gen_pset():
    pset=gp.PrimitiveSet("pset",number_inputs)
    pset.addPrimitive(add, 2)
    pset.addPrimitive(sub, 2)
    pset.addPrimitive(mul, 2)
    pset.addPrimitive(div, 2)
    pset.addPrimitive(neg, 1)
    pset.addPrimitive(math.cos, 1)
    pset.addPrimitive(math.sin, 1)
    return pset

def resigter_function():
    toolbox=base.Toolbox()
    toolbox.register("expr", gp.genFull, pset=pset, min_=3, max_=15)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("evaluate", evaluate_soln, input_set_train, cost_train)
    toolbox.register("select", tools.selTournament, tournsize=(math.floor(len(input_set_train) / 2)))

    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=4)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=prim_set)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def evaluate_soln(toolbox,input_sets, actual_costs, node):
    func = toolbox.compile(expr=node)

    if evaluation_method == EvalMethods.MEAN_ABSOLUTE_ERROR:
        sae = 0
        for i, input_set in enumerate(input_sets):
            sae += abs(actual_costs[i] - func(*input_set))
        return [sae / len(input_sets)]
    elif evaluation_method == EvalMethods.ROOT_MEAN_SQUARED_ERROR:
        sumsq = 0
        for i, input_set in enumerate(input_sets):
            sumsq += math.pow((actual_costs[i] - func(*input_set)), 2)
        return [math.sqrt(sumsq / len(input_sets))]

def gene_algorithm(split_res):
    pset=gen_pset()
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)



def linear_regression(split_res):
    linear_reg = LinearRegression()
    linear_reg.fit(input_set_train, cost_train)

    linear_pred = linear_reg.predict(input_set_test)


def main():
    read_file()
    split_res=split_dataset()
    linear_regression(split_res)
