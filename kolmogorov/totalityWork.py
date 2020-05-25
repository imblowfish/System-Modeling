'''
Работа с выборкой
'''
from randGenerator import RandomGenerator
from math import *

#нахождение значений ФРВ
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
	
#нахождение значений эмпирической ФРВ
def CalcEmpCumulativeFunc(valsNonSort, steps, n):
	vals = valsNonSort
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
	
#критерий Колмогорова
def Kolmogorov(cFun, eFun, n):
	#максимальное отклонение эмпирической ФРВ от теоретической ФРВ
	deltaP = 0 		
	maxP = 0
	for i in range(0, len(cFun)):
		#рассчитываем 2 случая учитывая взаимное расположение 
		#графиков(выше ФРВ или эмпирическая ФРВ)
		delta1 = fabs(cFun[i] - eFun[i])
		delta2 = fabs(eFun[i] - cFun[i])
		#выбираем среди них максимальную
		if delta1 >= delta2:
			max = delta1
		else:
			max = delta2
		#ищем 
		if max > deltaP:
			deltaP = max
			maxP = i
	#в качестве граничного для области согласия теор. и выб. законов 
	#рассматриваем P = 0.1 со значением лямбды = 1.22
	lamb = 1.22
	lambP = deltaP * sqrt(n)
	result = [deltaP, lambP]
	#если lampdaP < lambda, то считаем, что теор. и выборочной распр. согласуются
	if lambP <= lamb:
		result.append("Нет оснований отвергнуть гипотезу")
	else: 
		result.append("Гипотеза отвергается")
	result.append(maxP)
	return result
	
'''
Расчет всех характеристик и статистик для заданного объема n
1)Генерация последовательности с.в. заданного объема num
2)Нахождение мат.ожидания и дисперсии
3)Расчет значений ФРВ и эмпирической ФРВ для построения графиков
4)Проверяем согласованность ФРВ между собой по критерию Колмогорова
''' 
def GetValues(num):
	rGen = RandomGenerator()
	#генерируем последовательност сл. вел.
	values = rGen.GenerateRandomValues(num)
	#нахождения мат. ожидания и дисперсии
	avg = FindAverage(values)
	disp = FindDispersion(values, avg)
	#находим значения ф-ии распр. и шаги для построения графика
	[cFunc, xValues] = CalcCumulativeFunc(num)
	#находим значения эмпирической ф-ии распр.
	empCFunc = CalcEmpCumulativeFunc(values, xValues, num)
	#проверяем по критерию колмогорова
	result = Kolmogorov(cFunc, empCFunc, num)
	return cFunc, empCFunc, xValues, avg, disp, result