#!/usr/bin/env python

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

def greatest(x: list):
    """returns greatest value of a list"""
    greatest = abs(x[0])
    for i in x:
        greatest = abs(i) if abs(i) > greatest else greatest
    return greatest

def fitness(x, greatest):
    """Fitness function"""
    fit = []
    for i in x:
        fit.append(-absolute(i) + greatest)
    # Relative fitness
    print(fit)
    i = 0
    while i < len(x):
        x[i] = fit[i] / sum(fit)
        i += 1

# Datos iniciales
generations = 20
domStart = -10
domEnd = 10

x = codifyData(domStart, domEnd, 8)
y = codifyData(domStart, domEnd, 8)

sampleX = [ v for _, v in x.items() ]
sampleY = [ v for _, v in y.items() ]
X = sampleX[:10]
Y = sampleY[:10]

fitness(X, greatest(sampleX))
fitness(Y, greatest(sampleY))
