class Room:
  #Kelas dasar semua ruangan. Subclass mengisi label, aturan, dan atribut khususnya.
  label = "General"
  max_duration_hours = 4

  def __init__(self, room_id, name, capacity):
    self.room_id = room_id
    self.name = name
    self.capacity = capacity

  def get_description(self):
    return f"[{self.label}] {self.name} (Kapasitas: {self.capacity} org)"


class MeetingRoom(Room):
  label = "Meeting Room"
  max_duration_hours = 2

  def __init__(self, room_id, name, capacity, projector):
    super().__init__(room_id, name, capacity)
    self.projector = projector

  def get_description(self):
    return f"{super().get_description()} - Proyektor: {self.projector}"


class LabRoom(Room):
  label = "Lab Computer"
  max_duration_hours = 3

  def __init__(self, room_id, name, capacity, os):
    super().__init__(room_id, name, capacity)
    self.os = os

  def get_description(self):
    return f"{super().get_description()} - OS: {self.os}"


class Auditorium(Room):
  label = "Auditorium"
  max_duration_hours = 4

  def __init__(self, room_id, name, capacity, sound_system):
    super().__init__(room_id, name, capacity)
    self.sound_system = sound_system

  def get_description(self):
    return f"{super().get_description()} - Sound System: {self.sound_system}"