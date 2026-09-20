class Reservation:

  def __init__(self, res_id, user_name, room, date_str, time_str, duration_hours):
    self.res_id = res_id
    self.user_name = user_name
    self.room = room
    self.date_str = date_str
    self.time_str = time_str
    self.duration_hours = duration_hours
    self.status = "PENDING"

  def approve(self):
    if self.status == "PENDING":
      self.status = "APPROVED"
      return True, "Reservasi berhasil disetujui."
    elif self.status == "APPROVED":
      return False, "Reservasi sudah disetujui sebelumnya."
    elif self.status == "CANCELLED":
      return False, "Tidak dapat menyetujui reservasi yang sudah dibatalkan."
    elif self.status == "REJECTED":
      return False, "Tidak dapat menyetujui reservasi yang sudah ditolak."
    return False, "Status tidak valid."

  def reject(self):
    if self.status == "PENDING":
      self.status = "REJECTED"
      return True, "Reservasi telah ditolak."
    elif self.status == "CANCELLED":
      return False, "Reservasi sudah dibatalkan."
    elif self.status == "APPROVED":
      return False, "Reservasi yang sudah disetujui tidak bisa ditolak langsung."
    return False, "Status tidak valid."

  def cancel(self):
    if self.status in ["PENDING", "APPROVED"]:
      self.status = "CANCELLED"
      return True, "Reservasi berhasil dibatalkan."
    elif self.status == "CANCELLED":
      return False, "Reservasi sudah dibatalkan sebelumnya."
    elif self.status == "REJECTED":
      return False, "Reservasi yang ditolak tidak perlu dibatalkan."
    return False, "Status tidak valid."
