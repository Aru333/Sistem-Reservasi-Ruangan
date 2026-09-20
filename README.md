# Sistem-Reservasi-Ruangan
Tugas Kelompok Metode Pemrograman Modern

https://github.com/Aru333/Sistem-Reservasi-Ruangan

Anggota Kelompok:
1. Muhammad Arden Abdalla - 21060121130087 
2. Muhammad Hibat Al Alimi - 21060121140164
3. Farizi Nufairi Ilman - 21060122140173

Cara Menjalankan Kode/Aplikasi:
1. buat virtual environment dengan "python -m venv venv"
2. masuk ke virtual environment dengan "source venv/bin/activate"
3. masuk ke folder SistemReservasiRuangan dengan "cd SistemReservasiRuangan/"
4. install semua requirements termasuk flet dengan "pip install -r requirements.txt"
5. jalankan kode/aplikasi python dengan "flet run main.py"

Target Pengguna:
1. Mahasiswa
2. Dosen

Fitur Utama:
1. Katalog & Detail Ruangan (fasilitas, kapasitas, status). 
2. Pengajuan Reservasi Ruangan (pilih tanggal, jam, dan tujuan) oleh pengguna terautentikasi (services/reservation_service.py). 
3. Pengelolaan Status Reservasi oleh Admin(Pending Approved Rejected Cancelled) dan auto-cancel untuk multi pending cases  // 
4. Riwayat Pemesanan & Dashboard Notifikasi. 

Aplikasi ini menggunakan 3 Design Pattern:

1. Factory Method (`patterns/factory/`)
   **Masalah**: Menghindari pengondisian `if-else` manual pada models/room.py saat pembuatan objek berbagai tipe ruangan
   **Solusi**: Kelas `RoomFactory` mengisolasi pembuatan instansiasi kelas `MeetingRoom`, `LabRoom`, dan `Auditorium`
2. State Pattern (`patterns/state/`)
   **Masalah**: Mencegah aturan transisi status reservasi yang rumit dan bertumpuk di kelas utama pada models/reservation.py
   **Solusi**: Kelas `ReservationState` enkapsulasi aksi yang diizinkan untuk setiap status (`PendingState`, `ApprovedState`, `RejectedState`, `CancelledState`)
3. Observer Pattern (`patterns/observer/`)
   **Masalah**: Memperbarui tampilan log/notifikasi UI dengan update_ui_and_notify() pada views/main_view.py tanpa mengaitkan logika `ReservationService` secara langsung dengan Flet UI
   **Solusi**: Kelas `Subject` memanggil method `notify()` saat terjadi perubahan event untuk memperbarui seluruh antarmuka `Observer` secara otomatis


