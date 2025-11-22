from device import Device

class Room:
    def __init__(self, name: str):
        self.name = name
        self.devices: list[Device] = []
        self.temperature = 22
        self.light_level = 50  # 0–100
        self.scenarios = {
            "morning": {"temp": 23, "light": 80, "devices": "on"},
            "evening": {"temp": 21, "light": 30, "devices": None},
            "vacation": {"temp": 18, "light": 0, "devices": "off"},
        }

    def add_device(self, device: Device):
        self.devices.append(device)

    def total_power(self):
        return sum(d.get_consumption() for d in self.devices)

    # вызов сценария
    def run_scenario(self, name: str):
        if name not in self.scenarios:
            print("Сценарий не найден")
            return
        sc = self.scenarios[name]
        self.temperature = sc["temp"]
        self.light_level = sc["light"]
        if sc["devices"] == "on":
            for d in self.devices:
                d.turn_on()
        elif sc["devices"] == "off":
            for d in self.devices:
                d.turn_off()
        print(f"Сценарий '{name}' выполнен: {self.temperature}°C, свет {self.light_level}")

    def add_scenario(self, name: str, temp: int, light: int, devices: str):
        self.scenarios[name] = {"temp": temp, "light": light, "devices": devices}
        print(f"Сценарий '{name}' добавлен")

    def __str__(self):
        return f"{self.name} | {len(self.devices)} устройств | {self.total_power()}W | {self.temperature}°C | свет {self.light_level}"
