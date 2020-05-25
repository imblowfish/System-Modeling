'''
Работа с выборкой
'''
from randGenerator import RandomGenerator
from math import *
from random import *

def revCumNorm(x):
	func = 1/sqrt(2*pi)
	func *= exp((-x**2)/2)
	res = sqrt(-2 * log(sqrt(2*pi)*func))
	return res
	
def CalcNorm(num):
	cumFunc = []
	steps = []
	for i in range(0, num):
		x = revCumNorm(random())
		steps.append(x)
		#cumFunc.append(0.5+Fi(x))
	return cumFunc, steps 

#нахождение значений ФРВ заданным в варианте
def CalcCumulativeFunc(num):
	rGen = RandomGenerator()
	left = 0
	right = pi/6
	step = (right - left)/num
	cumFunc = []
	steps = []
	#находим значения функции распределения
	while left <= right:
		x = left
		cumFunc.append(rGen.cumulativeDistr(x))
		steps.append(x)
		left+=step
	return cumFunc, steps
	
#нахождение значений эмпирической ФРВ заданной в варианте
def CalcEmpCumulativeFunc(valsNonSort, steps, n):
	vals = valsNonSort.copy()
	#сортируем выборку
	vals.sort()
	res = []
	for i in steps:
		sum = 0
		for j in vals:
			#считаем кол-во xi <= x
			if j <= i:
				sum+=1
			else:
				break
		#записываем вероятность nx/n
		res.append(sum/n)
	return res
	
#нахождение мат ожидания
def FindAverage(vec):
	avg = 0
	for num in vec:
		avg += num
	return avg/len(vec)
	
#нахождение дисперсии
def FindDispersion(vec, avg):
	disp = 0
	for num in vec:
		disp += pow(num-avg,2)
	return disp/(len(vec)-1)
	
#получение двух значений распр по стандартизированному  нормальному закону
def getNormalValues():
	while True:
		psi1 = random()
		psi2 = random()
		V1 = 2*psi1 - 1
		V2 = 2*psi2 - 1
		s = V1**2 + V2**2
		if s >= 1 or s == 0:
			continue
		break
	r = sqrt(-2*log(s)/s)
	#получаем 2 распр по стандартизированному закону числа
	return [V1*r, V2*r]
	
#ряд для расчета интеграла вероятностей
def Fi(x):
	sum = 1
	power = 2
	val = 3
	eps = 0.01	#точность для определения влияния очередного члена ряда
	i = 1
	while True:
		prevSum = sum
		sum += (-1)**i * ((x**power)/(2**i*factorial(i)*val))
		val+=2
		power+=2
		i+=1
		if fabs(prevSum-sum) < eps:
			break
	return (x/sqrt(2*pi))*sum
	
#преобразование нормального закона распр. в равномерный
def getUniformValues(norm):
	unif = []
	for i in range(0, len(norm)):
		unif.append(0.5+Fi(norm[i]))
	return unif
	
#Колмогоров-Смирнов
def Kolmogorov_Smirnov(F1, F2):
	deltaP = 0
	m = len(F1)
	n = len(F2)
	for i in range(0, m):
		delta1 = fabs(F1[i] - F2[i])
		delta2 = fabs(F2[i] - F1[i])
		if delta1 >= delta2:
			max = delta1
		else:
			max = delta2
		if max > deltaP:
			deltaP = max
	lamb = 1.22
	lambP = deltaP * sqrt((m*n)/(m+n))
	result = [deltaP, lambP]
	#если lampdaP < lambda, то считаем, что теор. и выборочной распр. согласуются
	if lambP <= lamb:
		result.append(True)
	else: 
		result.append(False)
	return result