from datetime import datetime

class SmartHome:
    def __init__(self):
        self.rooms = []
        self.notifications = []
        self.energy_threshold_kwh = 5.0

    def add_room(self, room):
        self.rooms.append(room)

    def notify(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_msg = f"[{timestamp}] {message}"
        self.notifications.append(full_msg)
        print(f"Уведомление: {message}")

    def toggle_device(self, room_name, device_name):
        for room in self.rooms:
            if room.name == room_name:
                for dev in room.devices:
                    if dev.name == device_name:
                        dev.toggle()
                        state = "включено" if dev.is_on else "выключено"
                        self.notify(f"Устройство '{device_name}' в комнате '{room_name}' {state}.")
                        return
        self.notify(f"Устройство '{device_name}' не найдено в комнате '{room_name}'.")

    def check_all_schedules(self):
        now = datetime.now().time()
        for room in self.rooms:
            for dev in room.devices:
                dev.check_schedule(now)

    def total_hourly_consumption_kwh(self):
        return sum(room.hourly_consumption_kwh() for room in self.rooms)

    def check_energy_alert(self):
        total = self.total_hourly_consumption_kwh()
        if total > self.energy_threshold_kwh:
            self.notify(f"Внимание! Высокое энергопотребление: {total:.2f} кВт·ч/ч (порог: {self.energy_threshold_kwh} кВт·ч/ч)")
    def apply_scenario_to_room(self, room_name, scenario):
        for room in self.rooms:
            if room.name == room_name:
                room.apply_scenario(scenario)
                self.notify(f"Применён сценарий '{scenario}' в комнате '{room_name}'.")
                return
        self.notify(f"Комната '{room_name}' не найдена.")

    def get_daily_energy_estimate_kwh(self):
        return self.total_hourly_consumption_kwh() * 24

    def show_status(self):
        print("\n" + "="*50)
        print("СТАТУС УМНОГО ДОМА")
        print("="*50)
        total_hour = self.total_hourly_consumption_kwh()
        total_day = self.get_daily_energy_estimate_kwh()
        print(f"Энергопотребление сейчас: {total_hour:.2f} кВт·ч/ч")
        print(f"Оценка за сутки:        {total_day:.2f} кВт·ч")
        print("-"*50)
        for room in self.rooms:
            print(f"\n{room}")
            for dev in room.devices:
                print(f"  • {dev}")
        if self.notifications:
            print("\n Последние уведомления:")
            for n in self.notifications[-3:]:
                print(f"  • {n}")
        print("="*50 + "\n")