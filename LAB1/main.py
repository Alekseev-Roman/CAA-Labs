import time

class Square:
    def __init__(self, n):
        self.n = n      # Длина стороны
        self.k = 0      # Кол-во квадратов, которыми можно замостить
        self.squareList = []
        self.squareBoolMap = [[0 for a in range(n)] for b in range(n)]      # Карта заполнения
        self.minPrimeNumber = 1
        self.maxSize = int((n-1)/2)
        self.charMap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

    def print(self):    # Вывод результатов
        print(self.k)
        for element in self.squareList:
            print(*element, sep=' ')

    def pave(self):     # Нахождение минимального числа квадратов, которыми можно замостить квадрат со стороной n
        time_start = time.perf_counter()
        if self.n % 2 == 0:     # Если сторона четной длины
            self.k = 4
            self.squareList.append([1, 1, int(self.n / 2)])
            self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, 0,  int(self.n / 2), 0)

            self.squareList.append([1, 1 + int(self.n / 2), int(self.n / 2)])
            self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, int(self.n / 2),  int(self.n / 2), 1)

            self.squareList.append([1 + int(self.n / 2), 1, int(self.n / 2)])
            self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, int(self.n / 2), 0,  int(self.n / 2), 2)

            self.squareList.append([1 + int(self.n / 2), 1 + int(self.n / 2), int(self.n / 2)])
            self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, int(self.n / 2), int(self.n / 2),  int(self.n / 2), 3)

        else:   # Если сторона нечетной длины
            for i in range(3, int(self.n ** (1/2) + 1)):    # Нахождение минимального просто делителя
                if self.n % i == 0:
                    self.minPrimeNumber = i
                    break

            if self.minPrimeNumber != 1:     # Составные числа
                self.maxSize = int(self.n / self.minPrimeNumber)
                coeff = int(self.minPrimeNumber / 2)

                self.squareList.append([1, 1, self.maxSize*(coeff+1)])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, 0, self.maxSize*(coeff+1), 0)

                self.squareList.append([1, 1 + self.maxSize*(coeff+1), self.maxSize])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, self.maxSize*(coeff+1), self.maxSize*coeff, 1)

                self.squareList.append([1 + self.maxSize*(coeff+1), 1, self.maxSize])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, self.maxSize*(coeff+1), 0, self.maxSize*coeff, 2)

                self.paveRec(self.squareBoolMap, self.squareList, 3, 3)

            else:   # Простые числа
                self.squareList.append([1, 1, self.maxSize + 1])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, 0, self.maxSize + 1, 0)

                self.squareList.append([1, self.maxSize + 2, self.maxSize])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, self.maxSize + 1, self.maxSize, 1)

                self.squareList.append([2 + self.maxSize, 1, self.maxSize])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, self.maxSize + 1, 0, self.maxSize, 2)

                self.paveRec(self.squareBoolMap, self.squareList, 3, 3)

        print('Time:{0:.5f}'.format(time.perf_counter() - time_start))
        #return time.perf_counter() - time_start

    def paveRec(self, squareBoolMap, squareList, k, indexMap):
        if k >= self.k and self.k != 0:
            print('Количество квадратов превысило минимальное количество')    # Промежуточный вывод
            print('Все квадраты со стороной длины 1 и 2 удалены\n')
            return 0

        bufBoolMap = [[a for a in b] for b in squareBoolMap]	# Копирование данных
        bufList = [element for element in squareList]

        x, y = self.searchFreeCoord(bufBoolMap)

        if x < 0 and y < 0:	# Если нельзя вставить ни один квадрат
            if self.k > k or self.k == 0:
                print('Решение сохранено как новое минимальное\n')    # Промежуточный вывод
                print('Все квадраты со стороной длины 1 и 2 удалены\n')
                self.k = k
                self.squareList = bufList
                self.squareBoolMap = bufBoolMap
            else:
                print('Количество квадратов превысило минимальное количество')    # Промежуточный вывод
                print('Все квадраты со стороной длины 1 и 2 удалены\n')
            return 0

        bufX, bufY, maxSize = self.searchMaxSide(bufBoolMap)
        while maxSize == 2:	# Если максимальный квадрат с размером 2
            k += 1
            bufList.append([bufX + 1, bufY + 1, 2])
            self.paveBoolMap(bufBoolMap, bufX, bufY, 2, indexMap)
            print('x:', bufX+1, 'y:', bufY+1, 'w:', 2, '\nk =', k)  # Промежуточный вывод
            self.printMap(bufBoolMap)  # Промежуточный вывод
            indexMap += 1
            bufX, bufY, maxSize = self.searchMaxSide(bufBoolMap)
            if k >= self.k and self.k != 0:
                print('Количество квадратов превысило минимальное количество')    # Промежуточный вывод
                print('Все квадраты со стороной длины 1 и 2 удалены\n')
                return 0

        if maxSize <= 1:	# Если максимальный размер - 1
            for bufY in range(self.maxSize, self.n):
                for bufX in range(self.maxSize, self.n):
                    if not bufBoolMap[bufY][bufX]:
                        k += 1
                        bufList.append([bufX+1, bufY+1, 1])
                        bufBoolMap[bufY][bufX] = self.charMap[indexMap]
                        print('x:', bufX+1, 'y:', bufY+1, 'w:', 1, '\nk =', k)  # Промежуточный вывод
                        self.printMap(bufBoolMap)   # Промежуточный вывод
                        indexMap += 1
                        if k >= self.k and self.k != 0:
                            print('Количество квадратов превысило минимальное количество')    # Промежуточный вывод
                            print('Все квадраты со стороной длины 1 и 2 удалены\n')
                            return 0
            if k < self.k or self.k == 0:
                print('Решение сохранено как новое минимальное\n')    # Промежуточный вывод
                print('Все квадраты со стороной длины 1 и 2 удалены\n')
                self.k = k
                self.squareList = bufList
                self.squareBoolMap = bufBoolMap
            else:
                print('Количество квадратов превысило минимальное количество')    # Промежуточный вывод
                print('Все квадраты со стороной длины 1 и 2 удалены\n')
            return 0

        for m in range(self.maxSize, 0, -1):	# Перебор всех размеров для нового квадрата
            if self.checkSquareCoord(squareBoolMap, x, y, m):
                self.paveBoolMap(bufBoolMap, x, y, m, indexMap)
                print('Вставлен квадрат x:', x+1, 'y:', y+1, 'w:', m, '\nk =', k)  # Промежуточный вывод
                self.printMap(bufBoolMap)  # Промежуточный вывод
                bufList.append([x+1, y+1, m])
                self.paveRec(bufBoolMap, bufList, k+1, indexMap+1)
                self.removePaveBoolMap(bufBoolMap, x, y, m)
                print('Удален квадрат x:', x+1, 'y:', y+1, 'w:', m)
                self.printMap(bufBoolMap)
                bufList.pop()

        return 0

    def searchFreeCoord(self, squareBoolMap):   # Нахождение верхного левого угла свободного от квадратов
        for y in range(self.maxSize, self.n):
            for x in range(self.maxSize, self.n):
                if not squareBoolMap[y][x]:
                    return x, y
        return -1, -1

    def searchSideNewSquare(self, squareBoolMap, newX, newY):   # Нахождение стороны максимально большого квадрата,
        newSideX = newSideY = 0                                 # который можно вставить по заданным координатам
        for x in range(newX, self.n):
            if not squareBoolMap[newY][x]:
                newSideX += 1
            else:
                break
        for y in range(newY, self.n):
            if not squareBoolMap[y][newX]:
                newSideY += 1
            else:
                break
        if newSideX <= newSideY:
            return newSideX
        return newSideY

    def searchMaxSide(self, squareBoolMap):     # Нахождение стороны максимально большого квадрата, который можно
        bufX = bufY = 0                         # вставить в свободную часть
        newSide = 0
        for newY in range(self.maxSize, self.n):
            for newX in range(self.maxSize, self.n):
                bufNewSide = self.searchSideNewSquare(squareBoolMap, newX, newY)
                if bufNewSide > newSide:
                    newSide = bufNewSide
                    bufY = newY
                    bufX = newX
                if bufY + newSide >= self.n:
                    if newSide == 0:
                        return -1, -1, 0
                    return bufX, bufY, newSide
        if newSide == 0:
            return -1, -1, 0
        return bufX, bufY, newSide

    def checkSquareCoord(self, squareBoolMap, x, y, n):    # Можно ли вставить квадрат с заданной
        if x + n > self.n or y + n > self.n:               # стороной на координаты x y
            return False
        for bufY in range(y, y+n):
            side = 0
            for bufX in range(x, x+n):
                if not squareBoolMap[bufY][bufX]:
                    side += 1
            if side < n:
                return False
        return True

    def paveBoolMap(self, squareBoolMap, x, y, n, i):      # Заполнение пустых клеток на карте
        for bufY in range(y, y+n):
            for bufX in range(x, x+n):
                squareBoolMap[bufY][bufX] = self.charMap[i]
        return squareBoolMap

    def removePaveBoolMap(self, squareBoolMap, x, y, n):    # Удаление квадрата на карте по координатам и стороне
        for bufY in range(y, y+n):
            for bufX in range(x, x+n):
                squareBoolMap[bufY][bufX] = 0
        return squareBoolMap

    def printBoolMap(self):     # Вывод карты заполнения
        for y in range(self.n):
            for x in range(self.n):
                print(self.squareBoolMap[y][x], end='')
            print()

    def printMap(self, squareBoolMap):
        for y in range(self.n):
            for x in range(self.n):
                print(squareBoolMap[y][x], end='')
            print()
        print()



n = int(input())
if n < 2 or n > 20:
    print('Неверный ввод')
    exit()
square = Square(n)
square.pave()
square.print()
print('\nИтоговая матрица заполнения:')
square.printBoolMap()

'''squareFile = open("research.txt", "w")   # Исследование

for a in range(2, 21):
        square = Square(a)
        atime = square.pave()
        squareFile.write("(" + str(a) + "; {0:.5f})\n".format(atime))'''

