# main.py
import sys
import os
from smart_home import SmartHome
from room import Room
from device import Device

def run_cli():
    home = SmartHome()

    def show_menu():
        print("\n=== SmartHome CLI ===")
        print("1. Добавить комнату")
        print("2. Добавить устройство в комнату")
        print("3. Управлять комнатой")
        print("4. Общее потребление")
        print("5. Уведомления")
        print("0. Выход")

    while True:
        show_menu()
        cmd = input(">> ")
        # os.system("cls" if os.name == "nt" else "clear")

        if cmd == "1":
            name = input("Название комнаты: ")
            home.add_room(Room(name))
            print("Добавлено.")
# здесь был Бараускас
        elif cmd == "2":
            if not home.rooms:
                print("Нет комнат.")
                continue
            for i, r in enumerate(home.rooms, start=1):
                print(f"{i}. {r.name}")
            try:
                idx = int(input("Выбери номер комнаты: ")) - 1
                if not (0 <= idx < len(home.rooms)):
                    print("Неверный номер комнаты")
                    continue
            except ValueError:
                print("Ошибка: нужно ввести число")
                continue
            room = home.rooms[idx]
            dname = input("Название устройства: ")
            try:
                power = float(input("Потребление (W): "))
            except ValueError:
                print("Ошибка: нужно ввести число для мощности")
                continue
            room.add_device(Device(dname, power))
            print("Устройство добавлено.")

        elif cmd == "3":
            if not home.rooms:
                print("Нет комнат.")
                continue
            for i, r in enumerate(home.rooms, start=1):
                print(f"{i}. {r.name}")
            try:
                idx = int(input("Выбери номер комнаты: ")) - 1
                if not (0 <= idx < len(home.rooms)):
                    print("Неверный номер комнаты")
                    continue
            except ValueError:
                print("Ошибка: нужно ввести число")
                continue
            room = home.rooms[idx]

            print("\n1. Сценарии\n2. Список устройств\n3. Включить/выключить устройство")
            sub = input(">> ")

            if sub == "1":
                print("0. Добавить новый сценарий")
                names = list(room.scenarios.keys())
                for i, name in enumerate(names, start=1):
                    print(f"{i}. {name}")
                sc = input("Выбери сценарий или '0': ")
                if sc == "0":
                    try:
                        name = input("Имя сценария: ")
                        temp = int(input("Температура: "))
                        light = int(input("Свет (0-100): "))
                        devices = input("Устройства (on/off/none): ")
                        room.add_scenario(name, temp, light, devices)
                    except ValueError:
                        print("Ошибка: неверный ввод числового значения")
                else:
                    try:
                        idx = int(sc) - 1
                        if not (0 <= idx < len(names)):
                            print("Неверный выбор")
                            continue
                        room.run_scenario(names[idx])
                    except ValueError:
                        print("Ошибка: нужно ввести число")

            elif sub == "2":
                for d in room.devices:
                    print("-", d)
            elif sub == "3":
                for i, d in enumerate(room.devices, start=1):
                    print(f"{i}. {d.name}")
                try:
                    idx = int(input("Выбери номер устройства: ")) - 1
                    if not (0 <= idx < len(room.devices)):
                        print("Неверный номер устройства")
                        continue
                except ValueError:
                    print("Ошибка: нужно ввести число")
                    continue
                room.devices[idx].toggle()
                print(f"{room.devices[idx]} | Потребление: {room.devices[idx].get_consumption()}W")

        elif cmd == "4":
            print("Общее потребление:", home.total_consumption(), "W")

        elif cmd == "5":
            notes = home.notify()
            if not notes:
                print("Нет предупреждений.")
            else:
                for n in notes:
                    print(n)

        elif cmd == "0":
            sys.exit(0)


if __name__ == "__main__":
    run_cli()
