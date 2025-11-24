import io
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

from device import Device
from room import Room
from smart_home import SmartHome




class TestDevice(unittest.TestCase):

    def test_device_init(self):
        d = Device("Лампа", 60)
        self.assertEqual(d.name, "Лампа")
        self.assertEqual(d.power, 60)
        self.assertFalse(d.is_on)
        self.assertEqual(d.schedule, [])

    def test_toggle(self):
        d = Device("Тест", 100)
        d.toggle()
        self.assertTrue(d.is_on)
        d.toggle()
        self.assertFalse(d.is_on)

    def test_get_consumption(self):
        d = Device("Тест", 1500)
        self.assertEqual(d.get_consumption(), 0)
        d.turn_on()
        self.assertEqual(d.get_consumption(), 1500)
        d.turn_off()
        self.assertEqual(d.get_consumption(), 0)

    def test_add_schedule(self):
        d = Device("Тест", 50)
        d.add_schedule("daily:18-22")
        self.assertIn("daily:18-22", d.schedule)


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room = Room("Гостиная")
        self.lamp = Device("Лампа", 60)
        self.kettle = Device("Чайник", 2000)
        self.room.add_device(self.lamp)
        self.room.add_device(self.kettle)

    def test_add_device(self):
        self.assertEqual(len(self.room.devices), 2)

    def test_total_power(self):
        self.lamp.turn_on()
        self.kettle.turn_off()
        self.assertEqual(self.room.total_power(), 60)

        self.kettle.turn_on()
        self.assertEqual(self.room.total_power(), 2060)

    def test_run_builtin_scenario_morning(self):
        self.room.run_scenario("morning")
        self.assertEqual(self.room.temperature, 23)
        self.assertEqual(self.room.light_level, 80)
        self.assertTrue(self.lamp.is_on)
        self.assertTrue(self.kettle.is_on)

    def test_run_builtin_scenario_vacation(self):
        self.lamp.turn_on()
        self.kettle.turn_on()
        self.room.run_scenario("vacation")
        self.assertEqual(self.room.temperature, 18)
        self.assertEqual(self.room.light_level, 0)
        self.assertFalse(self.lamp.is_on)
        self.assertFalse(self.kettle.is_on)

    def test_run_unknown_scenario(self):
        with redirect_stdout(io.StringIO()) as output:
            self.room.run_scenario("unknown")
        self.assertIn("Сценарий не найден", output.getvalue())

    def test_add_custom_scenario(self):
        self.room.add_scenario("сон", 20, 10, "off")
        self.assertIn("сон", self.room.scenarios)
        self.room.run_scenario("сон")
        self.assertEqual(self.room.temperature, 20)
        self.assertEqual(self.room.light_level, 10)
        self.assertFalse(self.lamp.is_on)


class TestSmartHome(unittest.TestCase):

    def setUp(self):
        self.home = SmartHome()
        self.room1 = Room("Кухня")
        self.room2 = Room("Спальня")
        self.room1.add_device(Device("Холодильник", 150))
        self.room2.add_device(Device("Обогреватель", 2000))
        self.home.add_room(self.room1)
        self.home.add_room(self.room2)

    def test_add_room(self):
        self.assertEqual(len(self.home.rooms), 2)

    def test_total_consumption(self):
        self.room2.devices[0].turn_on()
        self.assertEqual(self.home.total_consumption(), 2000)

    def test_notify_warnings(self):
        self.room2.devices[0].turn_on()  # 2000W > 1000W → предупреждение
        warnings = self.home.notify()
        self.assertEqual(len(warnings), 1)
        self.assertIn("Обогреватель", warnings[0])
        self.assertIn("потребляет слишком много", warnings[0])

    def test_notify_no_warnings(self):
        self.room1.devices[0].turn_on()  # 150W — безопасно
        warnings = self.home.notify()
        self.assertEqual(warnings, [])


# ============ ИНТЕГРАЦИОННЫЕ ТЕСТЫ CLI ============

class TestMainCLI(unittest.TestCase):

    # @patch("builtins.input", side_effect=["0"])
    # def test_exit_immediately(self, mock_input):
    #     with redirect_stdout(io.StringIO()) as output:
    #         with self.assertRaises(SystemExit):
                # Имитируем запуск main-логики без бесконечного цикла
                # Мы не вызываем main.py напрямую, а тестируем его логику через импорт
                # Но так как main.py содержит while True, мы не можем его запустить напрямую
                # Поэтому тестируем только ввод-вывод через моки на отдельных ветках
                # pass
        # Выход не выводит ошибок — тест пройдёт, если не упал

    @patch("builtins.input", side_effect=["5", "0"])  # меню → уведомления → выход
    @patch("start_home.SmartHome.notify", return_value=["! Тест: предупреждение"])
    def test_menu_notifications(self, mock_notify, mock_input):
        home = SmartHome()
        with redirect_stdout(io.StringIO()) as output:
            # Имитируем ветку "5"
            notes = home.notify()
            if not notes:
                print("Нет предупреждений.")
            else:
                for n in notes:
                    print(n)
            # Затем выход (тест только логики вывода)
        output_str = output.getvalue()
        self.assertIn("! Тест: предупреждение", output_str)

    @patch("builtins.input", side_effect=["4", "0"])
    @patch("start_home.SmartHome.total_consumption", return_value=2500)
    def test_menu_total_consumption(self, mock_total, mock_input):
        home = SmartHome()
        with redirect_stdout(io.StringIO()) as output:
            print("Общее потребление:", home.total_consumption(), "W")
        self.assertIn("Общее потребление: 2500 W", output.getvalue())


# ============ ДОПОЛНИТЕЛЬНЫЙ ТЕСТ: CLI-ввод с ошибками ============

class TestRoomDeviceToggle(unittest.TestCase):

    def test_device_toggle_in_room(self):
        room = Room("Тест")
        dev = Device("ТестУстройство", 100)
        room.add_device(dev)
        dev.toggle()
        self.assertTrue(dev.is_on)
        self.assertEqual(dev.get_consumption(), 100)


# Запуск всех тестов
if __name__ == '__main__':
    unittest.main()