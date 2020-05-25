from math import *
from random import *

ALPHA = 0.5
D = 1
H = 0.02
S0 = H
T = 3/ALPHA
Tf = 1/ALPHA
Kf = sqrt((2*D)/(ALPHA*S0))

def Psi(t):
	return randint(0, round(t))/100

def Filter(x_prev, psi):
	return (-1/Tf*x_prev+(Kf/Tf)*psi)

def ModelStep(x_prev, rand_value):
	return (x_prev+Filter(x_prev, rand_value)*H)

def CalcModel(seed, psi, n):
	rand_values = []
	t_start = H
	values = []
	for i in range(0, n):
		if len(values) == 0:
			values.append(ModelStep(seed, psi[i]))
		else:
			values.append(ModelStep(values[-1], psi[i]))
	return values
	
def CalcKorrFunc(t):
	return D*exp(-ALPHA*fabs(t))
	
def CalcEmpKorrFunc(proc):
	#находим мат-ожидание
	n = len(proc)
	mx = sum(proc)/n
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

def getCorrValues(psi, n):
	seed = randint(0, 1000)/1000
	proc = CalcModel(seed, psi, n)
	return proc

def CalcCorrFunctions(proc):
	tStep = 0
	KorrFunc = []
	while tStep <= T:
		KorrFunc.append(CalcKorrFunc(tStep))
		tStep += H
	EmpKorrFunc = CalcEmpKorrFunc(proc)
	return [KorrFunc, EmpKorrFunc]