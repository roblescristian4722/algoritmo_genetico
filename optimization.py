#!/usr/bin/env python
from random import random
import matplotlib.pyplot as plt
import numpy as np

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
generations = 200
domStart = -10
domEnd = 10
poblationSize = 50
alleles = 8

# Dominio y rango de la función
domain = codifyData(domStart, domEnd, alleles)
gr = greatest(domain)
# Población inicial
X = subdictAsList(domain, len(domain) / 2  - poblationSize / 2, len(domain) / 2 + poblationSize / 2 - 1)

# Impresión en consola de datos iniciales
print("Datos iniciales:")
print("Generaciones: ", generations)
print("Tamaño de la población: ", len(X))
print("Número de alelos: ", alleles)
print(f"Población inicial (X): [{X[0]}, {X[len(X) - 1]}]")
print(f"Dominio sobre el que se evaluará la función: \
    [{list(domain.items())[0]}, {list(domain.items())[len(domain) - 1]}]")

i = 0
x_evolution = []
min = abs(domEnd)
minGen = 0
xValues = []
mean = 0
while i < generations:
    fitness(X, gr)
    newGenX = crossover(X, alleles)
    mutation(newGenX)
    X = generatePairs(newGenX, domain)

    print(f"progreso: {int( i / generations * 100 )}%", end="\r")
    i += 1

    xValues = [v for _, v in X ]
    mean = np.mean(xValues)
    if abs(mean) < min:
        min = abs(mean)
        minGen = i
    x_evolution.append(mean)

fig = plt.figure()
ax = fig.add_subplot()
fig.suptitle('Algoritmo genético para función benchmark "absolute"', fontweight='bold')
ax.set_title('Evolución de la población a través de las generaciones')
ax.set_ylabel('Promedio de la población (X)')
ax.set_xlabel('Cantidad de generaciones')
plt.plot([0 for _ in range(generations)], 'g--', label="Valor óptimo (mínimo global)")
plt.plot(range(generations), x_evolution, 'b-', label="Evolución de la población")
plt.plot(minGen, min, 'r*', label="Mejor solución encontrada")
plt.plot(generations, mean, 'r+', label="Última solución encontrada")
ax.legend()

print(f"\nResultados:\nX (promedio): {mean}")
plt.show()
