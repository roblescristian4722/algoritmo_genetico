#!/usr/bin/env python
import random

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

def fitness(x: dict, greatest):
    """Fitness function"""
    fit = {}
    for k, v in x.items():
        fit[k] = -absolute(v) + greatest
    # Relative fitness
    for k, v in fit.items():
        x[k] = fit[k] / sum(fit.values())

def subdict(x: dict, start, end) -> dict:
    """Retorna un subdirectorio de un determinado rango en un directorio"""
    sub = {}
    i = 0
    for k, v in x.items():
        if i >= start and i <= end:
            sub[k] = v
            if i == end:
                break
        i += 1
    return sub

def getParents(fit: dict, n: int) -> list:
    """Realiza la cruza"""
    parent = []
    parents = []
    while (len(parents) < n - 2):
        r = random.random()
        for k, v in fit.items():
            if len(parent) == 2:
                break
            if r < v and ( len(parent) == 0 or (len(parent) == 1 and parent[0] != k) ):
                parent.append(k)
        if len(parent) == 2:
            parents.append(parent)
            parent = []
    return parents

def crossover(fit: dict, n: int):
    for parents in getParents(fit, n):
        crossPoint = int(( random.random() * 10 ) % ( n - 1 )) + 1
        print(crossPoint)
        print(parents)
        child1 = parents[0][:crossPoint] + parents[1][crossPoint:]
        child2 = parents[1][:crossPoint] + parents[0][crossPoint:]
        print(f"child1: {child1} | child2: {child2}")


# Datos iniciales
generations = 20
domStart = -10
domEnd = 10
parentsGeneration = 10
alleles = 8

x = codifyData(domStart, domEnd, alleles)
y = codifyData(domStart, domEnd, alleles)
gr = greatest(x)

fitX = subdict(x, 0, parentsGeneration - 1)
fitY = subdict(y, 0, parentsGeneration - 1)

fitness(fitX, gr)
fitness(fitY, gr)

crossover(fitX, alleles)
