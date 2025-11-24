class Device:
    def __init__(self, name: str, power: float):
        self.name = name
        self.power = power
        self.is_on = False
        self.schedule = []

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on

    def get_consumption(self):
        return self.power if self.is_on else 0

    def add_schedule(self, rule: str):
        self.schedule.append(rule)

    def __str__(self):
        return f"{self.name} | {'ON' if self.is_on else 'OFF'} | {self.power}W"
