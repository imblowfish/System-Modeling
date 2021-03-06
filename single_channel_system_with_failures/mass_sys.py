#система массового обслуживания
from rand_generator import GetRandValue

class MassSys:
	lamb = 3								#интенсивность потока заявок
	mu = 4									#производительность канала
	T = 100									#количество времени на один эксперимент
	logTime = 10							#на протяжении скольких секунд выводить информацию о работе системы
	qN = 0									#количество событий отказа принятия заявки
	def __init__(self):
		#первую заявку считаем отработанной
		self.t = 0
		self.N = 1							#кол-во поступивших заявок
		self.M = 1							#кол-во обработанных заявок
	#одна серия опыта
	def experiment_step(self, n=-1):
		if n >= 0:
			for i in range(0, n):
				#генерируем интервал до поступления следующей заявки
				dt = GetRandValue(self.lamb)
				#увеличиваем кол-во поступивших заявок
				self.N += 1
				#и интервал до окончания обслуживания заявки
				dtau = GetRandValue(self.mu)
				if dt >= dtau:			#если успели завершить до следующей
					self.M += 1			#добавляем к обслуженным
				else: 					#если к наступлению след. текущая не завершена 
					self.qN += 1
				self.t += dt			#увеличиваем время
		else:
			self.t = GetRandValue(self.lamb)
			print("Первая заявка поступает на обслуживание")
			while self.t < self.T:
				#генерируем интервал до поступления следующей заявки
				dt = GetRandValue(self.lamb)
				#увеличиваем кол-во поступивших заявок
				self.N += 1
				if self.t <= self.logTime:
					print(f"Поступление очередной заявки, количество поступивших заявок: {self.N}")
				#и интервал до окончания обслуживания заявки
				dtau = GetRandValue(self.mu)
				if dt >= dtau:			#если успели завершить до следующей
					self.M += 1			#добавляем к обслуженным
					if self.t <= self.logTime:
						print(f"Канал свободен, заявка обслуживается, количество обслуженных заявок(поставленных на обслуживание):{self.M}")
						print("dt=%.4f >= dtau=%.4f"%(dt, dtau))
				else: 					#если к наступлению след. текущая не завершена 
					self.qN += 1
					if self.t <= self.logTime:
						print(f"Обслуживание предыдущей не завершено, отказ в обслуживании поступившей заявке, обслуженных заявок(поставленных на обслуживание):{self.M}")
						print("dt=%.4f < dtau=%.4f"%(dt, dtau))
				self.t += dt			#увеличиваем время
				if self.t <= self.logTime:
					print(f"Прошло {self.t} с")
					print("------------------")
					#input()
		#оцениваем вероятности
		pstar = self.M/self.N			#вероятность обслуживания
		qstar = (self.N - self.M)/self.N#вероятность отказа в обслуживании
		return pstar, qstar, self.qN, self.N 
				
			
			