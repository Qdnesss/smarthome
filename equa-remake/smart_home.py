from room import Room
from device import Device

class SmartHome:
    def __init__(self):
        self.rooms: list[Room] = []

    def add_room(self, room: Room):
        self.rooms.append(room)

    def list_rooms(self):
        return self.rooms

    def total_consumption(self):
        return sum(room.total_power() for room in self.rooms)

    def notify(self):
        warnings = []
        for room in self.rooms:
            for dev in room.devices:
                if dev.is_on and dev.power > 1000:
                    warnings.append(f"! {room.name}: {dev.name} потребляет слишком много")
        return warnings
