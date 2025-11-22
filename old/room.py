class Room:
    def __init__(self, name: str):
        self.name = name
        self.devices = []
        self.temperature_c = 20.0
        self.light_brightness = 0

    def add_device(self, device):
        self.devices.append(device)

    def set_temperature(self, temp):
        self.temperature_c = temp

    def set_light(self, brightness):
        self.light_brightness = max(0, min(100, brightness))

    def apply_scenario(self, scenario: str):
        if scenario == "утро":
            self.set_light(70)
            self.set_temperature(22.0)
            for d in self.devices:
                if "кофеварка" in d.name.lower():
                    d.turn_on()
        elif scenario == "вечер":
            self.set_light(40)
            self.set_temperature(20.0)
            for d in self.devices:
                if "телевизор" in d.name.lower():
                    d.turn_on()
        elif scenario == "отпуск":
            self.set_temperature(16.0)
            for d in self.devices:
                d.turn_off()
        else:
            raise ValueError(f"Неизвестный сценарий: {scenario}")

    def hourly_consumption_kwh(self):
        return sum(d.hourly_consumption_kwh() for d in self.devices)

    def __repr__(self):
        return f"Room('{self.name}', temp={self.temperature_c}°C, light={self.light_brightness}%)"
