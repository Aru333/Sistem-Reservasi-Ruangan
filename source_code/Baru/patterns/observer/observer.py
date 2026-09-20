"""Saat terjadi perubahan status reservasi (Pending -> Approved / Rejected), 
service memanggil metode notify() untuk memperbarui antarmuka log/notifikasi 
secara otomatis tanpa pengikatan langsung antara service dan UI Flet."""

# Nama event (biar tidak salah ketik string di banyak tempat)
RESERVATION_CREATED = "RESERVATION_CREATED"
STATUS_CHANGED = "STATUS_CHANGED"


class Observer:
    """Siapa pun yang ingin diberi tahu harus punya method update()."""

    def update(self, event_type, reservation, message):
        raise NotImplementedError


class Subject:
    """Yang 'mengumumkan' kejadian. Menyimpan daftar pendengar (observer)."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type, reservation, message):
        for observer in self._observers:
            observer.update(event_type, reservation, message)