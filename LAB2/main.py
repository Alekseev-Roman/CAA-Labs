class GrafVertex:       # Вершина графа
    def __init__(self):
        self.symbol = None      # Символ вершины
        self.parent = None      # Индекс родителя, через которого пришли
        self.child = []         # Список индексов потомков, весов ребер к ним и флагов посещения
        self.heur = None        # Эвристическая функция

    def setSymbol(self, symbol):    # Установить символ вершины
        self.symbol = symbol

    def addPar(self, newPar):   # Добавить родителя
        self.parent = newPar

    def addChild(self, newChild):   # Добавить потомка
        self.child.append(newChild)

    def __str__(self):      # Вывод вершины
        string = f"Вершина: {self.symbol}\n Индексы родителей:\n"
        string += f"Родитель: {self.parent}\n"
        string += " Индексы потомков:\n"
        for i in self.child:
            string += f"  {i}\n"
        return string


class Graf:
    def __init__(self, start, finish, interConc, individual):
        self.numStart = ord(start) - ord('a')                 # Индекс начальной вершины
        self.numFinish = ord(finish) - ord('a')               # Индекс конечной вершины
        self.graf = [GrafVertex() for _ in range(26)]   # Список вершин
        self.result = ""                                # Результат

        self.interConc = interConc                      # Промежуточные выводы
        self.individual = individual                    # Индивидуализация

    def printResult(self):      # Вывод результатов
        if self.interConc:
            print("\n\033[34mРезультат:\033[0m")
        print(self.result)

    def createGraf(self, edgesBuf):     # Создание графа из ребер
        if self.interConc:
            print("\033[33mСоздание графа из ребер:\033[0m")
        for edge in edgesBuf:
            numSVer = ord(edge[0]) - ord('a')     # Индекс вершины, где 97 - номер символа 'а' в ASCII
            numFVer = ord(edge[1]) - ord('a')
            weight = float(edge[2])
            if self.interConc:
                print(f"\tДобавление в граф ребра {edge[0]}──{weight}─>{edge[1]}")
            if not self.graf[numSVer].symbol:   # Если начальной вершины ребра ещё нет
                if self.interConc:
                    print(f"\tВершины \"{edge[0]}\" ещё нет в графе. Добавляем её.")
                self.graf[numSVer].setSymbol(edge[0])
            if not self.graf[numFVer].symbol:   # Если конечной вершины ребра ещё нет
                if self.interConc:
                    print(f"\tВершины \"{edge[1]}\" ещё нет в графе. Добавляем её.")
                self.graf[numFVer].setSymbol(edge[1])
            self.graf[numSVer].addChild([numFVer, weight, True])
            if self.interConc:
                print("")
        if self.interConc:
            print(f"\tГраф построен.\n")

    def greedyAlg(self):    # Жадный алгоритм
        if self.interConc:
            print("\033[32mЗапуск жадного алгоритма:\033[0m")
        numVer = self.numStart  # Номер начальной вершины
        self.result += chr(numVer + ord('a'))     # Добавляем начальную вершину в результат
        while True:
            if numVer == self.numFinish:    # Если текущая вершина - финальная, то путь найден
                if self.interConc:
                    print("\tДошли до конечной вершины, работа алгоритма окончена.\n")
                break

            bufWeight = 0
            bufIndChild = -1

            if self.interConc:
                print("\tВыбираем ребро с минимальным весом:")

            for indChild in range(len(self.graf[numVer].child)):    # Выбор первого ребра для перехода
                if self.graf[numVer].child[indChild][2]:            # Если по ребру ещё не проходили
                    bufWeight = self.graf[numVer].child[indChild][1]
                    bufIndChild = indChild
                    if self.interConc:
                        print(f"\t\tТекущее ребро с минимальным весом, по которому ещё не проходили: "
                              f"{chr(numVer + ord('a'))}──{bufWeight}─>{chr(bufIndChild + ord('a') + 1)}") # Тут конечная вершина неверна
                    break

            for indChild in range(len(self.graf[numVer].child)):    # Нахождение ребра с наименьшим весом
                if self.graf[numVer].child[indChild][1] < bufWeight and self.graf[numVer].child[indChild][2]:
                    bufWeight = self.graf[numVer].child[indChild][1]
                    bufIndChild = indChild
                    if self.interConc:
                        print(f"\t\tНовое ребро с минимальным весом, по которому ещё не проходили: "
                              f"{chr(numVer + ord('a'))}──{bufWeight}─>{self.graf[bufIndChild].symbol}") # Тут конечная вершина неверна

            if bufIndChild >= 0:    # Если нашли ребро
                if self.interConc:
                    print(f"\t\tПереходим к новой вершине по ребру: "
                          f"{chr(numVer + ord('a'))}──{bufWeight}─>{self.graf[bufIndChild].symbol}") # Тут конечная вершина неверна
                self.graf[numVer].child[bufIndChild][2] = False
                numVer = self.graf[numVer].child[bufIndChild][0]
                self.result += chr(numVer + 97)
            else:                   # Если из текущей веришны нет исходящих ребер
                if self.interConc:
                    print(f"\t\tИз вершины \"{chr(numVer + ord('a'))}\" нет исходящих ребер, по которым ещё не "
                          f"проходили. ", end='')
                self.result = self.result[:-1]  # Убираем текущую вершину из ответа
                if len(self.result) > 1:        # Получаем номер предыдущей вершины
                    numVer = ord(self.result[-1]) - ord('a')
                else:
                    numVer = self.numStart
                if self.interConc:
                    print(f"Переходим к предыдущей вершине \"{chr(numVer + ord('a'))}\"")
            if self.interConc:
                print('')

    def algAStar(self):     # Алгоритм А*
        if self.interConc:
            print("\033[32mЗапуск алгоритма А*:\033[0m")
        numVer = self.numStart

        queueVer = []
        passedVer = []
        g = [-1] * 26
        f = [-1] * 26

        queueVer.append(numVer)     # Добавляем в очередь начальную вершину
        g[numVer] = 0               # Т.к. расстояние из начальной вершины в саму себя без прохода по другим вершинам 0
        if self.individual:
            f[numVer] = float(g[numVer] + self.graf[numVer].heur)
        else:
            f[numVer] = float(g[numVer] + abs(ord(self.graf[numVer].symbol) - ord(self.graf[self.numFinish].symbol)))

        if self.interConc:
            print(f"\tДобавляем в очередь начальную вершину \"{self.graf[numVer].symbol}\" с приоритетом {f[numVer]}")
            print(f"\tОчередь с приоритетом: ", end='')
            for e in queueVer:
                print(f"{self.graf[e].symbol} [{f[e]}]\n")

        while len(queueVer):    # Пока не будут обработаны все вершины графа
            current = self.getVer(queueVer, f)
            if self.interConc:
                print(f"\tТекущая очередь: ", end='')
                for e in queueVer:
                    print(f"{self.graf[e].symbol} [{f[e]}]  ", end='')
                print(f"\n\tИзвлекаем из очереди вершину \"{self.graf[current].symbol}\"")

            if current == self.numFinish:   # Если достигнута конечная вершина
                if self.interConc:
                    print(f"\tИзвлеченная вершина является конечной вершиной\n")
                self.createResult()
                return

            queueVer.remove(current)    # Удаляем из очереди, т.к. обработали
            passedVer.append(current)   # Добавляем в список обработанных вершин

            if self.interConc:
                print(f"\tПроверяем всех детей выбранной вершины:")

            for child in self.graf[current].child:  # Перебираем всех детей текущей вершины
                tentativeScore = g[current] + child[1]  # Путь до ребенка от начальной вершины
                if self.interConc:
                    print(f"\t\tДля вершины \"{self.graf[child[0]].symbol}\":\n\t\t\tэвристическая функция - ", end='')
                    if self.individual:
                        print(self.graf[child[0]].heur)
                    else:
                        print(f"{abs(ord(self.graf[child[0]].symbol) - ord(self.graf[self.numFinish].symbol))}")
                    print(f"\t\t\tпуть от начальной вершины - {tentativeScore}")
                # Если ребенка ещё не обрабатывали или новый путь до него короче
                if child[0] not in passedVer or tentativeScore < g[child[0]]:
                    self.graf[child[0]].parent = current
                    g[child[0]] = tentativeScore
                    if self.individual:
                        f[child[0]] = g[child[0]] + self.graf[child[0]].heur
                    else:
                        f[child[0]] = g[child[0]] + abs(ord(self.graf[child[0]].symbol) -
                                                    ord(self.graf[self.numFinish].symbol))
                    if child[0] not in queueVer:    # Если ребенка ещё нет в очереди
                        if self.interConc:
                            print(f"\t\tДобавляем вершину \"{self.graf[child[0]].symbol}\" в очередь с приоритетом "
                                  f"{f[child[0]]}")
                        queueVer.append(child[0])
            self.result = ''
            if self.interConc:
                print("")

    def getVer(self, queueVer, f):  # Получение элемента из очереди с приоритетом
        bufI = -1
        bufF = -1
        for i in queueVer:  # Перебор элементов очереди
            if (f[i] <= bufF or bufF < 0) and f[i] >= 0:    # Найден меньший приоритет
                bufI = i
                bufF = f[i]
        return bufI

    def createResult(self):     # Создание результата при помощи прохода по графу в обратном направлении
        if self.interConc:
            print(f"\tСохранение пути при помощи прохода в обратном направлении:")

        numVer = self.numFinish
        self.result += str(chr(numVer + ord('a')))  # Добавляем конечную вершину

        if self.interConc:
            print(f"\t\tДобавляем в результат конечную вершину \"{self.graf[numVer].symbol}\"")
            print(f"\t\tТекущий результат: {self.result}\n")

        while True:     # Проходим по всем вершинам
            if self.interConc:
                bufNum = numVer

            numVer = self.graf[numVer].parent
            if numVer != None:  # Если текущая вершина не начальная
                self.result += chr(numVer + ord('a'))

                if self.interConc:
                    print(f"\t\tПри работе алгоритма в вершину \"{self.graf[bufNum].symbol}\" попали из вершины "
                          f"\"{self.graf[numVer].symbol}\"")
                    print(f"\t\tДобавим её в результат.\n\t\tТекущий результат: {self.result}\n")
            else:   # Если текущая вершина начальная
                if self.interConc:
                    print(f"\t\tПри работе алгоритма в вершину \"{self.graf[bufNum].symbol}\" попали из начальной "
                          f"вершины\n")
                break
        self.result = self.result[::-1]     # Переворачиваем результат

        if self.interConc:
            print("\t\tПеревернем результат")
            print(f"\t\tПолучим: {self.result}")


def firstTask(interConc):       # Первое задание
    start, finish = input().split()     # Считывание старта и финиша

    edges = []
    while True:     # Считывание ребер
        try:
            edge = input(' ')
            if edge == '' or edge == " ":   # Если ввод закончен
                break
        except (EOFError):  # Если ввод закончен
            break
        edges.append(list(edge.split()))

    graf = Graf(start, finish, interConc, False)
    graf.createGraf(edges)
    graf.greedyAlg()
    graf.printResult()


def secondTask(interConc):      # Второе задание
    start, finish = input().split()  # Считывание старта и финиша

    edges = []
    while True:  # Считывание ребер
        try:
            edge = input(' ')
            if edge == '' or edge == " ":   # Если ввод закончен
                break
        except (EOFError):  # Если ввод закончен
            break
        edges.append(list(edge.split()))

    graf = Graf(start, finish, interConc, False)
    graf.createGraf(edges)
    graf.algAStar()
    graf.printResult()


def individualTask(interConc):      # Второе задание с индивидуализацией
    start, finish = input().split()  # Считывание старта и финиша

    edges = []
    while True:  # Считывание ребер
        try:
            edge = input(' ')
            if edge == '' or edge == " ":  # Если ввод закончен
                break
        except (EOFError):  # Если ввод закончен
            break
        edges.append(list(edge.split()))

    graf = Graf(start, finish, interConc, True)
    graf.createGraf(edges)
    print("Введите значения эвристических функций:")
    for ver in graf.graf:
        if ver.symbol != None:
            print(f"{ver.symbol}: ", end='')
            ver.heur = int(input())
    print("")
    graf.algAStar()
    graf.printResult()


if __name__ == "__main__":
    firstTask(True)
    #secondTask(False)
    #individualTask(True)