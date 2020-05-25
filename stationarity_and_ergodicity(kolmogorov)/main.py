from math import *
from random import *
from randGenerator import RandomGenerator
import matplotlib.pyplot as plt
import filter
import totalityWork as tw
		
def generateProcess():
	rGen = RandomGenerator()
	n = 10000
	normalValues = []
	for i in range(0, round(n/2)):
		normalValues.extend(tw.getNormalValues())
	corrValues = filter.getCorrValues(normalValues, n)
	uniformValues = tw.getUniformValues(corrValues)
	result = rGen.GenerateValues(uniformValues, n)
	return result


def main():
	#генераций num реализаций сл. процесса, в каждом по 10000 значений
	processes = []
	num = 100
	for i in range(0, num):
		processes.append(generateProcess())
	#t1 и t2 случайные моменты времени в реализациях
	t1 = randint(0, len(processes[0]))
	t2 = randint(0, len(processes[0]))
	p1 = []
	p2 = []
	[cFunc, xValues] = tw.CalcCumulativeFunc(num)
	#берем значения случ. процессов, соответствующие моменту времени t1 и t2
	for proc in processes:
		p1.append(proc[t1])
		p2.append(proc[t2])
	#расчитываем статистические функции распределения
	F1 = tw.CalcEmpCumulativeFunc(p1, xValues, num)								#для момента t1
	F2 = tw.CalcEmpCumulativeFunc(p2, xValues, num)								#для момента t2
	step = round(len(processes[0])/num)											#закомментировать
	p3 = processes[0][0:len(processes[0]):step]									#закомментировать
	F3 = tw.CalcEmpCumulativeFunc(p3, xValues, num)								#закомментировать
	#[cFunc, xValues2] = tw.CalcCumulativeFunc(len(processes[0]))
	#F3 = tw.CalcEmpCumulativeFunc(processes[0], xValues2, len(processes[0]))	#для одной реализации случайного процесса
	#проверяем по Колмогорову-Смирнову
	result = tw.Kolmogorov_Smirnov(F1, F2)										#сравниваем распределения значений в моменты времени t1 и t2
	result2 = tw.Kolmogorov_Smirnov(F1, F3)										#сравниваем распределения значений в t1 и в одной реализации
	print("deltaP=%.4f"%result[0])
	print("lambdaP=%.4f"%result[1])
	if result[2] == True:
		print("Выборки однородны")
	else:
		print("Выборки не однородны")
	print("deltaP=%.4f"%result2[0])
	print("lambdaP=%.4f"%result2[1])
	if result2[2] == True:
		print("Процесс эргодичен")
	else:
		print("Процесс не эргодичен")
	plt.title("t1 и t2")
	plt.xlabel("x")
	plt.ylabel("F*(x)")
	plt.plot(xValues, F1)
	plt.plot(xValues, F2)
	plt.figure()
	plt.title("t1 и реализация")
	plt.plot(xValues, F1)
	plt.plot(xValues, F3)														#закомментировать
	#plt.plot(xValues2, F3)
	plt.show()
	
main()