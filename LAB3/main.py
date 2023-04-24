class Graf:     # Граф
    def __init__(self, start, finish, edges, interConc):
        self.start = start              # Исток
        self.finish = finish            # Сток
        self.result = []                # Результаты
        self.fronts = [{self.start: 0}] # Текущий набор фронтов для поиска в ширину
        self.graf = {}                  # Граф
        self.grafPar = {}               # Словарь вида: вершина: родитель, пропуск. способность.
        self.interConc = interConc      # Промежуточные выводы
        self.createGraf(edges)          # Создание графа

    def createGraf(self, edges):    # Создание графа
        if self.interConc:
            print("Создание графа:")
        for edge in edges:  # Перебор всех ребер
            if self.interConc:
                print(f"\tДобавление в граф ребра \"{edge[0]}\" \"{edge[1]}\" {edge[2]}")

            fV = edge[0]    # Вершина, откуда исходит ребро
            sV = edge[1]    # Вершина, в которую входит ребро

            if self.graf.get(fV):   # Если родительская вершина уже есть в графе
                if self.interConc:
                    print(f"\t\tВершина \"{fV}\" уже есть в графе. Добавляем новое исходящее из неё ребро")
                self.graf[fV][sV] = [int(edge[2]), int(edge[2]), True]
            else:   # Если родительской вершины ещё нет в графе
                if self.interConc:
                    print(f"\t\tВершины \"{fV}\" нет в графе, добаляем её. Добавляем исходящее из неё ребро")
                self.graf[fV] = {sV: [int(edge[2]), int(edge[2]), True]}

            if self.graf.get(sV):   # Если дочерняя вершина есть в графе
                if self.interConc:
                    print(f"\t\tВершина \"{sV}\" уже есть в графе. Добавляем новое входящее в неё ребро")
                if not self.graf[sV].get(fV): # Если ребра до родительской вершины ещё нет
                    self.graf[sV][fV] = [0, 0, False]
            else:   # Если дочерней вершины ещё нет в графе
                if self.interConc:
                    print(f"\t\tВершины \"{sV}\" нет в графе, добаляем её. Добавляем входящее в неё ребро")
                self.graf[sV] = {fV: [0, 0, False]}
            if self.interConc:
                print()

    def algFF(self):    # Алгоритм Форда-Фалкерсона
        if self.interConc:
            print("Запуск алгоритма Фодра-Фалкерсона:")

        while True:     # Повторяем шаги, пока не закончатся пути
            self.grafPar = {self.start: [None, 0]}

            self.breadthFirstSearch()   # Поиск в ширину

            self.fronts = [{self.start: 0}]

            if self.reduceBandwidth():  # Уменьшение пропускных способностей
                break

    def breadthFirstSearch(self):   # Поиск в ширину
        if self.interConc:
            print("\tЗапуск поиска в ширину:")
        for front in self.fronts:   # Проходим по всем фронтам
            if self.interConc:
                print(f"\t\tТекущий фронт: ", end='')
                for f in front:
                    print(f"{f} ", end='')
                print()
            for ver in front:       # Проходи по вершинам текущего фронта
                if self.interConc:
                    print(f"\t\tОбрабатываем вершину \"{ver}\":")
                for newVer in self.graf[ver]:   # Проходим по дочерним вершинам текущей вершины
                    if self.interConc:
                        print(f"\t\t\tПотомок \"{newVer}\":")
                    ed = self.grafPar.get(newVer)   # Проверка, попадали ли ранее в дочернюю вершину

                    if front == self.fronts[-1]:    # СОздание нового фронта по необходимости
                        self.fronts.append({})

                    if ed:  # Если в дочернюю вершину уже есть путь
                        if self.interConc:
                            print(f"\t\t\t\tУже есть путь")
                        i = self.fronts[-1].get(newVer)     # Лежит ли дочерняя вершина в текущем фронте

                        # Если дочерняя вершина в текущем фронте, старая пропускная способность меньше новой и
                        # до дочерней вершины можно пройти по ребру
                        if i and self.fronts[-1][newVer] < self.graf[ver][newVer][0] and self.graf[ver][newVer][0] > 0:
                            if self.interConc:
                                print(f"\t\t\t\tЗаменяем путь на новый, т.к. пропуск. способность нового больше: "
                                      f"{self.graf[ver][newVer][0]}")
                            self.grafPar[newVer] = [ver, self.graf[ver][newVer][0]] # Заменяем родителя на нового
                            self.fronts[-1][newVer] = self.graf[ver][newVer][0]     # Заменяем пропуск. спос. на новую

                    elif self.graf[ver][newVer][0] > 0: # Если в дочернюю вершину ещё не заходили
                        if self.interConc:
                            print(f"\t\t\t\tПути ещё нет")
                            print(f"\t\t\t\tДобавляем путь с пропуск. способностью: {self.graf[ver][newVer][0]}")
                        self.fronts[-1][newVer] = self.graf[ver][newVer][0]     # Добавляем дочернюю вершину в фронт
                        self.grafPar[newVer] = [ver, self.graf[ver][newVer][0]] # Добавляем родителя
                if self.interConc:
                    print()

    def reduceBandwidth(self):  # Уменьшение пропускных способностей
        if self.interConc:
            print(f"\n\tЗапуск уменьшения пропуск. способности:")
        ver = self.grafPar.get(self.finish) # В качестве начальной вершины - сток

        if ver == None:     # Если из стока никуда нельзя попасть, значит путей до стока нет
            if self.interConc:
                print(f"\t\tПути из истока до стока нет\n")
            self.createResult()
            return True

        minBW = -1  # Минимальный вес в пути

        ver = [self.finish, -1]

        while True:     # Проходим по вершинам, пока не дойдем до истока
            if self.interConc and ver[0] != None and self.grafPar[ver[0]][0] != None:
                print(f"\t\tПроходим по ребру \"{ver[0]}\" \"{self.grafPar[ver[0]][0]}\" {ver[1]}")
            # Если минимальная пропуск. способность большей текущей
            if (minBW > ver[1] or minBW == -1) and ver[0] != None:
                if self.interConc:
                    print(f"\t\tТ.к. текущая мин. пропуск. способность {minBW} больше чем у ребра {ver[1]}, заменяем её")
                minBW = ver[1]

            ver = self.grafPar.get(ver[0])
            if ver == None: # Если дошли до истока
                break
        if self.interConc:
            print(f"\t\tМинимальная пропуск. способность пути: {minBW}")

        sV = self.finish    # Вершина, в которую входит ребро
        fV = self.grafPar[self.finish][0]   # Вершина, из которой исходит ребро
        while True:
            self.graf[fV][sV][0] -= minBW   # Уменьшаем пропуск. способность ребра
            self.graf[sV][fV][0] += minBW   # Увеличиваем пропуск. способность противополож. ребра
            sV = fV
            fV = self.grafPar[fV][0]
            if sV == self.start or fV == None:  # Если достигли истока
                break
        if self.interConc:
            print()

        if self.interConc:
            print(f"\t\tГраф после изменения остаточной пропускной способности:")
            for ver in self.graf:  # Перебираем все вершины графа
                for newVer in self.graf[ver]:  # Перебираем все дочерние вершины
                    if self.graf[ver][newVer][2]:  # Если ребро в дочернюю вершину было в изначальном графе
                        if self.graf[ver][newVer][0] >= 0:
                            print(f"\t\t\t\"{ver}\" \"{newVer}\" {self.graf[ver][newVer][0]}")
                        else:
                            print(f"\t\t\t\"{ver}\" \"{newVer}\" 0")
            print()
        return False

    def createResult(self):     # Формирование результата
        if self.interConc:
            print(f"\tЗапуск формирования результата:")
        flow = 0    # Максимальный поток
        edges = []  # Ребра графа
        for ver in self.graf:   # Перебираем все вершины графа
            for newVer in self.graf[ver]:   # Перебираем все дочерние вершины
                if self.graf[ver][newVer][2]:   # Если ребро в дочернюю вершину было в изначальном графе
                    edges.append([ver, newVer, self.graf[ver][newVer][1] - self.graf[ver][newVer][0]])
                    if self.interConc:
                        print(f"\t\tДобавляем ребро \"{ver}\" \"{newVer}\" {self.graf[ver][newVer][1] - self.graf[ver][newVer][0]} в результат")
                    if edges[-1][2] < 0:
                        edges[-1][2] = 0
                    if newVer == self.finish:   # Если ребро входит в сток
                        if self.interConc:
                            print(f"\t\tУвеличиваем макс. поток на "
                                  f"{self.graf[ver][newVer][1] - self.graf[ver][newVer][0]}:")
                        flow += self.graf[ver][newVer][1] - self.graf[ver][newVer][0]

        self.result.append(flow)
        if self.interConc:
            print(f"\t\tТекущий результат:")
            print(f"\t\t\t{flow}")
            for i in range(len(edges)):
                print(f"\t\t\t{edges[i][0]} {edges[i][1]} {edges[i][2]}")
            print(f"\t\tСортируем результат\n")
        edges.sort()
        self.result += edges

    def printResult(self):  # Вывод результата
        if self.interConc:
            print("Результат:")
        for i in range(len(self.result)):
            if i == 0:
                print(self.result[i])
            else:
                print(f"{self.result[i][0]} {self.result[i][1]} {self.result[i][2]}")


if __name__ == "__main__":
    n = int(input())
    start = input()
    finish = input()

    edges = []
    for _ in range(n):
        edges.append(list(input().split()))

    graf = Graf(start, finish, edges, True)
    graf.algFF()
    graf.printResult()



