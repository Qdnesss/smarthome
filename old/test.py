import unittest
from datetime import time
from device import Device
from room import Room
from smarthome import SmartHome


class TestDevice(unittest.TestCase):

    def test_device_initial_state(self):
        dev = Device("Лампа", 60)
        self.assertEqual(dev.name, "Лампа")
        self.assertEqual(dev.power_w, 60)
        self.assertFalse(dev.is_on)
        self.assertEqual(dev.schedule, [])

    def test_toggle_device(self):
        dev = Device("Тест", 100)
        dev.toggle()
        self.assertTrue(dev.is_on)
        dev.toggle()
        self.assertFalse(dev.is_on)

    def test_schedule_activation(self):
        dev = Device("Лампа", 60)
        dev.add_schedule(time(18, 0), time(22, 0))
        # Тестируем вне расписания
        dev.check_schedule(time(10, 0))
        self.assertFalse(dev.is_on)
        # Тестируем внутри расписания
        dev.check_schedule(time(20, 0))
        self.assertTrue(dev.is_on)

    def test_hourly_consumption(self):
        dev = Device("Тест", 1000)  # 1000 Вт = 1 кВт
        self.assertEqual(dev.hourly_consumption_kwh(), 0.0)
        dev.turn_on()
        self.assertEqual(dev.hourly_consumption_kwh(), 1.0)


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room = Room("Гостиная")
        self.lamp = Device("Лампа", 60)
        self.tv = Device("Телевизор", 100)
        self.room.add_device(self.lamp)
        self.room.add_device(self.tv)

    def test_initial_state(self):
        self.assertEqual(self.room.name, "Гостиная")
        self.assertEqual(self.room.temperature_c, 20.0)
        self.assertEqual(self.room.light_brightness, 0)
        self.assertEqual(len(self.room.devices), 2)

    def test_set_temperature_and_light(self):
        self.room.set_temperature(22.5)
        self.room.set_light(80)
        self.assertEqual(self.room.temperature_c, 22.5)
        self.assertEqual(self.room.light_brightness, 80)

    def test_apply_scenario_morning(self):
        self.room.apply_scenario("утро")
        self.assertEqual(self.room.light_brightness, 70)
        self.assertEqual(self.room.temperature_c, 22.0)
        # Ни одно устройство не включено (нет "кофеварки")
        self.assertFalse(self.lamp.is_on)
        self.assertFalse(self.tv.is_on)

    def test_apply_scenario_evening(self):
        self.room.apply_scenario("вечер")
        self.assertEqual(self.room.light_brightness, 40)
        self.assertEqual(self.room.temperature_c, 20.0)
        self.assertTrue(self.tv.is_on)  # телевизор включён
        self.assertFalse(self.lamp.is_on)

    def test_apply_scenario_vacation(self):
        self.lamp.turn_on()
        self.tv.turn_on()
        self.room.apply_scenario("отпуск")
        self.assertEqual(self.room.temperature_c, 16.0)
        self.assertFalse(self.lamp.is_on)
        self.assertFalse(self.tv.is_on)

    def test_invalid_scenario(self):
        with self.assertRaises(ValueError):
            self.room.apply_scenario("неизвестный")

    def test_hourly_consumption(self):
        self.lamp.turn_on()  # 60 Вт → 0.06 кВт
        self.tv.turn_off()   # 0
        expected = 0.06
        self.assertAlmostEqual(self.room.hourly_consumption_kwh(), expected, places=5)


class TestSmartHome(unittest.TestCase):

    def setUp(self):
        self.home = SmartHome()
        self.living_room = Room("Гостиная")
        self.kitchen = Room("Кухня")

        self.tv = Device("Телевизор", 100)
        self.coffee = Device("Кофеварка", 1500)

        self.living_room.add_device(self.tv)
        self.kitchen.add_device(self.coffee)

        self.home.add_room(self.living_room)
        self.home.add_room(self.kitchen)

    def test_add_room(self):
        self.assertEqual(len(self.home.rooms), 2)

    def test_toggle_existing_device(self):
        self.home.toggle_device("Гостиная", "Телевизор")
        self.assertTrue(self.tv.is_on)
        self.assertIn("включено", self.home.notifications[-1])

    def test_toggle_missing_device(self):
        self.home.toggle_device("Гостиная", "Холодильник")
        self.assertIn("не найдено", self.home.notifications[-1])

    def test_apply_scenario_to_existing_room(self):
        self.home.apply_scenario_to_room("Кухня", "утро")
        self.assertTrue(self.coffee.is_on)
        self.assertEqual(self.kitchen.temperature_c, 22.0)
        self.assertEqual(self.kitchen.light_brightness, 70)

    def test_apply_scenario_to_missing_room(self):
        self.home.apply_scenario_to_room("Спальня", "утро")
        self.assertIn("не найдена", self.home.notifications[-1])

    def test_total_energy_consumption(self):
        self.coffee.turn_on()  # 1500 Вт → 1.5 кВт
        total = self.home.total_hourly_consumption_kwh()
        self.assertAlmostEqual(total, 1.5, places=2)

    def test_energy_alert(self):
        # Установим порог ниже текущего потребления
        self.home.energy_threshold_kwh = 1.0
        self.coffee.turn_on()  # 1.5 кВт > 1.0 → должно быть уведомление
        self.home.check_energy_alert()
        self.assertTrue(any("Внимание!" in msg for msg in self.home.notifications))

    def test_daily_estimate(self):
        self.tv.turn_on()  # 100 Вт → 0.1 кВт/ч
        daily = self.home.get_daily_energy_estimate_kwh()
        self.assertAlmostEqual(daily, 0.1 * 24, places=2)  # 2.4 кВт·ч


if __name__ == '__main__':
    unittest.main()