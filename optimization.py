#!/usr/bin/env python
from random import random

def decimalToBinary(num: int) -> str:
    """Convierte un entero decimal a binario en formato string"""
    holder = ""
    if num >= 1:
        holder = decimalToBinary(num // 2)
    res = holder + str(num % 2)
    return res[1:] if res[0] == '0' and len(res) > 1 else res

def fillZeros(binary: str, n: int):
    """Llena un número binario con ceros a la izquierda"""
    return '0' * (n - len(binary)) + binary

def codifyData(domStart: float, domEnd: float, alleles: int) -> dict:
    """Retorna un diccionario de genes compuestos por una cierta cantidad de alelos"""
    solutions = {}
    increment = ( abs(domStart) + abs(domEnd) ) / ( 2 ** alleles - 1 )
    maxDigits = len(decimalToBinary(2 ** alleles - 1))
    for i in range(2 ** alleles):
        key = decimalToBinary(i)
        if len(key) < maxDigits:
            key = fillZeros(key, maxDigits)
        solutions[key] = domStart
        domStart += increment
    return solutions

def absolute(*args) -> float:
    """Benchmark function"""
    res = 0
    for x in args:
        res += abs(x)
    return res

def greatest(x: dict):
    """returns greatest value of a list"""
    greatest = 0
    for _, v in x.items():
        greatest = abs(v) if abs(v) > greatest else greatest
    return greatest

def fitness(x: list, greatest):
    """Fitness function"""
    fit = []
    sumValue = 0
    for k, v in x:
        fitValue = -absolute(v) + greatest
        fit.append( [ k, fitValue ] )
        sumValue += fitValue
    # Relative fitness
    x.clear()
    for k, v in fit:
        x.append([k, v / sumValue])

def subdictAsList(x: dict, start, end) -> list:
    """Retorna un subdirectorio de un determinado rango en un directorio en forma
    de lista de duplas"""
    sub = []
    i = 0
    for k, v in x.items():
        if i >= start and i <= end:
            sub.append([k, v])
            if i == end:
                break
        i += 1
    return sub

def getParents(fit: list) -> list:
    """Retorna una lista de binas de padres que serán cruzados para obtener un hijo"""
    parent = []
    parents = []
    while (len(parents) < len(fit) / 2):
        r = random()
        for k, v in fit:
            if len(parent) == 2:
                break
            if r < v and ( len(parent) == 0 or (len(parent) == 1 and parent[0] != k) ):
                parent.append(k)
        if len(parent) == 2:
            parents.append(parent)
            parent = []
    return parents

def crossover(fit: list, n: int) -> list:
    """Realiza la cruza"""
    newGen = []
    for parents in getParents(fit):
        crossPoint = int(( random() * 10 ) % ( n - 1 )) + 1
        newGen.append( parents[0][:crossPoint] + parents[1][crossPoint:] )
        newGen.append( parents[1][:crossPoint] + parents[0][crossPoint:] )
    return newGen

def mutation(x: list):
    """Aplica una mutación con un 2% de efectuarse sobre cada bit de los individuos
    de la población"""
    mutRate = 0.98
    i = 0
    while i < len(x):
        j = 0
        while j < len(x[i]):
            if random() >= mutRate:
                newAllele = "1" if x[i][j] == "0" else "0"
                x[i] = x[i][:j] + newAllele + x[i][j + 1:]
            j += 1
        i += 1

def generatePairs(population: list, domain: dict):
    """Genera una lista de tuplas de tipo:
        código_binario: valor del dominio de la función"""
    pairs = []
    for i in population:
        pairs.append([ i, domain[i] ])
    return pairs

# Datos iniciales
generations = 10000
domStart = -10
domEnd = 10
poblationSize = 25
alleles = 8

# Dominio y rango de la función
x = codifyData(domStart, domEnd, alleles)
y = codifyData(domStart, domEnd, alleles)
gr = greatest(x)

# Población inicial
X = subdictAsList(x, 0, poblationSize - 1)
Y = subdictAsList(y, 0, poblationSize - 1)

while generations > 0:
    fitness(X, gr)
    fitness(Y, gr)

    newGenX = crossover(X, alleles)
    newGenY = crossover(Y, alleles)
    mutation(newGenX)
    mutation(newGenY)
    X = generatePairs(newGenX, x)
    Y = generatePairs(newGenY, y)
    print(generations)
    generations -= 1
print(f"X: {X}\n\nY:{Y}")
