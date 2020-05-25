'''
Работа с выборкой
'''
from randGenerator import RandomGenerator
from math import *

#нахождение значений ФРВ
def CalcCumulativeFunc(num):
	rGen = RandomGenerator()
	start  = 1
	end = 2.71
	step = (end - start)/num
	cumFunc = []
	steps = []
	x = start
	#находим значения функции распределения
	while x < end:
		cumFunc.append(rGen.cumulativeDistr(x))
		steps.append(x)
		x+=step
	return cumFunc, steps
	
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

#нахождение относительных частот
def findFreq(arr):
	#сортируем значения
	arr.sort()
	n = len(arr)
	#m разный в зависимости от шага
	if n <= 500:
		m = n/20
	else:
		m = 3.3*log(n)-1
	xmax = max(arr)
	xmin = min(arr)
	deltaX = (xmax-xmin)/m	
	freqList = []
	#рассчитываем частоты попавших в диапазон значений
	while xmin <= xmax:
		cnt = 0
		for i in arr:
			if i < xmin+deltaX:
				cnt+=1
		freqList.append(cnt/n)
		xmin += deltaX
	return freqList, m

#критерий Пирсона
def Pirson(cFun, eFun):
	[p, m] = findFreq(cFun)
	[pStar, m] = findFreq(eFun)
	n = len(pStar)
	if n > len(p):
		n = len(p)
	#находим значение статистики Хи^2
	hiQuad = 0
	for j in range(0, n):
		hiQuad += pow((pStar[j]-p[j]),2)/p[j]
	#количество параметров теоретического закона(у нас один только x)
	s = 1
	#расчитываем r
	r = m - s - 1
	return [p, pStar, hiQuad, r]
'''
Расчет всех характеристик и статистик для заданного объема n
1)Генерация последовательности с.в. заданного объема num
2)Нахождение мат.ожидания и дисперсии
3)Расчет значений ФРВ для построения графиков
4)Расчет частот для построения диаграммы
4)Проверяем гипотезу о равенстве двух ФРВ по критерию Пирсона
''' 
def GetValues(num):
	rGen = RandomGenerator()
	#генерируем последовательност сл. вел.
	values = rGen.GenerateRandomValues(num)
	#нахождения мат. ожидания и дисперсии
	avg = FindAverage(values)
	disp = FindDispersion(values, avg)
	#находим значения ф-ии распр. и шаги для построения значений
	#будем использовать их для нахождения относительных частот
	[cFunc, xValues] = CalcCumulativeFunc(num)
	cFuncValues = []
	#рассчитываем значения обратной функции по вероятностям полученным из ФРВ
	for i in cFunc:
		cFuncValues.append(rGen.revCumulativeDistr(i))
	cFuncValues.sort()
	values.sort()
	#расчитываем статистику Пирсона
	#result хранит в себе относительные вероятности теор. и эмп.
	#значение статистики Пирсона и число степеней свободы r
	result = Pirson(cFuncValues, values)
	return avg, disp, result