import importlib.util
import pathlib

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / 'personal' / 'Math 690' / 'reversePolishNotation.py'
spec = importlib.util.spec_from_file_location('rpn', MODULE_PATH)
rpn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rpn)


def test_simple_addition():
    computer = rpn.Computer(['2', '3', '+'])
    result = computer.returnResult()
    assert result == 5


def test_complex_expression():
    # Expression: 2 + 5 - 6 * 7 + 4 -> -31
    expr = list('2567*-4++')
    computer = rpn.Computer(expr)
    assert computer.returnResult() == -31
