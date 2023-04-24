import queue

class GrafVertex:       # Вершина графа
    def __init__(self):
        self.symbol = None      # Символ вершины
        self.parent = None      # Индекс родителя, через которого пришли
        self.child = []         # Список индексов потомков, весов ребер к ним и флагов посещения

    def setSymbol(self, symbol):    # Установить символ вершины
        self.symbol = symbol

    def addPar(self, newPar):   # Добавить родителя
        self.parent = newPar

    def addChild(self, newChild):   # Добавить потомка
        self.child.append(newChild)

    def __str__(self):      # Вывод вершины
        string = f"Вершина: {self.symbol}\n Индексы родителей:\n"
        for i in self.parent:
            string += f"  {i}\n"
        string += " Индексы потомков:\n"
        for i in self.child:
            string += f"  {i}\n"
        return string


class Graf:
    def __init__(self, start, finish, interConc):
        self.numStart = ord(start) - ord('a')                 # Индекс начальной вершины
        self.numFinish = ord(finish) - ord('a')               # Индекс конечной вершины
        self.graf = [GrafVertex() for _ in range(26)]   # Список вершин
        self.result = ""                                # Результат

        self.interConc = interConc                      # Промежуточные выводы

    def printResult(self):      # Вывод результатов
        if self.interConc:
            print("Результат:")
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
                              f"{chr(numVer + ord('a'))}──{bufWeight}─>{chr(bufIndChild + ord('a') + 1)}")
                    break

            for indChild in range(len(self.graf[numVer].child)):    # Нахождение ребра с наименьшим весом
                if self.graf[numVer].child[indChild][1] < bufWeight and self.graf[numVer].child[indChild][2]:
                    bufWeight = self.graf[numVer].child[indChild][1]
                    bufIndChild = indChild
                    if self.interConc:
                        print(f"\t\tНовое ребро с минимальным весмо, по которому ещё не проходили: "
                              f"{chr(numVer + ord('a'))}──{bufWeight}─>{chr(bufIndChild + ord('a') + 1)}")

            if bufIndChild >= 0:    # Если нашли ребро
                if self.interConc:
                    print(f"\t\tПереходим к новой вершине по ребру: "
                          f"{chr(numVer + ord('a'))}──{bufWeight}─>{chr(bufIndChild + ord('a') + 1)}")
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

        queueVer = queue.PriorityQueue(0)
        passedVer = []
        g = [-1] * 26
        f = [-1] * 26

        g[numVer] = 0
        f[numVer] = float(g[numVer] + abs(ord(self.graf[numVer].symbol) - ord(self.graf[self.numFinish].symbol)))
        queueVer.put((f[numVer], numVer))


        while queueVer.qsize() > 0:
            current = queueVer.get()
            #print(f"cur: {current}, queue: {queueVer}")

            if current == self.numFinish:
                self.createResult()
                return

            #queueVer.get(current)
            passedVer.append(current)

            for child in self.graf[current[1]].child:
                tentativeScore = g[current[1]] + child[1]
                if child[0] not in passedVer or tentativeScore < g[child[0]]:
                    self.graf[child[0]].parent = current[1]
                    g[child[0]] = tentativeScore
                    f[child[0]] = g[child[0]] + abs(ord(self.graf[child[0]].symbol) -
                                                    ord(self.graf[self.numFinish].symbol))
                    if (f[child[0]], child[0]) not in queueVer:
                        queueVer.put((f[child[0]], child[0]))

    def getVer(self, queueVer, f):
        bufI = -1
        bufF = -1
        for i in queueVer:
            if (f[i] <= bufF or bufF < 0) and f[i] >= 0:
                bufI = i
                bufF = f[i]
        return bufI

    def createResult(self):
        numVer = self.numFinish
        self.result += str(chr(numVer + ord('a')))
        while True:
            #print(self.result)
            numVer = self.graf[numVer].parent
            if numVer != None:
                self.result += chr(numVer + ord('a'))
            else:
                break
        self.result = self.result[::-1]


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

    graf = Graf(start, finish, interConc)
    graf.createGraf(edges)
    graf.greedyAlg()
    graf.printResult()


def secondTask(interConc):
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

    graf = Graf(start, finish, interConc)
    graf.createGraf(edges)
    graf.algAStar()
    graf.printResult()


if __name__ == "__main__":
    #firstTask(True)
    secondTask(False)