class Room:

  def __init__(self, room_id, name, room_type, capacity, extra_info=""):
    self.room_id = room_id
    self.name = name
    self.room_type = room_type  # "meeting", "lab", "auditorium"
    self.capacity = capacity
    self.extra_info = extra_info

  def get_description(self):
    if self.room_type == "meeting":
      return (
          f"[Meeting Room] {self.name} (Kapasitas: {self.capacity} org) -"
          f" Proyektor: {self.extra_info}"
      )
    elif self.room_type == "lab":
      return (
          f"[Lab Computer] {self.name} (Kapasitas: {self.capacity} org) - OS:"
          f" {self.extra_info}"
      )
    elif self.room_type == "auditorium":
      return (
          f"[Auditorium] {self.name} (Kapasitas: {self.capacity} org) - Sound"
          f" System: {self.extra_info}"
      )
    else:
      return f"[General] {self.name} (Kapasitas: {self.capacity} org)"