from totalityWork import *
import matplotlib.pyplot as plt
from tkinter import *
from math import *
from randGenerator import RandomGenerator

#Установка надписей графика и названия
def SetGraphic(title, xname, yname):
	plt.title(title)
	plt.xlabel(xname)
	plt.ylabel(yname)

#Добавление значений характеристик и статистик для дальнейшего вывода
def UpdateStr(n, cFunc, empCFunc, xVals, average, disp, result):
	str="При n=%d"%n+'\n'
	str+="Мат. ожидание=%.4f"%average+'\n'
	str+="Дисперсия=%.4f"%disp+'\n'
	str+="deltaP=%.4f"%result[0]+'\n'
	str+="lambdaP=%.4f"%result[1]+'\n'
	str+=result[2]+'\n'
	str+="------------------\n"
	return str

def main():
	root = Tk()
	root.title("Лабораторная №3")
	root.geometry("250x450")
	strVal = ""
	plt.rcParams.update({'font.size':5})
	nums = [50, 100, 1000, 1000]
	#счетчик для определения области вывода графика
	counter = 1	
	for i in nums:
		print(f"Расчет {i}")
		plt.subplot(2,2,counter)
		#рассчитываем все, что нужно для выборки заданного объема
		[cFunc, empCFunc, xVals, average, disp, result]=GetValues(i)
		#добавляем полученные значения в строку для вывода
		strVal += UpdateStr(i, cFunc, empCFunc, xVals, average, disp, result)
		#устанавливаем надписи на графике
		SetGraphic("При n="+str(i), "x", "F(x) и F*(x)")
		#отрисовываем ФРВ и эмпир. ФРВ
		plt.plot(xVals, cFunc)
		plt.plot(xVals, empCFunc)
		x = xVals[result[-1]]
		y1 = cFunc[result[-1]]
		y2 = empCFunc[result[-1]]
		plt.plot([x,x], [y1, y2])
		counter+=1
	#построение функции плотности
	rg = RandomGenerator()
	plt.figure()
	SetGraphic("Функция плотности", "x", "f(x)")
	zVals = []
	plotVals = []
	zStart = 0
	zEnd = pi/6
	step = zEnd/100
	while zStart <= zEnd:
		zVals.append(zStart)
		plotVals.append(rg.plotn(zStart))
		zStart+=step
	plt.plot(zVals, plotVals)
	#выводим все значения в label
	label = Label(text=strVal, justify=LEFT)
	label.pack()
	#отображаем график
	plt.show()

#начинаем работу программы
main()