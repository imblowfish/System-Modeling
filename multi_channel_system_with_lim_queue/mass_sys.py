#система массового обслуживания
from rand_generator import GetRandValue

class MassSys:
	lamb = 3								#интенсивность потока заявок
	mu = 4									#производительность канала
	T = 100									#количество времени на один эксперимент
	logTime = 10							#на протяжении скольких секунд выводить информацию о работе системы
	qN = 0									#количество событий отказа принятия заявки
	n = 1
	m = 4
	def __init__(self):
		#первую заявку считаем отработанной
		self.t = 0
		self.N = 0							#кол-во поступивших заявок
		self.M = 0							#кол-во обработанных заявок
		self.k = 0							#кол-во занятых каналов
		self.r = 0							#занятые места в очереди
	#одна серия опыта
	def experiment_step(self, n=-1):
		if n < 0:
			while self.t < self.T:
				#генерируем интервал до поступления следующей заявки
				dt = GetRandValue(self.lamb)
				if self.k == 0:
					self.N += 1
					self.M += 1
					self.k += 1
					if self.t <= self.logTime:
						print(f"Новая заявка поступила и принята на обслуживание. Поступивших заявок {self.N}, обслуженных {self.M}, занятых каналов {self.k} из {self.n}")
					self.t += dt
				elif self.k > 0:
					#интервал до окончания обслуживания заявки
					dtau = GetRandValue(self.mu * self.k)
					if dt < dtau:
						self.N += 1
						if self.t <= self.logTime:
							print(f"Поступила новая заявка, поступивших заявок {self.N}")
						self.t += dt
						if self.k < self.n:
							self.M += 1
							self.k += 1
							if self.t <= self.logTime:
								print(f"Заявка поступает на обслуживание в свободный канал, обслуженных заявок {self.M}, занятых каналов {self.k} из {self.n}")
						elif self.k == self.n and self.r < self.m:
							self.M += 1
							self.r += 1
							if self.t <= self.logTime:
								print(f"Заявка занимает место в очереди, количество обслуженных заявок {self.M}, мест в очереди занято {self.r} из {self.m}")
						else:
							self.qN += 1
							if self.t <= self.logTime:
								print(f"Заявке отказано в обслуживании")
					else:
						self.t += dtau
						if self.r == 0:
							self.k -= 1
							if self.t <= self.logTime:
								print(f"Один канал освобождается, занято каналов {self.k} из {self.n}")
						elif self.r > 0:
							self.r -= 1
							if self.t <= self.logTime:
								print(f"Заявка переходит из очереди на обслуживание, занято мест в очереди {self.r} из {self.m}")
					if self.t <= self.logTime:
						print(f"Прошло {self.t} с")
						print("-------------------")
						#input()
		else:
			for i in range(0, n):
				#генерируем интервал до поступления следующей заявки
				dt = GetRandValue(self.lamb)
				if self.k == 0:
					self.N += 1
					self.M += 1
					self.k += 1
					self.t += dt
				elif self.k > 0:
					#интервал до окончания обслуживания заявки
					dtau = GetRandValue(self.mu * self.k)
					if dt < dtau:
						self.N += 1
						self.t += dt
						if self.k < self.n:
							self.M += 1
							self.k += 1
						elif self.k == self.n and self.r < self.m:
							self.M += 1
							self.r += 1
						else:
							self.qN += 1
					else:
						self.t += dtau
						if self.r == 0:
							self.k -= 1
						elif self.r > 0:
							self.r -= 1
		#оцениваем вероятности
		pstar = self.M/self.N			#вероятность обслуживания
		qstar = (self.N - self.M)/self.N#вероятность отказа в обслуживании
		return pstar, qstar, self.qN, self.N 
				
			
			