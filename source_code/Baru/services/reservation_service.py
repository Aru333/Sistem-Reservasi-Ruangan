from datetime import datetime, timedelta
import json
import os
from models.reservation import Reservation
from patterns.observer.observer import RESERVATION_CREATED, STATUS_CHANGED, Subject


class ReservationService(Subject):

  def __init__(
      self, room_service, user_service, file_path="data_reservations.json"
  ):
    super().__init__()
    self.room_service = room_service
    self.user_service = user_service
    self.file_path = file_path
    self.reservations = []
    self.load_from_json()

  def validate_user(self, user_name):
    return self.user_service.find_by_name(user_name) is not None

  # ---- Aturan hak akses (dipakai service DAN view, jadi aturannya cuma di sini) ----
  def can_review(self, actor):
    # hanya admin yang boleh menyetujui / menolak
    return actor.is_admin()

  def can_cancel(self, res, actor):
    # admin boleh membatalkan apa saja; pemohon hanya miliknya sendiri
    return actor.is_admin() or res.user_name == actor.name

  def get_user_reservations(self, user_name):
    return [r for r in self.reservations if r.user_name == user_name]

  def get_active_reservations(self):
    # reservasi yang masih "hidup" (Pending & Approved)
    return [r for r in self.reservations if r.is_active]

  # Konversi time_str (HH:MM) + durasi menjadi datetime object untuk komparasi mudah.
  def _calculate_end_time(self, time_str, duration_hours):
    start_dt = datetime.strptime(time_str, "%H:%M")
    end_dt = start_dt + timedelta(hours=duration_hours)
    return start_dt, end_dt

  # Mengecek apakah jadwal baru bentrok dengan reservasi aktif (APPROVED / PENDING).
  def is_time_overlap(
      self, room_id, date_str, new_time_str, new_duration_hours
  ):

    new_start, new_end = self._calculate_end_time(
        new_time_str, new_duration_hours
    )

    for res in self.reservations:
      # Hanya cek reservasi di ruangan & tanggal yang sama, dan statusnya APPROVED
      if (
          res.room.room_id == room_id
          and res.date_str == date_str
          and res.status == "APPROVED"
      ):

        existing_start, existing_end = self._calculate_end_time(
            res.time_str, res.duration_hours
        )

        # Logika Pengecekan bentrokan Waktu (Overlap Condition)
        if existing_start < new_end and new_start < existing_end:
          return True, res  # Terjadi bentrok!

    return False, None

  # Batalkan otomatis reservasi PENDING lain yang jadwalnya bentrok dengan reservasi yang sudah diAPPROVE
  def cancel_conflicting_pending_reservations(self, approved_res):
    app_start, app_end = self._calculate_end_time(
        approved_res.time_str, approved_res.duration_hours
    )
    cancelled_count = 0

    for res in self.reservations:
      # Cari reservasi lain pada ruangan & tanggal sama yang masih PENDING
      if (
          res.res_id != approved_res.res_id
          and res.room.room_id == approved_res.room.room_id
          and res.date_str == approved_res.date_str
          and res.status == "PENDING"
      ):

        p_start, p_end = self._calculate_end_time(
            res.time_str, res.duration_hours
        )

        # Jika waktunya bentrok, ubah status menjadi CANCELLED/REJECTED
        if p_start < app_end and app_start < p_end:
          # Jika menggunakan State Pattern, panggil transition/set_state ke CancelledState
          if hasattr(res, "cancel"):
            res.cancel()
          else:
            res.status = "CANCELLED"
          cancelled_count += 1

    return cancelled_count

  # Bikin Reservasi
  def create_reservation(
      self, user_name, room, date_str, time_str, duration_hours, purpose
  ):
    # Validasi Whitelist user
    if not self.validate_user(user_name):
      return (
          False,
          f"Akses Ditolak: Nama '{user_name}' tidak terdaftar dalam sistem!",
          None,
      )

    # Validasi tujuan reservasi
    purpose = purpose.strip() if purpose else ""
    if not purpose:
      return False, "Tujuan reservasi wajib diisi!", None
    if len(purpose) > 100:
      return False, "Tujuan reservasi maksimal 100 karakter.", None

    # Validasi durasi maksimum sesuai tipe ruangan
    if duration_hours > room.max_duration_hours:
      return (
          False,
          (
              f"Durasi terlalu lama! {room.name} maksimal"
              f" {room.max_duration_hours} jam."
          ),
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
              f"Jadwal Bentrok! Ruangan '{room.name}' sudah direservasi pada"
              f" jam {existing_res.time_str} - {end_time_str} WIB (Status:"
              f" {existing_res.status})."
          ),
          None,
      )

    # Buat Reservasi Baru Jika Tidak Bentrok
    res_id = len(self.reservations) + 1
    new_res = Reservation(
        res_id, user_name, room, date_str, time_str, duration_hours, purpose
    )
    self.reservations.append(new_res)

    # Simpan perubahan ke JSON
    self.save_to_json()
    message = (
        f"Reservasi baru #{res_id} ({date_str} jam {time_str} selama "
        f"{duration_hours} jam) berhasil diajukan oleh {user_name}"
    )
    self.notify(RESERVATION_CREATED, new_res, message)
    return True, message, new_res

  def approve_reservation(self, res, actor):
    if not self.can_review(actor):
      return False, "Hanya admin yang boleh menyetujui reservasi."
    return self._apply_action(res, res.approve)

  def reject_reservation(self, res, actor):
    if not self.can_review(actor):
      return False, "Hanya admin yang boleh menolak reservasi."
    return self._apply_action(res, res.reject)

  def cancel_reservation(self, res, actor):
    if not self.can_cancel(res, actor):
      return False, "Kamu hanya boleh membatalkan reservasi milikmu sendiri."
    return self._apply_action(res, res.cancel)

  def _apply_action(self, res, action):
    success, msg = action()
    if success:
      if res.status == "APPROVED":
        self.cancel_conflicting_pending_reservations(res)
      self.save_to_json()
      self.notify(
          STATUS_CHANGED,
          res,
          f"Reservasi #{res.res_id} status berubah menjadi {res.status}",
      )
    return success, msg

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
          "purpose": res.purpose,
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
            res = Reservation(
                item["res_id"],
                item["user_name"],
                room,
                item["date_str"],
                item["time_str"],
                item["duration_hours"],
                item.get("purpose", ""),
            )
            res.status = item["status"]  # Pulihkan status terakhir
            self.reservations.append(res)
    except Exception as e:
      print(f"Gagal memuat data dari JSON: {e}")

  def get_all_reservations(self):
    return self.reservations