"""Mencegah terjadinya switch-case atau nested if-else yang rumit di dalam
class Reservation saat mengeksekusi metode approve(), reject(), atau cancel()"""

class ReservationState:
    """Dasar: semua aksi ditolak. Subclass hanya membuka aksi yang boleh."""
    name = ""
    blocks_schedule = False  # apakah status ini memblokir jadwal ruangan
    reviewable = False       # apakah status ini masih menunggu keputusan admin

    def approve(self, reservation):
        return False, f"Tidak dapat menyetujui reservasi berstatus {self.name}."

    def reject(self, reservation):
        return False, f"Tidak dapat menolak reservasi berstatus {self.name}."

    def cancel(self, reservation):
        return False, f"Tidak dapat membatalkan reservasi berstatus {self.name}."


class PendingState(ReservationState):
    name = "PENDING"
    blocks_schedule = True
    reviewable = True

    def approve(self, reservation):
        reservation.state = ApprovedState()
        return True, "Reservasi berhasil disetujui."

    def reject(self, reservation):
        reservation.state = RejectedState()
        return True, "Reservasi telah ditolak."

    def cancel(self, reservation):
        reservation.state = CancelledState()
        return True, "Reservasi berhasil dibatalkan."


class ApprovedState(ReservationState):
    name = "APPROVED"
    blocks_schedule = True

    def cancel(self, reservation):
        reservation.state = CancelledState()
        return True, "Reservasi berhasil dibatalkan."


class RejectedState(ReservationState):
    name = "REJECTED"
    reviewable = True

class CancelledState(ReservationState):
    name = "CANCELLED"


_STATES = {s.name: s for s in (PendingState, ApprovedState, RejectedState, CancelledState)}


def state_from_name(name):
    """Dipakai saat memuat JSON: teks status -> objek state."""
    return _STATES[name]()