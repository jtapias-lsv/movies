from unittest import TestCase
import time


def enlista(num:int) -> list:
    '''Devuelve una lista con los digitos de un numero pasado por parámetro'''
    try:
        result = list(map(int, str(num)))
    except:
        result = []
    return result


def creciente(num:int) -> bool:
    '''Devuelve True si el numero pasado por parámetro es creciente'''
    lista = enlista(num)
    creci = True
    # ciclo para la comparacion de digitos adyacentes
    for pos in range(0, len(str(num))-1):
        if lista[pos+1] < lista[pos]:
            creci = False
            break
    return creci


def decreciente(num:int) -> bool:
    '''Devuelve True si el numero pasado por parámetro es decreciente'''
    lista = enlista(num)
    decre = True
    # ciclo para la comparacion de digitos adyacentes
    for pos in range(0, len(str(num))-1):
        if lista[pos+1] > lista[pos]:
            decre = False
            break
    return decre


def bouncy(percent:float) -> int:
    '''Devuelve el primer número (mínimo) para el cual
       la proporción de números bouncy es exactamente el 99%'''
    i = 1  # variable que determina el total de numeros analizados
    j = 0  # variable que determina la posición consecutiva del bouncy
    k = 0  # variable que determina la proporción
    # ciclo que se ejecuta hasta que se cumpla la condición
    while k != percent:
        if not creciente(i):
            if not decreciente(i):
                j += 1  # incremento del consecutivo del bouncy
                k = j/i  # calculo de la proporción
                # condición de cumplimiento
                if k == percent:
                    # imprime: numero mínimo y proporción
                    return i
                    break  # interrupción del ciclo

        i += 1  # incremento del total de numeros analizados

# llamada a la función
#print("El numero mínimo para 99 es: " + str(bouncy(0.99)))

start = time.time()
print(bouncy(0.99),time.time()-start)

class BouncyNumbersTest(TestCase):

    def test_is_a_list_whit_one(self):
        assert isinstance(enlista(1), list)

    def test_is_an_error(self):
        assert isinstance(enlista('a'),list)


    def test_134468_is_increase_number(self):
        assert creciente(134468)


    def test_141_not_is_increase_number(self):
        assert not creciente(141)


    def test_66420_is_decrease_number(self):
        assert decreciente(66420)


    def test_648_not_is_decrease_number(self):
        assert not decreciente(648)


    def test_538_is_50_percent_bouncy_number(self):
        assert bouncy(0.5) == 538


    def test_21780_is_90_percent_bouncy_number(self):
        assert bouncy(0.9) == 21780


    def test_1587000_is_99_percent_bouncy_number(self):
        assert bouncy(0.99) == 1587000




