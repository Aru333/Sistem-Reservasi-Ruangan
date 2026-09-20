from datetime import datetime, timedelta
import json
import os
from models.reservation import Reservation


class ReservationService:

  ALLOWED_USERS = [
      "Muhammad Arden Abdalla",
      "Muhammad Hibat",
      "Muhammad Arfan",
      "Farizi",
  ]

  def __init__(self, room_service, file_path="data_reservations.json"):
    self.room_service = room_service
    self.file_path = file_path
    self.reservations = []
    self.load_from_json()

  def validate_user(self, user_name):
    return user_name in self.ALLOWED_USERS
  
  #Konversi time_str (HH:MM) + durasi menjadi datetime object untuk komparasi mudah.
  def _calculate_end_time(self, time_str, duration_hours):
    start_dt = datetime.strptime(time_str, "%H:%M")
    end_dt = start_dt + timedelta(hours=duration_hours)
    return start_dt, end_dt

  #Mengecek apakah jadwal baru bentrok dengan reservasi aktif (APPROVED / PENDING).
  def is_time_overlap(
      self, room_id, date_str, new_time_str, new_duration_hours
      ):
    
    new_start, new_end = self._calculate_end_time(
        new_time_str, new_duration_hours
    )

    for res in self.reservations:
      # Hanya cek reservasi di ruangan & tanggal yang sama, dan statusnya belum CANCELLED/REJECTED
      if (
          res.room.room_id == room_id
          and res.date_str == date_str
          and res.status in ["PENDING", "APPROVED"]
          ):

        existing_start, existing_end = self._calculate_end_time(
            res.time_str, res.duration_hours
        )

        # Logika Pengecekan bentrokan Waktu (Overlap Condition)
        if existing_start < new_end and new_start < existing_end:
          return True, res  # Terjadi bentrok!

    return False, None

  def create_reservation(
    self, user_name, room, date_str, time_str, duration_hours
    ):
    # Validasi Whitelist user
    if not self.validate_user(user_name):
      return (
          False,
          f"Akses Ditolak: Nama '{user_name}' tidak terdaftar dalam sistem!",
          None,
          )

    # Validasi Jadwal Bentrok
    is_clash, existing_res = self.is_time_overlap(
        room.room_id, date_str, time_str, duration_hours
    )
    if is_clash:
      end_time_str = (
          datetime.strptime(existing_res.time_str, "%H:%M")
          + timedelta(hours=existing_res.duration_hours)
      ).strftime("%H:%M")
      return (
          False,
          (
              f"Jadwal Bentrok! Ruangan '{room.name}' sudah direservasi pada jam {existing_res.time_str} - "
              f"{end_time_str} WIB (Status: {existing_res.status})."
          ),
          None,
      )

    # Buat Reservasi Baru Jika Tidak Bentrok
    res_id = len(self.reservations) + 1
    new_res = Reservation(
        res_id, user_name, room, date_str, time_str, duration_hours
        )
    self.reservations.append(new_res)

    # Simpan perubahan ke JSON
    self.save_to_json()
    return (
        True,
        f"Reservasi baru #{res_id} ({date_str} jam {time_str} selama"
        f"{duration_hours} jam berhasil diajukan oleh {user_name}",
        new_res,
    )

  # Mengubah objek Reservation menjadi list of dictionary dan menyimpannya ke file JSON.
  def save_to_json(self):
    data = []
    for res in self.reservations:
      data.append({
          "res_id": res.res_id,
          "user_name": res.user_name,
          "room_id": res.room.room_id,  # Cukup simpan ID ruangan
          "date_str": res.date_str,
          "time_str": res.time_str,
          "duration_hours": res.duration_hours,
          "status": res.status,
      })

    with open(self.file_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4)

  # Membaca file JSON dan merekonstruksi kembali menjadi objek Reservation.
  def load_from_json(self):
    if not os.path.exists(self.file_path):
      return  # Jika file belum ada, biarkan list kosong

    try:
      with open(self.file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        self.reservations = []
        for item in data:
          # Cari objek room berdasarkan room_id yang tersimpan
          room = self.room_service.find_room_by_id(item["room_id"])
          if room:
            #time_val = item.get("time_str", "08:00")
            res = Reservation(
                item["res_id"], 
                item["user_name"], 
                room, 
                item["date_str"],
                item["time_str"],
                item["duration_hours"]
                #time_val,
                
            )
            res.status = item["status"]  # Pulihkan status terakhir
            self.reservations.append(res)
    except Exception as e:
      print(f"Gagal memuat data dari JSON: {e}")

  def get_all_reservations(self):
    return self.reservations