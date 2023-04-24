class Graf:
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        self.result = []
        self.fronts = [{self.start: 0}]
        self.graf = {}
        self.grafPar = {}
        self.createGraf()

    def createGraf(self):
        for edge in edges:
            fV = str(edge[0])
            sV = str(edge[1])

            ed = self.graf.get(fV)
            if ed:
                self.graf[fV][sV] = [int(edge[2]), int(edge[2])]
            else:
                self.graf[fV] = {sV: [int(edge[2]), int(edge[2])]}

            ed = self.graf.get(sV)
            if ed == None:
                self.graf[sV] = []

    def algFF(self):
        while True:
            self.grafPar = {'a': [None, 0]}

            self.breadthFirstSearch()

            self.fronts = [{self.start: 0}]

            if self.reduceBandwidth():
                break

    def breadthFirstSearch(self):
        finalVer = True
        for front in self.fronts:
            if finalVer:
                firstVer = True
                for ver in front:
                    for newVer in self.graf[ver[0]]:
                        ed = self.grafPar.get(newVer)
                        if ed:
                            i = front.get(newVer)
                            if i and front[newVer] < self.graf[ver[0]][newVer][0] and self.graf[ver[0]][newVer][0] > 0:
                                if newVer == self.finish:
                                    finalVer = False
                                self.grafPar[ed[0]] = [ver[0], self.graf[ver[0]][newVer][0]]
                                self.fronts.append({newVer: self.graf[ver[0]][newVer][0]})
                        elif self.graf[ver[0]][newVer][0] > 0:
                            if newVer == self.finish:
                                finalVer = False
                            if firstVer:
                                firstVer = False
                                self.fronts.append({newVer: self.graf[ver[0]][newVer][0]})
                            else:
                                self.fronts[-1][newVer] = self.graf[ver[0]][newVer][0]
                            self.grafPar[newVer] = [ver[0], self.graf[ver[0]][newVer][0]]

    def reduceBandwidth(self):
        ver = self.grafPar.get(self.finish)

        if ver == None:
            self.createResult()
            return True

        minBW = -1
        k = 0
        while k < n:
            if (minBW > ver[1] or minBW == -1) and ver[0] != None:
                minBW = ver[1]

            ver = self.grafPar.get(ver[0])
            if ver == None:
                break
            k += 1

        fV = [self.finish, 0]
        sV = self.grafPar[self.finish]
        k = 0
        while k < n:
            self.graf[sV[0]][fV[0]][0] -= minBW
            fV = sV
            sV = self.grafPar.get(sV[0])

            if fV[0] == 'a' or sV == None:
                break
            if self.graf[sV[0]].get(fV[0]) == None:
                break
            k += 1

        return False

    def createResult(self):
        flow = 0
        edges = []
        vers = self.graf.keys()
        for ver in vers:
            for newVer in self.graf[ver]:
                edges.append([ver, newVer, self.graf[ver][newVer][1] - self.graf[ver][newVer][0]])
                if newVer == self.finish:
                    flow += self.graf[ver][newVer][1] - self.graf[ver][newVer][0]

        self.result.append(flow)
        edges.sort()
        self.result += edges

    def printResult(self):
        #print(self.graf)
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
    graf = Graf(start, finish)
    graf.algFF()
    graf.printResult()



