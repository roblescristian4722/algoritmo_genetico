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

def subdict(x: dict, start, end):
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

# Datos iniciales
generations = 20
domStart = -10
domEnd = 10

x = codifyData(domStart, domEnd, 8)
y = codifyData(domStart, domEnd, 8)

X = subdict(x, 0, 9)
Y = subdict(x, 0, 9)
fitness(X, greatest(X))
fitness(Y, greatest(Y))
