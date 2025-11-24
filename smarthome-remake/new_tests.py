# tests.py
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

try:
    from main import run_cli as smart_home_main
except ImportError:
    print("Ошибка: не найден main.py или функция run_cli().")
    print("Убедись, что основной файл назван main.py и содержит функцию run_cli()")
    exit(1)


def simulate_input(inputs):
    """Генератор для имитации input()"""
    iterator = iter(inputs)
    return lambda prompt="": next(iterator, "0")


def run_menu_option(option_sequence):
    """Запускает run_cli() с заданной последовательностью ввода"""
    f = io.StringIO()
    try:
        with redirect_stdout(f), redirect_stderr(f), patch('builtins.input', side_effect=simulate_input(option_sequence)):
            smart_home_main()
        return True, ""
    except SystemExit:
        return True, ""
    except Exception as e:
        return False, str(e)


def test_all_menu_options():
    print("Тестирую все пункты меню SmartHome...\n")

    # Шаблон: создаём комнату, чтобы было куда добавлять устройства и сценарии
    base_setup = ["1", "Гостиная"]  # добавить комнату

    test_cases = [
        ["0. Выход", ["0"]],
        ["1. Добавить комнату", ["1", "Спальня", "0"]],
        ["2. Добавить устройство", base_setup + ["2", "1", "Лампа", "60", "0"]],
        ["3. Сценарии: добавить новый", base_setup + ["3", "1", "1", "0", "сон", "20", "10", "off", "0"]],
        ["3. Сценарии: выполнить встроенный", base_setup + ["3", "1", "1", "1", "1", "0"]],  # morning
        ["3. Список устройств", base_setup + ["3", "1", "2", "0"]],
        ["3. Вкл/выкл устройство", base_setup + ["3", "1", "3", "1", "0"]],
        ["4. Общее потребление", base_setup + ["4", "0"]],
        ["5. Уведомления", base_setup + ["5", "0"]],
    ]

    results = []
    for name, inputs in test_cases:
        print(f"Тестируется: {name} ...", end=" ")
        success, error = run_menu_option(inputs)
        if success:
            print("РАБОТАЕТ")
            results.append(True)
        else:
            print("ОШИБКА")
            print(f"   Ошибка: {error}")
            results.append(False)

    # Итог
    passed = sum(results)
    total = len(results)
    print("\n" + "="*50)
    print(f"Успешно: {passed} из {total}")
    if passed == total:
        print("ВСЕ ПУНКТЫ МЕНЮ РАБОТАЮТ!")
    else:
        print("Некоторые пункты вызывают ошибки. См. лог выше.")
    print("="*50)


if __name__ == "__main__":
    test_all_menu_options()
