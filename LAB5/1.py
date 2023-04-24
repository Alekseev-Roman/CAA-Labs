class BohrTop:
    def __init__(self, p, symb):
        self.numPattern = 0         # Номер шаблона
        self.nextTop = [-1] * 5     # Вершины в которые можно перейти
        self.flag = False           # Входит ли в исходную строку
        self.suffLink = -1          # Суфф. ссылка
        self.suffFLink = -1         # "Хорошая" суфф. ссылка
        self.autoMove = [-1] * 5    # Возможные переходы между состояниями
        self.par = p                # Номер предка
        self.symb = symb            # Номер символа в алфавите

    def __str__(self):
        return str(self.symb)


class AlgAC:
    def __init__(self, strT, n, setP):
        self.strT = strT    # Исходная строка
        self.n = n
        self.setP = setP    # Шаблоны
        self.result = []
        self.alphabet = ['A', 'C', 'G', 'T', 'N']   # Алфавит
        self.patterns = []
        self.bohr = []
        self.bohr.append(BohrTop(0, '$'))   # Инициализация бора

    def print(self):  # Вывод полей класса
        print(f"T: {self.strT}\nn = {self.n}\nP:")
        for el in self.setP:
            print(el)

    '''def printBohr(self):    # Вывод элементов в боре
        print("Бор:")
        for i in self.bohr:
            print(i)'''

    def printResult(self):  # Вывод результата
        #print("Текущий результат:")
        #print(self.setP)
        #print(self.patterns)
        self.result.sort()
        for el in self.result:
            print(el[0], el[1])

    def createBohr(self):
        for p in self.setP:
            self.addStrToBohr(p)

    def addStrToBohr(self, newStr):     # Добавление новой строки в бор
        num = 0     # Номер вершины бора
        for i in range(len(newStr)):
            numChar = self.alphabet.index(newStr[i])    # Номер символа в алфавите
            if self.bohr[num].nextTop[numChar] == -1:   # Ребра нет
                self.bohr.append(BohrTop(num, numChar))
                self.bohr[num].nextTop[numChar] = len(self.bohr) - 1
            num = self.bohr[num].nextTop[numChar]
        self.bohr[num].flag = True
        self.patterns.append(newStr)
        self.bohr[num].numPattern = len(self.patterns) - 1

    def checkStrInBohr(self, s):       # Проверка на наличие строки в боре
        num = 0
        for i in range(len(s)):
            numChar = self.alphabet.index(s[i])     # Номер символа в алфавите
            if self.bohr[num].nextTop[numChar] == -1:   # Ребра нет
                return False
            num = self.bohr[num].nextTop[numChar]
        return True

    def getAutoMove(self, v, ch):   # Переход между состояниями автомата
        if self.bohr[v].autoMove[ch] == -1:
            if self.bohr[v].nextTop[ch] != -1:
                self.bohr[v].autoMove[ch] = self.bohr[v].nextTop[ch]
            else:
                if v == 0:
                    self.bohr[v].autoMove[ch] = 0
                else:
                    self.bohr[v].autoMove[ch] = self.getAutoMove(self.getSuffLink(v), ch)
        return self.bohr[v].autoMove[ch]

    def getSuffLink(self, v):   # Получение суффиксной ссылки для v вершины
        if self.bohr[v].suffLink == -1:     # Ещё не нашли суфф. ссылку
            if v == 0 or self.bohr[v].par == 0:     # V или предок V - корень
                self.bohr[v].suffLink = 0
            else:
                self.bohr[v].suffLink = self.getAutoMove(self.getSuffLink(self.bohr[v].par), self.bohr[v].symb)
        return self.bohr[v].suffLink

    def getSuffFLink(self, v):  # Получение "хорошей" суфф. ссылки
        if self.bohr[v].suffFLink == -1:     # Ещё не нашли суфф. ссылку
            u = self.getSuffLink(v)
            if u == 0:     # V - корень, или U указывает на корень
                self.bohr[v].suffFLink = 0
            else:
                if self.bohr[u].flag:
                    self.bohr[v].suffFLink = u
                else:
                    self.bohr[v].suffFLink = self.getSuffFLink(u)
        return self.bohr[v].suffFLink

    def search(self, v, i):     # Поиск вхождений одного шаблона
        u = v
        while u != 0:
            if self.bohr[u].flag:
                self.result.append([i - len(self.patterns[self.bohr[u].numPattern]) + 1, self.bohr[u].numPattern + 1])
                #self.result.append([i - len(self.patterns[self.bohr[u].numPattern]) + 1, self.patterns[self.bohr[u].numPattern]])
            u = self.getSuffFLink(u)

    def searchAll(self):    # Поиск всех входжений всех шаблонов
        u = 0
        for i in range(len(self.strT)):
            u = self.getAutoMove(u, self.alphabet.index(self.strT[i]))
            self.search(u, i+1)



if __name__ == '__main__':
    strT = input()
    n = int(input())
    setP = []
    for _ in range(n):
        setP.append(input())
    '''strT = 'AAAAAAAAAA'
    n = 5
    setP = ['A', 'AAA', 'AA', 'AAAA', 'AAAAA', 'AAAAAA', 'AAAAAAA']'''

    alg = AlgAC(strT, n, setP)
    alg.createBohr()
    alg.searchAll()
    alg.printResult()
