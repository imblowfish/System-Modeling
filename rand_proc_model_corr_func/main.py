from math import *
from random import *
import matplotlib.pyplot as plt

ALPHA = 0.5
D = 5
H = 0.02
S0 = H/12
T = 3/ALPHA
Tf = 1/ALPHA
Kf = sqrt((2*D)/(ALPHA*S0))

unVal = []

def DrawGraphic(title, xname, yname, x, y):
	plt.rcParams.update({'font.size':5})
	plt.title(title)
	plt.xlabel(xname)
	plt.ylabel(yname)
	plt.plot(x, y, linewidth = 1)

def Filter(x_prev, psi):
	return (-1/Tf*x_prev+(Kf/Tf)*psi)

def ModelStep(x_prev, rand_value):
	return (x_prev+Filter(x_prev, rand_value)*H)

def CalcModel(seed, n):
	rand_values = []
	t_start = H
	values = []
	for i in range(0, n):
		if len(values) == 0:
			psi = random()-0.5				#центрирование
			unVal.append(psi)
			values.append(ModelStep(seed, psi))
		else:
			psi = random()-0.5				#центрирование
			unVal.append(psi)
			values.append(ModelStep(values[-1], random()))
	return values
	
def CalcKorrFunc(t):
	return D*exp(-ALPHA*fabs(t))
	
	
def CalcEmpKorrFunc(proc):
	#находим мат-ожидание
	n = len(proc)
	mx = sum(proc)/n
	Dx = 0
	for i in range(0, n):
		Dx += pow((proc[i] - mx), 2)
	Dx /= n-1
	#находим эмп. корр. функцию
	korr = []
	calcVal = 0
	steps = T/H
	for j in range(0, round(steps)):
		for i in range(0, n-j-1):
			calcVal += (proc[i]-mx)*(proc[i+j]-mx)
		calcVal /= (n-j*H)
		#делим на дисперсию, получаем нормированную эмп. корр. функцию
		korr.append(calcVal)
	return korr

def main():
	seed = 50
	proc = CalcModel(seed, 20000)
	plt.figure()
	#вывод случайного процесса
	DrawGraphic("Случайный процесс", "t", "x(t)", range(0, len(proc)), proc)
	#вывод корреляционной функции и теоретической корреляционной функции
	tStep = 0
	KorrFunc = []
	while tStep <= T:
		KorrFunc.append(CalcKorrFunc(tStep))
		tStep += H
	plt.figure()
	DrawGraphic("Соответствие корр. ф-ий", "t", "K(t) и K*(t)", range(0, len(KorrFunc)), KorrFunc)
	#вывод графика эмп. корр. функции
	EmpKorrFunc = CalcEmpKorrFunc(proc)
	DrawGraphic("Соответствие корр. ф-ий", "t", "K(t) и K*(t)", range(0, len(EmpKorrFunc)), EmpKorrFunc)
	plt.figure()
	DrawGraphic("График белого шума", "n", "g(t)", range(0, 20000) , unVal)
	mx = sum(proc)/len(proc)
	print(f"Мат ожидание = {mx}")
	Dx = 0
	for i in range(0, len(proc)):
		Dx += pow((proc[i] - mx), 2)
	Dx /= len(proc)-1
	print(f"Дисперсия {Dx}")
	plt.show()
	
main()