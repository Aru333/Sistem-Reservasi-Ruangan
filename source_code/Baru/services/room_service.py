from patterns.factory.room_factory import RoomFactory

class RoomService:
    def __init__(self):
        self.rooms = []
        self._seed_data()

    def _seed_data(self):
        self.create_room_manual("meeting", "Ruang Rapat A", 10, "4K Projector")
        self.create_room_manual("meeting", "Ruang Sidang", 10, "4K Projector")
        self.create_room_manual("lab", "Lab Komputer", 40, "Linux Ubuntu")
        self.create_room_manual("auditorium", "Ruang Seminar", 60, "Speaker Standar")
        self.create_room_manual("auditorium", "Aula Utama", 200, "Dolby Atmos")

    def create_room_manual(self, room_type, name, capacity, extra_info):
        r_id = len(self.rooms) + 1
        new_room = RoomFactory.create(room_type, r_id, name, capacity, extra_info)
        self.rooms.append(new_room)
        return new_room

    def get_all_rooms(self):
        return self.rooms

    def find_room_by_id(self, room_id_str):
        return next((r for r in self.rooms if str(r.room_id) == str(room_id_str)), None)