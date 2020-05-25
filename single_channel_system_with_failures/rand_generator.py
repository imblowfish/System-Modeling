#генератор случайных чисел по экспоненциальному закону

from math import *
from random import *

#den - знаменатель(интенсивность либо производительность) 
def GetRandValue(den):
	#генерация сл. числа с равномерным законом распределения
	psi = random()
	return (-1/den)*log(1-psi)
	