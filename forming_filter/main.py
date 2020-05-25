from math import *
from random import *
from randGenerator import RandomGenerator
import matplotlib.pyplot as plt
import filter
import totalityWork as tw

def DrawGraphic(title, xname, yname, x, y, scatter=False, bar=False):
	#plt.rcParams.update({'font.size':5})
	plt.title(title)
	plt.xlabel(xname)
	plt.ylabel(yname)
	if scatter == True:
		plt.scatter(x,y, s=0.1)
	elif bar == True:
		ax = plt.gca()
		ax.bar(x,y,align='edge', alpha=0.5)
	else:
		plt.plot(x, y, linewidth = 1)


def main():
	rGen = RandomGenerator()
	plt.rcParams.update({'font.size':4})
	#получим количество случайных величин n/2
	n = 10000
	'''
	Этап 1) Преобразование равномерного закона распр. 
	белого шума в стандартизированный нормальный закон распр.
	'''
	normalValues = []
	for i in range(0, round(n/2)):
		normalValues.extend(tw.getNormalValues())
	#проверка по стьюденту
	avg = tw.FindAverage(normalValues)
	disp = tw.FindDispersion(normalValues, avg)
	t = ((0-avg)*sqrt(len(normalValues)))/sqrt(disp)
	t = fabs(t)
	tReal = len(normalValues) - 1
	#минимальное значение критерия для большого количества элементов обычно 1.2, округлим до 1
	plt.subplot(5,1,1)
	print("ЭТАП 1")
	print("Результат проверки по критерию Стьюдента")
	print("t = %.2f"%t)
	if t < 1.2:
		print("Не отвергаем гипотезу о стандартизированном нормальном распределении")
	else:
		print("Отвергается гипотеза о стандартизированном нормальном распределении")
	korrFunc = filter.CalcEmpKorrFunc(normalValues)
	DrawGraphic("Нормальные значения 1 этап", "x", "value", range(0, len(normalValues)), normalValues, scatter=True)
	'''
	Этап 2)обеспечение требуемых корр. свойств с 
	помощью формирующего фильтра
	'''
	corrValues = filter.getCorrValues(normalValues, n)
	plt.subplot(5,1,2)
	#построение графиков для проверки соответствия
	[korrFunc, empKorrFunc] = filter.CalcCorrFunctions(corrValues)
	DrawGraphic("Соответствие корр. ф-ий 2 этап", "t", "K(t)", range(0, len(korrFunc)), korrFunc)
	DrawGraphic("Соответствие корр. ф-ий 2 этап", "t", "K*(t)", range(0, len(empKorrFunc)), empKorrFunc)
	'''
	Этап 3)преобразование нормального закона распр ген.
	процесса в равномерный
	'''
	uniformValues = tw.getUniformValues(corrValues)
	#проверка на равномерность
	[pStar, p, hi, r, xValues, cFunc] = tw.Pirson(uniformValues)
	#строим гистограмму
	plt.subplot(5,1,3)
	DrawGraphic("Проверка на равномерность 3 этап", "t", "K(t)", range(len(pStar)), pStar, bar=True)
	DrawGraphic("Проверка на равномерность 3 этап", "t", "K(t)", range(len(p)), p, bar=True)
	#!!!!plt.figure()
	#plt.subplot(4,2,6)
	#DrawGraphic("Равномерные значения после 3 этапа", "x", "value", range(len(uniformValues)), uniformValues, scatter=True)
	#print("левая графница a=%.2f b=%.2f"%(min(uniformValues), max(uniformValues)))
	'''
	Этап 4)обеспечение требуемого закона распределения
	'''
	result = rGen.GenerateValues(uniformValues, n)
	#проверка на соответствие законов распределения друг другу
	#получаем значение теор функции
	[cFunc, xValues] = tw.CalcCumulativeFunc(n)
	#получаем значения эмп функции
	empFunc = tw.CalcEmpCumulativeFunc(result, xValues, n)
	#проверяем по Колмогорову
	'''
	методы восстановления законов критерия согласия предусматривают
	отсутствие взаимной зависимости реализаций сл. вел.
	n/20, т.к. есть взаимная зависимость в реализации коррелированного с.п.,
	а значит берем элементы из выборки с большим шагом, чтобы хоть как-то
	избежать влияния на результат
	'''
	kolmAnswer = tw.Kolmogorov(cFunc, empFunc, round(n/40))
	#выводим графики
	plt.subplot(5,1,4)
	DrawGraphic("Соответствие ФРВ 4 этап", "x", "F(x) и F*(x)", xValues, cFunc)
	DrawGraphic("Соответствие ФРВ 4 этап", "x", "F(x) и F*(x)", xValues, empFunc)
	
	plt.subplot(5,1,5)
	korrFunc = filter.CalcEmpKorrFunc(result)
	[korrFunc, empKorrFunc] = filter.CalcCorrFunctions(corrValues)
	DrawGraphic("Соответствие корр. ф-ий 4 этап", "t", "K(t)", range(0, len(korrFunc)), korrFunc)
	DrawGraphic("Соответствие корр. ф-ий 4 этап", "t", "K*(t)", range(0, len(empKorrFunc)), empKorrFunc)
	print("lambdaP=%.4f"%kolmAnswer[1])
	print(kolmAnswer[2])
	#вывод мат.ожидания и дисперсии
	avg = tw.FindAverage(result)
	disp = tw.FindDispersion(result, avg)
	print("Мат. ожидание=%.4f"%avg)
	print("Дисперсия=%.4f"%disp)
	plt.show()
	
	
main()