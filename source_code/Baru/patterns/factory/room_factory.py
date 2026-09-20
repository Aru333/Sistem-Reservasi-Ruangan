""""Menggantikan pengondisian if-else manual saat membuat objek ruangan. 
Jika ada tipe ruangan baru di masa mendatang, pengembangan cukup menambahkan 
class konkret baru tanpa mengubah kode instansiasi di UI."""

from models.room import MeetingRoom, LabRoom, Auditorium


class RoomFactory:
    """Satu-satunya tempat yang tahu cara membuat tiap tipe ruangan."""

    _room_classes = {
        "meeting": MeetingRoom,
        "lab": LabRoom,
        "auditorium": Auditorium,
    }

    @classmethod
    def create(cls, room_type, room_id, name, capacity, extra_info):
        room_class = cls._room_classes.get(room_type)
        if room_class is None:
            raise ValueError(f"Tipe ruangan tidak dikenal: {room_type}")
        return room_class(room_id, name, capacity, extra_info)