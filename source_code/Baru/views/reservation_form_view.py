from datetime import datetime, timedelta
import flet as ft


class ReservationFormView:
    """Halaman Ajukan: form pengajuan reservasi."""

    def __init__(self, page, room_service, reservation_service, get_current_user, show_message):
        self.page = page
        self.room_service = room_service
        self.reservation_service = reservation_service
        self.get_current_user = get_current_user
        self.show_message = show_message

        self.selected_date = None
        self.selected_time = None

        self.room_dropdown = ft.Dropdown(
            label="Pilih Ruangan",
            width=300,
            options=[
                ft.dropdown.Option(key=str(r.room_id), text=r.name)
                for r in self.room_service.get_all_rooms()
            ],
        )

        # DATE PICKER
        tomorrow = datetime.now() + timedelta(days=1)
        self.selected_date_text = ft.Text("Belum memilih tanggal", color=ft.Colors.GREY_700)
        self.date_picker = ft.DatePicker(first_date=tomorrow, on_change=self.on_date_change)
        self.page.overlay.append(self.date_picker)
        self.btn_pick_date = ft.Button(
            "Pilih Tanggal via Kalender",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_date_picker,
        )

        # TIME PICKER
        self.selected_time_text = ft.Text("Pilih tanggal terlebih dahulu", color=ft.Colors.GREY_500)
        self.time_picker = ft.TimePicker(
            confirm_text="Pilih",
            error_invalid_text="Waktu tidak valid",
            help_text="Tentukan Jam & Menit",
            on_change=self.on_time_change,
        )
        self.page.overlay.append(self.time_picker)
        self.btn_pick_time = ft.Button(
            "Pilih Waktu Mulai",
            icon=ft.Icons.ACCESS_TIME,
            disabled=True,
            on_click=self.open_time_picker,
        )

        self.duration_dropdown = ft.Dropdown(
            label="Durasi Penggunaan (jam)",
            width=300,
            options=[ft.dropdown.Option(key=str(i), text=f"{i} Jam") for i in (1, 2, 3, 4)],
            value="1",
        )
        self.purpose_input = ft.TextField(
            label="Tujuan Reservasi",
            width=300,
            hint_text="Contoh: Rapat organisasi",
            max_length=100,
        )

        self.control = ft.Column(
            [
                ft.Text("Ajukan Reservasi", size=20, weight="bold"),
                self.room_dropdown,
                self.btn_pick_date,
                self.selected_date_text,
                self.btn_pick_time,
                self.selected_time_text,
                self.duration_dropdown,
                self.purpose_input,
                ft.Button("Ajukan Reservasi", on_click=self.submit),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def refresh(self):
        pass  # form tidak perlu dimuat ulang

    def open_date_picker(self, e):
        self.date_picker.open = True
        self.page.update()

    def on_date_change(self, e):
        if self.date_picker.value:
            self.selected_date = self.date_picker.value.strftime("%Y-%m-%d")
            self.selected_date_text.value = f"Terpilih: {self.selected_date}"
            self.selected_date_text.color = ft.Colors.GREEN_700
            self.btn_pick_time.disabled = False
            self.selected_time = None
            self.selected_time_text.value = "belum memilih jam"
            self.selected_time_text.color = ft.Colors.GREY_700
            self.page.update()

    def open_time_picker(self, e):
        self.time_picker.open = True
        self.page.update()

    def on_time_change(self, e):
        if self.time_picker.value:
            self.selected_time = self.time_picker.value.strftime("%H:%M")
            self.selected_time_text.value = f"Mulai: {self.selected_time} WIB"
            self.selected_time_text.color = ft.Colors.GREEN_700
            self.page.update()

    def submit(self, e):
        if not (self.room_dropdown.value and self.selected_date and self.selected_time):
            self.show_message("Mohon pilih ruangan, tanggal, dan jam!", is_error=True)
            return

        room = self.room_service.find_room_by_id(self.room_dropdown.value)
        success, msg, _ = self.reservation_service.create_reservation(
            self.get_current_user().name,
            room,
            self.selected_date,
            self.selected_time,
            int(self.duration_dropdown.value),
            self.purpose_input.value,
        )
        if not success:
            self.show_message(msg, is_error=True)
            return

        # Berhasil: pesan sukses datang otomatis lewat Observer. Tinggal reset form.
        self.purpose_input.value = ""
        self.selected_date = None
        self.selected_time = None
        self.selected_date_text.value = "Belum memilih tanggal"
        self.selected_date_text.color = ft.Colors.GREY_700
        self.btn_pick_time.disabled = True
        self.selected_time_text.value = "Pilih tanggal terlebih dahulu"
        self.selected_time_text.color = ft.Colors.GREY_700
        self.page.update()
