from unittest import TestCase
import time


def en_lista(num:int) -> list:
    """
    function to make a list whit a number's digits
    Args:
        num: number to be separated in its digits

    Returns: a list with parameter number's digits example: 234 -> [2,3,4]

    """
    try:
        result = list(map(int, str(num)))
    except:
        result = []
    return result


def creciente(num:int) -> bool:
    """

    Args:
        num: number to be analized

    Returns: a bool, True if number parameter is an increaser number

    """

    lista = en_lista(num)
    creci = True
    # loop for adjacent digits comparison
    for pos in range(0, len(str(num))-1):
        if lista[pos+1] < lista[pos]:
            creci = False
            break
    return creci


def decreciente(num:int) -> bool:
    """

    Args:
        num: number to be analized

    Returns: a bool, True if number parameter is an decreaser number

    """

    lista = en_lista(num)
    decre = True
    # loop for adjacent digits comparison
    for pos in range(0, len(str(num))-1):
        if lista[pos+1] > lista[pos]:
            decre = False
            break
    return decre


def bouncy(percent:float) -> int:
    """

    Args:
        percent: number to be compared with the proportion division

    Returns: Returns the first (minimum) number for which the proportion of bouncy numbers
            is exactly the percentage passed by parameter

    """

    i = 1  # it determines total numbers analized
    j = 0  # it determines position of bouncy number
    k = 0  # it determine proportion
    # infinite loop until condition mets
    while k != percent:
        if not creciente(i):
            if not decreciente(i):
                j += 1
                k = j/i

                if k == percent:
                    return i
                    break

        i += 1


start = time.time()
print(bouncy(0.99),time.time()-start)

class BouncyNumbersTest(TestCase):

    def test_is_a_list_whit_one(self):
        assert isinstance(en_lista(1), list)

    def test_is_an_error(self):
        assert isinstance(en_lista('a'), list)


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




