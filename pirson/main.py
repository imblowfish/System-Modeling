from totalityWork import *
import matplotlib.pyplot as plt
from tkinter import *

#Настройка гистограммы
def SetHist(arr):
	s = arr
	x = range(len(arr))
	ax = plt.gca()
	ax.bar(x,s,align='edge', alpha=0.5)

#Добавление значений характеристик и статистик для дальнейшего вывода
def UpdateStr(n, average, disp, res):
	str="При n=%d"%n+'\n'
	str+="Мат. ожидание=%.4f"%average+'\n'
	str+="Дисперсия=%.4f"%disp+'\n'
	str+="hiQuad=%.4f"%res[2]+'\n'
	str+="r=%.4f"%res[3]+'\n'
	str+="------------------\n"
	return str

def main():
	root = Tk()
	root.title("Лабораторная №3")
	root.geometry("250x450")
	strVal = ""
	plt.rcParams.update({'font.size':5})
	nums = [50, 100, 1000, 10000]
	#счетчик для определения области вывода графика
	counter = 1	
	for i in nums:
		plt.subplot(2,2,counter)
		#рассчитываем все, что нужно для выборки заданного объема
		[average, disp, result]=GetValues(i)
		#добавляем полученные значения в строку для вывода
		strVal += UpdateStr(i, average, disp, result)
		#построение гистограммы эмп. частот и отн. частот
		SetHist(result[0])
		SetHist(result[1])
		counter+=1
	#выводим все значения в label
	label = Label(text=strVal, justify=LEFT)
	label.pack()
	#отображаем график
	plt.show()

#начинаем работу программы
main()