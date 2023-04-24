import copy

class Square:
    def __init__(self, n):
        self.n = n      # Длина стороны
        self.k = 0      # Кол-во квадратов, которыми можно замостить
        self.squareList = []
        self.squareBoolMap = [[False for a in range(n)] for b in range(n)]      # Карта заполнения
        self.minPrimeNumber = 1

    def print(self):    # Вывод результатов
        print(self.k)
        for element in self.squareList:
            print(*element, sep=' ')

    def pave(self):     # Нахождение минимального числа квадратов, которыми можно замостить квадрат со стороной n
        if self.n % 2 == 0:     # Если сторона четной длины
            self.k = 4
            self.squareList.append([1, 1, int(self.n / 2)])
            self.squareList.append([1, 1 + int(self.n / 2), int(self.n / 2)])
            self.squareList.append([1 + int(self.n / 2), 1, int(self.n / 2)])
            self.squareList.append([1 + int(self.n / 2), 1 + int(self.n / 2), int(self.n / 2)])

        else:   # Если сторона нечетной длины
            for i in range(2, int(self.n ** (1/2) + 1)):    # Нахождение минимального просто делителя
                if self.n % i == 0:
                    self.minPrimeNumber = i
                    break

            if self.minPrimeNumber != 1:     # Составные числа
                size = int(self.n / self.minPrimeNumber)

                self.squareList.append([1, 1, size*2])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, 0, size*2)

                self.squareList.append([1, 1 + size*2, size])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, size*2, size)

                self.squareList.append([1 + size*2, 1, size])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, size*2, 0, size)

                self.paveCompositeNumber(self.squareBoolMap, copy.deepcopy(self.squareList), size, 3)
                #self.pavePrimeNumber(self.squareBoolMap, copy.deepcopy(self.squareList), int((self.n - 1) / 2), 3, False, 0)

            else:   # Простые числа
                self.squareList.append([1, 1, int((self.n + 1) / 2)])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, 0, int((self.n + 1) / 2))

                self.squareList.append([1, 1 + int((self.n + 1) / 2), int((self.n - 1) / 2)])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, 0, int((self.n + 1) / 2), int((self.n - 1) / 2))

                self.squareList.append([1 + int((self.n + 1) / 2), 1, int((self.n - 1) / 2)])
                self.squareBoolMap = self.paveBoolMap(self.squareBoolMap, int((self.n + 1) / 2), 0, int((self.n - 1) / 2))

                g = self.pavePrimeNumber(self.squareBoolMap, copy.deepcopy(self.squareList),  int((self.n-1)/2), 3, False, 0)
                #print(g)

    def paveCompositeNumber(self, squareBoolMap, squareList, n, k):
        x, y = self.searchFreeCoord(squareBoolMap)

        if x > 0 and y > 0:
            k += 1
            if self.k <= k and self.k != 0:
                return 0
            n = self.searchSideNewSquare(squareBoolMap, x, y)
            squareList.append([x+1, y+1, n])
            self.paveBoolMap(squareBoolMap, x, y, n)
            self.paveCompositeNumber(squareBoolMap, copy.deepcopy(squareList), n, k)
        elif self.k > k or self.k == 0:
            self.k = k
            self.squareList = squareList

        return 0

    def pavePrimeNumber(self, squareBoolMap, squareList, n, k, flag, g):
        g += 1
        bufBoolMap = copy.deepcopy(squareBoolMap)
        bufList = copy.deepcopy(squareList)
        bufk = k
        x, y = self.checkSquare(squareBoolMap, n)
        m = n

        if n <= 1 and x < 0 and y < 0:
            if self.k > k or self.k == 0:
                self.k = k
                self.squareList = copy.deepcopy(squareList)
            return g

        if self.k <= k and self.k != 0:
            return g

        if x >= 0 or y >= 0:
            bufList.append([x+1, y+1, n])
            bufk += 1
            print('vvvvvvvvvvvvvvvvvvvvvvvvv')
            for ys in range(self.n):
                for xs in range(self.n):
                    print(int(bufBoolMap[ys][xs]), end=' ')
                print()
            self.paveBoolMap(bufBoolMap, x, y, n)
            print()
            for ys in range(self.n):
                for xs in range(self.n):
                    print(int(bufBoolMap[ys][xs]), end=' ')
                print()
            print('^^^^^^^^^^^^^^^^^^^^^^^^^')
            print()

            if m <= 1:
                self.paveBoolMap(bufBoolMap, 9, 10, 1)
                bufList.append([10, 11, 1])
                k += 1

                for cy in range(self.n):
                    for cx in range(self.n):
                        if not squareBoolMap[cy][cx]:
                            k += 1
                            squareList.append([cx+1, cy+1, 1])
                if self.k > k or self.k == 0:
                    self.k = k
                    self.squareList = copy.deepcopy(squareList)
                return g

            if flag:
                x, y, m = self.searchMaxSide(squareBoolMap)

            g = self.pavePrimeNumber(bufBoolMap, bufList, m, bufk, False, g)
        elif n > 1:
            g = self.pavePrimeNumber(bufBoolMap, bufList, m - 1, bufk, False, g)
        if n > 1 and (x >= 0 or y >= 0):
            g = self.pavePrimeNumber(copy.deepcopy(squareBoolMap), squareList, n - 1, k, True, g)
        return g

    def searchFreeCoord(self, squareBoolMap):   # Нахождение верхного левого угла свободного от квадратов
        for y in range(self.n):
            for x in range(self.n):
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
        for newY in range(self.n):
            for newX in range(self.n):
                bufNewSide = self.searchSideNewSquare(squareBoolMap, newX, newY)
                if bufNewSide > newSide:
                    newSide = bufNewSide
                    bufX = newX
                    bufY = newY
                if bufY + newSide >= self.n:
                    if newSide == 0:
                        return -1, -1, 0
                    return bufX, bufY, newSide
        if newSide == 0:
            return -1, -1, 0
        return bufX, bufY, newSide

    def paveBoolMap(self, squareBoolMap, x, y, n):      # Заполнение пустых клеток на карте
        for bufY in range(y, y+n):
            for bufX in range(x, x+n):
                squareBoolMap[bufY][bufX] = True
        return squareBoolMap

    def printBoolMap(self):     # Вывод карты заполнения
        for y in range(self.n):
            for x in range(self.n):
                print(int(self.squareBoolMap[y][x]), end=' ')
            print()

    def checkSquare(self, squareBoolMap, n):    # Можно ли вставить квадрат с заданной стороной
        for y in range(self.n):
            for x in range(self.n):
                if not squareBoolMap[y][x]:
                    side = self.searchSideNewSquare(squareBoolMap, x, y)
                    if side >= n:
                        return x, y
        return -1, -1


n = int(input())
square = Square(n)
square.pave()
square.print()
#square.printBoolMap()





























