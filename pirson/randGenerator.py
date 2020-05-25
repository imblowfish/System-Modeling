'''
Генератор случайной величины по заданному закону распределения
'''

from math import *
from random import *

class RandomGenerator:
	#функция распределения
	def cumulativeDistr(self, x):
		#возвращаем значение -ctg(psi)+1
		return pow(log(x),2)
	#обратная функция распределения
	def revCumulativeDistr(self, psi):
		#arcctg(psi)
		return exp(sqrt(psi))
	#генерация последовательности псевдослучайных чисел по закону распределения
	#n - объем генерируемой выборки
	def GenerateRandomValues(self, n):
		#генерация последовательности
		vec = []
		for i in range(0,n):
			vec.append(self.revCumulativeDistr(random()))
		return vec
	