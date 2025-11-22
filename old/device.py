from datetime import datetime, time

class Device:
    def __init__(self, name: str, power_w: float):
        self.name = name
        self.power_w = power_w
        self.is_on = False
        self.schedule = []

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on

    def add_schedule(self, start: time, end: time):
        self.schedule.append({'start': start, 'end': end})

    def check_schedule(self, current_time=None):
        if current_time is None:
            current_time = datetime.now().time()
        for slot in self.schedule:
            if slot['start'] <= current_time <= slot['end']:
                self.turn_on()
                return
        self.turn_off()

    def hourly_consumption_kwh(self):
        return (self.power_w / 1000.0) if self.is_on else 0.0

    def __repr__(self):
        return f"Device('{self.name}', {'ON' if self.is_on else 'OFF'}, {self.power_w}W)"
