class BohrTop:      # Вершина бора
    def __init__(self, p, symb):
        self.pattern = []           # Номера шаблонов, которые кончаются этой вершиной
        self.nextTop = [-1] * 5     # Вершины в которые можно перейти
        self.flag = False           # Конец шаблона
        self.suffLink = -1          # Суфф. ссылка
        self.suffFLink = -1         # "Хорошая" суфф. ссылка
        self.autoMove = [-1] * 5    # Возможные переходы между состояниями
        self.par = p                # Номер предка
        self.symb = symb            # Номер символа в алфавите

    def __str__(self):
        return str(self.symb)


class AlgAC:
    def __init__(self, strT, setP, interConc):
        self.strT = strT  # Исходная строка
        self.setP = setP  # Шаблоны
        self.result = []    # Результаты
        self.patterns = []  # Шаблоны
        self.bohr = []      # Бор
        self.alphabet = ['A', 'C', 'G', 'T', 'N']   # Алфавит
        self.bohr.append(BohrTop(0, '$'))   # Инициализация бора
        self.isJocker = False   # Флаг задания
        self.interConc = interConc  # Флаг промежуточных выводов

        # Для джокера
        self.numP = []    # Индексы начал шаблонов
        self.c = [0] * len(strT)    # Список количеств вхождений по i индексу
        self.resultJocker = []  # Результаты 2 задания
        self.lenPat = 0     # Длина шаблона

    def printBohr(self):    # Вывод бора
        print("└──$──◯")    # Корневая вершина
        for j in range(len(self.alphabet)): # Проход по детям корневой вершины
            isLast = True
            for e in range(j+1, len(self.alphabet)):    # Проверка на то, является ли ребенок последним
                if self.bohr[0].nextTop[e] != -1:
                    isLast = False
            if self.bohr[0].nextTop[j] != -1:   # Если ребенок есть
                self.printTopBohr(self.bohr[0].nextTop[j], "      ", isLast)
        print()

    def printTopBohr(self, top, pref, isLast):  # Вывод вершин бора
        print(pref, end="")
        print(f"└──{self.alphabet[int(self.bohr[top].symb)]}──", end='')    # Вывод ребра с символом
        if self.bohr[top].flag:
            print("⚫")
        else:
            print("◯")

        if self.bohr[top].nextTop.count(-1) == len(self.bohr[top].nextTop):     # Если вершина - лист
            return

        if isLast:  # Увеличение префикса
            pref += "      "
        else:
            pref += "│     "

        for j in range(len(self.alphabet)):  # Перебор детей вершины
            isLast = True
            for e in range(j+1, len(self.alphabet)):    # Проверка на то, является ли ребенок последним
                if self.bohr[top].nextTop[e] != -1:
                    isLast = False
            if self.bohr[top].nextTop[j] != -1: # Если ребенок есть
                self.printTopBohr(self.bohr[top].nextTop[j], pref, isLast)


    def printResult(self):  # Вывод результата АК
        if self.interConc:
            print("Результат:")
        self.result.sort()
        for el in self.result:
            print(el[0], el[1])

    def printResJocker(self):   # Вывод результата АК с джокерами
        if self.interConc:
            print("Результат:")
        self.resultJocker.sort()
        for el in self.resultJocker:
            print(el)

    def printInd(self):     # Вывод индивидуализации
        print(f"\nКол-во вершин в автомате: {len(self.bohr)}")
        intersec = []
        '''for i in range(len(self.result)):
            for e in range(i, len(self.result)):
                if self.result[e] != self.result[i]:
                    if self.result[i][0] + len(self.setP[self.result[i][1]-1]) > self.result[e][0]:
                        intersec.append([self.setP[self.result[i][1]-1], self.setP[self.result[e][1]-1],
                                         self.result[i][0]-1, self.result[e][0]-1])
        if len(intersec):
            print("Образцы, имеющие пересечения с другими образцами в строке поиска:")
            for el in intersec:
                print(f"\tОбразцы {el[0]} и {el[1]} пересекаются символами под номерами:")
                diff = el[2] + len(el[0]) - el[3]
                if diff >= len(el[1]):
                    lenIntersec = len(el[1])
                else:
                    lenIntersec = diff
                for i in range(lenIntersec):
                    print("\t", el[3] + i + 1, f"- символ {self.strT[el[3] + i]}")
                print()
        else:
            print("Образцы не пересекаются между собой в строке поиска")'''

        for i in range(len(self.result)):
            for e in range(i, len(self.result)):
                if self.result[e] != self.result[i]:    # Если результаты различны
                    if self.result[i][0] + len(self.setP[self.result[i][1]-1]) > self.result[e][0]:
                            intersec.append(self.setP[self.result[i][1] - 1])
                            intersec.append(self.setP[self.result[e][1] - 1])
                            intersec.append("")
        if len(intersec):
            print("Образцы, имеющие пересечения с другими образцами в строке поиска:")
            for el in intersec:
                print(el)
        else:
            print("Образцы не пересекаются между собой в строке поиска")

    def createBohr(self):   # Создание бора
        if self.interConc:
            print("Создание бора:")
        for p in self.setP:     # Перебор всех шаблонов в списке
            if self.interConc:
                print(f"Добавим в бор шаблон {p}:")
                print("Бор до добавления:")
                self.printBohr()
            self.addStrToBohr(p)    # Добавление шаблона
            if self.interConc:
                print(f"Бор в результате добавления шаблона {p}:")
                self.printBohr()

    def setNumLen(self, numP, lenPat):  # Сохранение доп. данных
        self.numP = numP
        self.lenPat = lenPat
        self.isJocker = True

    def addStrToBohr(self, newStr):  # Добавление новой строки в бор
        num = 0  # Номер вершины бора
        for i in range(len(newStr)):
            numChar = self.alphabet.index(newStr[i])  # Номер символа в алфавите
            if self.bohr[num].nextTop[numChar] == -1:  # Ребра нет
                self.bohr.append(BohrTop(num, numChar))
                self.bohr[num].nextTop[numChar] = len(self.bohr) - 1
                if self.interConc:
                    print(f"Символа {newStr[i]} под индексом {i+1} нет в боре, добавляем новую вершину. Бор после "
                          f"добавления:")
                    self.printBohr()
            elif self.interConc:
                print(f"Символ {newStr[i]} под индексом {i+1} уже есть в боре, переходим к след. символу шаблона")
            num = self.bohr[num].nextTop[numChar]
        self.bohr[num].flag = True  # Вершина является последней для шаблона
        self.patterns.append(newStr)
        self.bohr[num].pattern.append(len(self.patterns) - 1)  # Сохранения номера шаблона, заканчиающегося вершиной

    def getAutoMove(self, v, ch):   # Получение функции перехода между состояниями
        if self.bohr[v].autoMove[ch] == -1:     # Если функции перехода ещё нет
            if self.bohr[v].nextTop[ch] != -1:  # Если есть дети
                self.bohr[v].autoMove[ch] = self.bohr[v].nextTop[ch]
            else:
                if v == 0:   # Если вершина - корень
                    self.bohr[v].autoMove[ch] = 0
                else:
                    self.bohr[v].autoMove[ch] = self.getAutoMove(self.getSuffLink(v), ch)
        return self.bohr[v].autoMove[ch]

    def getSuffLink(self, v):  # Получение суффиксной ссылки для v вершины
        if self.bohr[v].suffLink == -1:  # Ещё не нашли суфф. ссылку
            if self.interConc:
                print(f"Для вершины {v} ещё нет суфф. ссылки")
            if v == 0 or self.bohr[v].par == 0:  # V или предок V - корень
                if self.interConc:
                    print(f"Вершина {v} является корнем или её предок корень, суфф. ссылка устанавливается на корень")
                self.bohr[v].suffLink = 0
            else:
                self.bohr[v].suffLink = self.getAutoMove(self.getSuffLink(self.bohr[v].par), self.bohr[v].symb)
                if self.interConc:
                    print(f"Суфф. ссылка для вершины {v} устанавливается на вершину {self.bohr[v].suffLink}")
        elif self.interConc:
            print(f"Суфф. ссылка для вершины {v} уже была установлена - {self.bohr[v].suffLink}")
        if self.interConc:
            print()
        return self.bohr[v].suffLink

    def getSuffFLink(self, v):  # Получение "хорошей" суфф. ссылки
        if self.bohr[v].suffFLink == -1:  # Ещё не нашли суфф. ссылку
            if self.interConc:
                print(f"Для вершины {v} ещё нет хорошей суфф. ссылки")
            u = self.getSuffLink(v)
            if u == 0:  # V - корень, или U указывает на корень
                if self.interConc:
                    print(f"Вершина {v} является корнем или её предок корень, хорошая суфф. ссылка устанавливается "
                          f"на корень")
                self.bohr[v].suffFLink = 0
            else:
                if self.bohr[u].flag:
                    self.bohr[v].suffFLink = u
                else:
                    self.bohr[v].suffFLink = self.getSuffFLink(u)
                    if self.interConc:
                        print(f"Хорошая суфф. ссылка для вершины {v} устанавливается на вершину "
                              f"{self.bohr[v].suffFLink}")
        elif self.interConc:
            print(f"Хорошая суфф. ссылка для вершины {v} уже была установлена - {self.bohr[v].suffFLink}")
        if self.interConc:
            print()
        return self.bohr[v].suffFLink

    def search(self, u, i):     # Поиск вхождений шаблона по индексу
        if self.interConc:
            print(f"Поиск для вершины {u} и символа под индексом {i}")
        while u != 0:
            if self.bohr[u].flag:   # Если в вершине заканчивается шаблон
                if self.interConc:
                    print(f"Вершина {u} является концом для одного из шаблонов в боре")
                numberPat = self.bohr[u].pattern
                for pat in numberPat:
                    lenPat = len(self.patterns[pat])
                    if self.interConc:
                        print(f"Сохранение в результат шаблона {self.setP[pat]} и индекса начала его"
                              f"вхождения {i - lenPat + 1}")
                    self.result.append([i - lenPat + 1, pat + 1])
                    # Для джокера
                    if self.isJocker and i - self.numP[pat] >= 0:
                        if self.interConc:
                            print(f"Увеличение кол-ва шаблонов без джокеров, начинающихся с индекса "
                                  f"{i - lenPat - self.numP[pat]}")
                        self.c[i - self.numP[pat] - lenPat] += 1
            u = self.getSuffFLink(u)
            if self.interConc:
                print(f"Переходим по \"хорошей\" суффиксной ссылке к вершине {u}")
            if self.interConc:
                print(f"Переход по суффиксной ссылке к новой вершине - {u}")
        if self.interConc:
            print("По суффиксной ссылке пришли к корню, дальнешие переходы не имеют смысла\n")

    def searchAll(self):    # Поиск вхождений всех шаблонов
        if self.interConc:
            print("Поиск вхождений шаблонов в строку поиска:")
        u = 0
        for i in range(len(self.strT)):     # Проход по всем символам строки
            if self.interConc:
                print(f"Для вершины {u} и символа {self.strT[i]} переходим к вершине", end=" ")
            u = self.getAutoMove(u, self.alphabet.index(self.strT[i]))
            if self.interConc:
                print(f"{u}")
            self.search(u, i+1)
        if self.interConc:
            print()

    def searchJocker(self):     # Поиск с джокерами
        if self.interConc:
            print("Поиск вхождений шаблона с джокерами")
        self.searchAll()
        for i in range(len(self.c)):
            if self.c[i] == len(self.setP) and i + self.lenPat <= len(self.strT):
                if self.interConc:
                    print(f"Сохранение индекса начала вхождения шаблона - {i + 1}")
                self.resultJocker.append(i + 1)
        if self.interConc:
            print()


def cutPattern(pattern, jocker):  # Нарезка шаблона на подстроки без джокеров
    setP = []
    numP = []
    buf = ''
    flag = False
    e = 0
    for i in range(len(pattern)):   # Проход по символам шаблона
        if pattern[i] == jocker:    # Если символ - джокер
            if flag:
                setP.append(buf)
                buf = ''
                numP.append(e)
            flag = False
        else:
            if not flag:
                e = i
            buf += pattern[i]
            flag = True
    if buf != '':
        setP.append(buf)
        numP.append(e)
    return setP, numP


def first(interConc):    # Первая часть
    strT = input()
    n = int(input())
    setP = []
    for _ in range(n):  # Считывание шаблонов
        setP.append(input())
    alg = AlgAC(strT, setP, interConc)
    alg.createBohr()
    alg.searchAll()
    alg.printResult()
    alg.printInd()


def second(interConc):   # Вторая часть
    strT = input()
    pattern = input()
    jocker = input()

    setP, numP = cutPattern(pattern, jocker)
    if interConc:
        print("Шаблон был разделен на подстроки без джокеров, результат:")
        for i in range(len(setP)):
            print(numP[i], setP[i])
        print()
    lenPat = len(pattern)

    alg = AlgAC(strT, setP, interConc)
    alg.setNumLen(numP, lenPat)
    alg.createBohr()
    alg.searchJocker()
    alg.printResJocker()
    #alg.printInd()


if __name__ == '__main__':
    first(True)
    #second(True)
