# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:仲逊
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        #初始化
        self.birth_prob=birth_prob
        self.death_prob=death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        #有death_prob的可能性返回真
        return random.random()<self.death_prob

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        #reproduce概率为self.birth_prob * (1 - pop_density)
        probability=self.birth_prob * (1 - pop_density)
        #有probability的可能性繁殖，没有则抛出异常
        if(random.random()<probability):
            return SimpleBacteria(self.birth_prob,self.death_prob)
        else:
            raise NoChildException()

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        #初始化
        self.bacteria=bacteria.copy()
        self.max_pop=max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        #返回细菌种群数量
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        #去掉死亡的细菌
        new_bacteria=[one for one in self.bacteria if not one.is_killed()]
        #当前细菌密度=当前细菌数/最大量 
        cur_pop_dens=len(new_bacteria)/self.max_pop
        #拷贝一份列表，防止迭代时列表被修改
        tem_bacteria=new_bacteria.copy()
        
        for one in tem_bacteria:
            try:
                #细菌根据当前密度进行繁衍
                child = one.reproduce(cur_pop_dens)
                #没有抛出异常则繁衍成功，加进列表
                new_bacteria.append(child)
            #否则无需加入列表
            except NoChildException:
                continue
        
        self.bacteria=new_bacteria
        return self.get_total_pop()


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    #总数量
    total_pop=0
    #遍历第n时间的数量求和
    for i in range(len(populations)):
        total_pop+=populations[i][n]
    #返回平均数
    return total_pop/len(populations)


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    #二维列表 populations[i][j]是i次实验j时间的细菌数
    populations=[]
    #num_trials次实验
    for _ in range(num_trials):
        #初始化为num_bacteria个SimpleBacteria的列表
        bacteria=[SimpleBacteria(birth_prob,death_prob) for i in range(num_bacteria)]
        patient=Patient(bacteria,max_pop)
        #每次实验得到300个时间步长得到的细菌数列表
        populations.append([patient.update() for i in range(300)])
    return populations


# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)
# avg_pop=[calc_pop_avg(populations, n) for n in range(300)]
# make_one_curve_plot(range(300),avg_pop,"Timestep","Average population","Without Antibiotic")

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    #得到平均数量
    mean=calc_pop_avg(populations,t)
    #遍历t时间步长的数量求其与平均数差的平方和
    total_square=0
    for i in range(len(populations)):
        total_square+=(populations[i][t]-mean)**2
    #sqrt(平方和/总数)即为标准差std
    return math.sqrt(total_square/len(populations))

def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    #得到平均数量
    mean=calc_pop_avg(populations,t)
    #得到标准差
    std=calc_pop_std(populations,t)
    #1.96*标准差/sqrt(数量)即为SEM
    return (mean,1.96*std/math.sqrt(len(populations)))


##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        #初始化
        super().__init__(birth_prob, death_prob)
        self.resistant=resistant
        self.mut_prob=mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        #有抗药性则有death_prob概率返回true
        if self.get_resistant():
            return random.random()<self.death_prob
        #没有则有death_prob/4概率返回true
        else:
            return random.random()<self.death_prob/4

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        #繁殖概率=birth_prob*(1-pop_density)
        repro_prob=self.birth_prob*(1-pop_density)
        #如果成功繁殖
        if random.random()<repro_prob:
            resi_prob=self.mut_prob*(1-pop_density)
            #则其后代有resi_prob概率有抗药性
            if self.get_resistant() or random.random()<resi_prob:
                return ResistantBacteria(self.birth_prob, self.death_prob,True,self.mut_prob)
            #有1-resi_prob概率没有抗药性
            else:
                return ResistantBacteria(self.birth_prob, self.death_prob,False,self.mut_prob)
        #没有成功繁殖，抛异常
        else:
            raise NoChildException
            
class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        #初始化
        super().__init__(bacteria,max_pop)
        self.on_antibiotic=False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic=True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        #统计细菌列表中有抗药性的数量
        return sum([1 for one in self.bacteria if one.get_resistant()])

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        #去掉死亡的细菌
        new_bacteria=[one for one in self.bacteria if not one.is_killed()]
        #如果病人已经服用过抗生素
        if self.on_antibiotic:
            #则把没有抗生素抗性的细菌去掉
            resist_bacteria=[one for one in new_bacteria if one.get_resistant()]
            new_bacteria=resist_bacteria
        #当前细菌密度=当前细菌数/最大量    
        cur_pop_dens=len(new_bacteria)/self.max_pop
        #拷贝一份列表，防止迭代时列表被修改
        tem_bacteria=new_bacteria.copy()
        for one in tem_bacteria:
            try:
                #细菌根据当前密度进行繁衍
                child = one.reproduce(cur_pop_dens)
                #没有抛出异常则繁衍成功，加进列表
                new_bacteria.append(child)
            #否则无需加入列表
            except NoChildException:
                continue
        
        self.bacteria=new_bacteria
        return self.get_total_pop()



##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    #total_pop_list[i][j]表示第i次实验j时间的细菌总数量
    total_pop_list=[]
    #total_resistant_pop_list[i][j]表示第i次实验j时间的抗药细菌总数量
    total_resistant_pop_list=[]

    for _ in range(num_trials):
        #列表初始化为num_bacteria个细菌
        bacteria=[ResistantBacteria(birth_prob, death_prob, resistant, mut_prob)]*num_bacteria
        patient=TreatedPatient(bacteria, max_pop)  
        #一次实验中各个时间的细菌总数和抗药细菌总数
        pop_list=[]
        resistant_pop_list=[]
        #未服用抗生素，实验150个时间步
        for _ in range(150):
            #分别将两种细菌总数加入列表
            pop_list.append(patient.get_total_pop())
            resistant_pop_list.append(patient.get_resist_pop())
            patient.update()   
       #服用抗生素，实验250个时间步
        patient.set_on_antibiotic()
        for _ in range(250):
            #分别将两种细菌总数加入列表
            pop_list.append(patient.get_total_pop())
            resistant_pop_list.append(patient.get_resist_pop())
            patient.update()
        #把一次实验的结果加进对应列表   
        total_pop_list.append(pop_list)   
        total_resistant_pop_list.append(resistant_pop_list) 
    
    return (total_pop_list, total_resistant_pop_list)



# When you are ready to run the simulations, uncomment the next lines one
# at a time
#
#total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.3,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)
#avg_total_pop=[calc_pop_avg(total_pop, n) for n in range(400)]
#avg_resistant_pop=[calc_pop_avg(resistant_pop, n) for n in range(400)]
#make_two_curve_plot(range(400), 
#                    avg_total_pop, 
#                    avg_resistant_pop, 
#                    'Total', 'Resistant', 
#                    'Timestep', 'Average population', 
#                    'With an Antibiotic') 
#print('95% confidence interval for the total population estimate at time step 299:',calc_95_ci(total_pop,299))  
#print('95% confidence interval for the resistant bacteria estimate at time step 299:',calc_95_ci(resistant_pop,299))  
#  
#    
#total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.17,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)
#avg_total_pop=[calc_pop_avg(total_pop, n) for n in range(400)]
#avg_resistant_pop=[calc_pop_avg(resistant_pop, n) for n in range(400)]
#make_two_curve_plot(range(400), 
#                    avg_total_pop, 
#                    avg_resistant_pop, 
#                    'Total', 'Resistant', 
#                    'Timestep', 'Average population', 
#                    'With an Antibiotic') 
#print('95% confidence interval for the total population estimate at time step 299:',calc_95_ci(total_pop,299))  
#print('95% confidence interval for the resistant bacteria estimate at time step 299:',calc_95_ci(resistant_pop,299))