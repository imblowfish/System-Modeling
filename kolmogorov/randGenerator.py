'''
Генератор случайной величины по заданному закону распределения
'''

from math import *
from random import *


class RandomGenerator:
	#функция распределения
	def cumulativeDistr(self, x):
		return 2*sin(x)
	#обратная функция распределения
	def revCumulativeDistr(self, psi):
		return asin(psi/2)
	def plotn(self, z):
		return 2*cos(z)
	#генерация последовательности псевдослучайных чисел по закону распределения
	#n - объем генерируемой выборки
	def GenerateRandomValues(self, n):
		#генерация последовательности
		vec = []
		for i in range(0,n):
			#посылаем случайное число от 0 до 1
			vec.append(self.revCumulativeDistr(random()))
		return vec
	