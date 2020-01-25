class hero:
    def __init__(self, start, hp, end):
        self.start = start
        self.hp = hp
        self.end = end

def fieldToMatrix(len, width, field):
    newField = field.replace('\n', '')
    field = newField.replace(' ', '')
    field = str(field)
    countElm = len * width
    matrix = []
    for i in range(countElm):
        row = []
        for _ in range(countElm):
            row.append((0,0))
        matrix.append(row)
    for numberOfCell, cell in enumerate(field):
        if cell == '0':
            for i in [numberOfCell-1, numberOfCell+1, numberOfCell-width, numberOfCell+width]:
                try:
                    matrix[i][numberOfCell] = (1,0)
                except Exception:
                    continue
        elif cell != '#' and int(cell) > 0:
            for i in [numberOfCell - 1, numberOfCell + 1, numberOfCell - width, numberOfCell + width]:
                try:
                    matrix[i][numberOfCell] = (1,int(cell))
                except Exception:
                    continue
    return matrix


def pathWithOutMonsters(coordStart,coordEnd, matrix, lenght, width):
    size = len(matrix)
    vertex = [1] * size
    distance  = [10000] * size
    start = coordStart[0] * width + coordStart[1]
    distance[start] = 0
    while True:
        minindex = 10000
        min = 10000
        for i in range(size):
            if vertex[i] == 1 and distance[i] < min:
                min = distance[i]
                minindex = i
        if(minindex != 10000):
            for i in range(size):
                if matrix[minindex][i][0] > 0:
                    temp = min + 1
                    if temp < distance[i]: distance[i] = temp
            vertex[minindex] = 0
        if minindex >= 10000: break
    vertexPath = []
    end = coordEnd[0] * width + coordEnd[1]
    vertexPath.append(end)
    weight = distance[end]
    while end != start:
        for i in range(size):
            if matrix[end][i][0] != 0:
                temp = weight - matrix[end][i][0]
                if temp == distance[i]:
                    weight = temp
                    end = i
                    vertexPath.append(i)
    vertexPath.reverse()               
    return vertexPath


def pathWithMonsters(coordStart,coordEnd, matrix, lenght, width, hp):
    size = len(matrix)
    vertex = [1] * size
    start = coordStart[0] * width + coordStart[1]
    distance  = []
    for _ in range(size):
            distance.append((10000,10000))
    distance[start] = (0,0)
    while True:
        minindex = 10000
        min = 10000
        minHP = 10000
        for i in range(size):
            if vertex[i] == 1 and distance[i][0] < min:
                min, minHP = distance[i]
                minindex = i
        if(minindex != 10000):
            for i in range(size):
                if matrix[minindex][i][0] > 0:
                    temp = min + 1
                    tempHP = minHP + matrix[minindex][i][1]
                    if temp < distance[i][0] and hp > minHP: distance[i] = (temp, tempHP)
            vertex[minindex] = 0
        
        if minindex >= 10000: break
    print(distance)
    vertexPath = []
    end = coordEnd[0] * width + coordEnd[1]
    vertexPath.append(end)
    weight = distance[end][0]
    if distance[end] == (10000, 10000):
        return 'YOU DEAD'
    while end != start:
        for i in range(size):
            if matrix[end][i][0] != 0:
                temp = weight - matrix[end][i][0]
                if temp == distance[i][0]:
                    weight = temp
                    end = i
                    vertexPath.append(i)
    vertexPath.reverse()               
    return vertexPath

witcher = hero((0,1) ,5 ,(2,1))

Field = '''
        0020
        0900
        9090
        0900
'''
Len = 4
Width = 4
Matrix = fieldToMatrix(Len,Width,Field)
#print(pathWithOutMonsters(witcher.start, witcher.end, Matrix, Len, Width))

print(pathWithMonsters(witcher.start, witcher.end, Matrix, Len, Width, witcher.hp))
