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
			if i >= xmin and i <= xmin+deltaX:
				cnt+=1
		freqList.append(cnt/n)
		xmin += deltaX
	return freqList, m

#критерий Колмогорова
def Kolmogorov(cFun, eFun, n):
	#максимальное отклонение эмпирической ФРВ от теоретической ФРВ
	deltaP = 0			
	for i in range(0, len(cFun)-1,20):
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
			#print(deltaP)
	#в качестве граничного для области согласия теор. и выб. законов 
	#рассматриваем P = 0.1 со значением лямбды = 1.22
	lamb = 1.22
	lambP = deltaP * sqrt(n)
	result = [deltaP, lambP]
	print("4 ЭТАП")
	#если lampdaP < lambda, то считаем, что теор. и выборочной распр. согласуются
	if lambP <= lamb:
		result.append("Нет оснований отвергнуть гипотезу")
	else: 
		result.append("Гипотеза отвергается")
	return result

def revUniform(a, b, rand):
	return rand/(b-a)+a
	
def uniformCumFun(x, a, b):
	return (x-a)/(b-a)
	
#критерий Пирсона
def Pirson(eFun):
	#опреляем графницы ф-ии распр
	a = min(eFun)
	b = max(eFun)
	cFun = []
	xValues = []
	#находим значения обратной ф-ии норм распределения
	for i in range(0, len(eFun)):
		randVal = random()
		revVal = revUniform(a, b, randVal)
		xValues.append(revVal)
		cFun.append(uniformCumFun(revVal, a, b))
	#рассчитываем частоты
	[p, m] = findFreq(xValues)
	[pStar, m] = findFreq(eFun)
	n = len(p)
	#находим значение статистики Хи^2
	hiQuad = 0
	for j in range(0, len(pStar)):
		hiQuad += pow((pStar[j]-p[j]),2)/p[j]
	#количество параметров теоретического закона(у нас один только x)
	#m = len(pStar)
	#расчитываем r
	r = m - 3
	print("ЭТАП 3")
	print("Хи-квадрат=%.5f"%hiQuad)
	print("r=%.5f"%r)
	#1.6 минимальное в таблице распр Пирсона, если прям очень равны, то будет близко к нулю
	if hiQuad < 1.6:
		print("Не отвергаем, что равномерный")
	else:
		print("Отвергаем, что равномерный")
	return [pStar, p, hiQuad, r, xValues, cFun]