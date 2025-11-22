from datetime import time
from device import Device
from room import Room
from smarthome import SmartHome


# === ПРИМЕР ЗАПУСКА ПРОГРАММЫ ===
if __name__ == "__main__":
    # Создаём устройства
    lamp = Device("Лампа", 60)
    tv = Device("Телевизор", 100)
    coffee_maker = Device("Кофеварка", 1500)
    ac = Device("Кондиционер", 1200)

    # Настраиваем расписание для лампы (включать с 18:00 до 22:00)
    lamp.add_schedule(time(18, 0), time(22, 0))

    # Создаём комнаты
    living_room = Room("Гостиная")
    living_room.add_device(lamp)
    living_room.add_device(tv)
    living_room.add_device(ac)

    kitchen = Room("Кухня")
    kitchen.add_device(coffee_maker)

    # Инициализируем умный дом
    home = SmartHome()
    home.add_room(living_room)
    home.add_room(kitchen)

    # Применяем сценарии
    home.apply_scenario_to_room("Кухня", "утро")
    home.apply_scenario_to_room("Гостиная", "вечер")

    # Проверяем расписание (имитация текущего времени)
    home.check_all_schedules()

    # Проверяем энергопотребление
    home.check_energy_alert()

    # Показываем текущий статус
    home.show_status()

    # Пример удалённого управления
    home.toggle_device("Гостиная", "Телевизор")
    home.show_status()
