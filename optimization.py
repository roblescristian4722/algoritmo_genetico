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
    """
    domStart: inicio del dominio
    domEnd: final del dominio
    alleles: Cantidad de alelos (bit) por cada gen a generar
    Retorna un diccionario de genes compuestos por una cierta cantidad de alelos
    """
    solutions = {}
    increment = ( abs(domStart) + abs(domEnd) ) / ( 2 ** alleles - 1 )
    maxDigits = len(decimalToBinary(2 ** alleles - 1))
    print(decimalToBinary(2 ** alleles + 1))
    for i in range(2 ** alleles):
        key = decimalToBinary(i)
        if len(key) < maxDigits:
            key = fillZeros(key, maxDigits)
        solutions[key] = domStart
        domStart += increment
    return solutions

# Datos iniciales
generations = 20
domStart = -200
domEnd = 200

x = codifyData(domStart, domEnd, 10)
# y = codifyData(domStart, domEnd, 10)

print(len(x))
