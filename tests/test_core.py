import random
import pytest
from game import GeoWar


@pytest.fixture
def target_count():
    return 5


@pytest.fixture
def gw_state(target_count):
    g = GeoWar()
    g.targets = [random.randint(1, 89) for _ in range(target_count)]

    state = g.yield_play()
    output_state = next(state)
    assert output_state == 'READY FOR A NEW GAME?'

    input_state = next(state)
    input_state('y')
    output_state = next(state)
    assert output_state == 'ENTER DEGREE OF SHOT'

    return g, state


def test_hit(target_count, gw_state):  # проверка на попадание
    gw, state = gw_state
    input_state = next(state)
    input_state(gw.targets[0])
    output_state = next(state)
    output_state_2 = next(state)
    assert output_state == '..CONGRATULATIONS..   A HIT.'
    assert len(gw.targets) == target_count - 1
    assert output_state_2 == 'ENTER DEGREE OF SHOT'


def test_near_hit(gw_state):  # проверка на близкий промах (расстояние в 1 градус)
    gw, state = gw_state
    gw.targets = [random.randint(1, 89)]

    input_state = next(state)
    input_state(gw.targets[0] - 1)
    output_state = next(state)
    input_state_2 = next(state)
    assert output_state == 'A NEAR HIT. ENEMY HAS RELOCATED.'
    assert input_state_2 == 'ENTER DEGREE OF SHOT'
    assert len(gw.targets) == 1


def test_lose(gw_state):  # проверка на полный промах
    gw, state = gw_state
    gw.targets = [random.randint(42, 56)]

    input_state = next(state)
    input_state(gw.targets[0] + random.randint(6, 10))
    output_state = next(state)
    input_state_2 = next(state)
    assert output_state == 'NO LUCK -- TRY AGAIN.'
    assert input_state_2 == 'ENTER DEGREE OF SHOT'
    assert len(gw.targets) == 1


# проверка когда программа ожидает ввода числа а пользователь вводит текст
# программа ответит что неверный ввод
def test_wrong_input(gw_state):
    gw, state = gw_state
    gw.targets = [random.randint(1, 89)]

    input_state = next(state)
    input_state('wrong input')
    output_state = next(state)
    input_state_2 = next(state)
    assert output_state == 'PLEASE ENTER A VALID INTEGER.'
    assert input_state_2 == 'ENTER DEGREE OF SHOT'
    assert len(gw.targets) == 1


# проверка случая когда пользователь вводит неверный угол ( больше 90 или меньше 0 )
def test_wrong_angle(gw_state):
    gw, state = gw_state
    gw.targets = [random.randint(1, 89)]

    input_state = next(state)
    input_state(random.randint(91, 100))
    output_state = next(state)
    input_state_2 = next(state)
    assert output_state == 'ANGLE MUST BE BETWEEN 1 AND 90.'
    assert input_state_2 == 'ENTER DEGREE OF SHOT'
    assert len(gw.targets) == 1

    input_state = next(state)
    input_state(random.randint(-300, -1))
    output_state = next(state)
    input_state_2 = next(state)
    assert output_state == 'ANGLE MUST BE BETWEEN 1 AND 90.'
    assert input_state_2 == 'ENTER DEGREE OF SHOT'
    assert len(gw.targets) == 1
