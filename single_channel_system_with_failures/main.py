#главный файл
from mass_sys import MassSys
from math import sqrt
from math import fabs
from math import pow

#параметр для нахождения оценки q(вероятность отказа или нахождения в x1 - занят)
#то есть за событие A принимается отказ от выполнения заявки

def print_all(qteor, eps, epsStar, qstar, Ndop=-1):
	#вывод итоговых значений и оценок
	print("Теоретическое q = %.8f"%qteor)
	print("Допустимая погрешность eps = %.2f"%eps)
	print("Оценка погрешности eps* = %.4f"%epsStar)
	print("Оценка q* = %.8f"%qstar)
	if Ndop < 0:
		print("%.8f < %.8f"%(epsStar, eps))
		return 0
	else:
		print("%.8f >= %.8f"%(epsStar, eps))
		
	print("Автоматическое определение рекомендует Nдоп=%d"%Ndop)
	while True:
		num = input("Введите свое количество Nдоп, либо не вводите ничего:")
		if num.isdigit() or num == "":
			break
	if num == "":
		return Ndop
	else:
		return int(num)

def main():
	ms = MassSys()
	#Теоретические находим через calcTeor.py
	pteor = 0.571329							#теор. значение вер. принятия
	qteor = 0.428571							#теор значение вер. отказа
	eps = 0.01									#допустимая погрешность
	ad = 3										#коэф. дов. интервала
	
	probStar = -1								#оценка вероятности
	Ndop = -1									#количество проведений опыта(в начале)
	Nsum = Ndop									#сколько всего раз провели опыт
	NAprev = 0
	Nprev = 0
	#итерационный алгоритм
	while True:
		#проводим эксперимент нужное кол. раз, получаем значение оценок
		#и количество случаев появления события A
		if Ndop >= 0:
			print("\nОПЫТ С КОЛИЧЕСТВОМ ИТЕРАЦИЙ = %d"%Ndop)
			print("ОБЩЕЕ КОЛИЧЕСТВО ИТЕРАЦИЙ = %d"%Nsum)
		[pstar, qstar, NA, N] = ms.experiment_step(Ndop)	
		
		if Ndop < 0:
			print("\nРезультат после 100 с")
		
		if probStar == -1:						#если первая итерация
			probStar = NA/N						#оцениваем вероятность
		else:
			probStar = (NAprev + NA)/(Nprev + N)
		
		temp = (probStar*(1-probStar))
		epsStar = ad*sqrt(temp/N)				#оценка погрешности
		
		if epsStar < eps:
			break
		else:
			Ntreb = (pow(ad, 2) * temp) / (pow(eps, 2)) 	#оценка требуемого кол. опытов
			Ntreb = round(Ntreb)
			#запоминем предыдущие значения Na и N
			NAprev = NA
			Nprev = N
			Ndop = Ntreb - N								#объем дополнительной серии опытов
			Ndop = print_all(qteor, eps, epsStar, qstar, Ndop)
			Nsum += Ndop
	
	print_all(qteor, eps, epsStar, qstar)
	print("Требуемое время наблюдения для оценки q с eps=%.2f = %.2f с"%(eps, ms.t))
	
main()