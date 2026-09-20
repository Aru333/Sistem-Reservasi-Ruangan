from datetime import datetime, timedelta
import flet as ft

class ReservationAppView:
    def __init__(self, page: ft.Page, room_service, reservation_service):
        self.page = page
        self.room_service = room_service
        self.reservation_service = reservation_service
        
        self.selected_date_val = [None]
        self.selected_time_val = [None]
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "Sistem Reservasi Ruangan (Tanpa Pattern)"
        self.page.window.width = 900
        self.page.window.height = 850

        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        self.user_input = ft.TextField(
            label="Nama Pemesan",
            width=300,
            hint_text="Masukkan nama terdaftar..."
        )
        self.room_dropdown = ft.Dropdown(
            label="Pilih Ruangan",
            width=300,
            options=[
                ft.dropdown.Option(key=str(r.room_id), text=r.name) 
                for r in self.room_service.get_all_rooms()
            ],
        )
        self.selected_date_text = ft.Text("Belum memilih tanggal", color=ft.Colors.GREY_700)
        self.selected_time_text = ft.Text("Belum memilih waktu", color=ft.Colors.GREY_700)

        # DATE PICKER
        self.date_picker = ft.DatePicker(
            first_date=tomorrow,
            on_change=self.on_date_change
        )
        self.page.overlay.append(self.date_picker)

        btn_pick_date = ft.Button(
            "Pilih Tanggal via Kalender",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_date_picker
        )

        # TIME PICKER
        self.selected_time_text = ft.Text(
            "Pilih tanggal terlebih dahulu", color=ft.Colors.GREY_500
        )
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
            options=[
            ft.dropdown.Option(key="1", text="1 Jam"),
            ft.dropdown.Option(key="2", text="2 Jam"),
            ft.dropdown.Option(key="3", text="3 Jam"),
            ft.dropdown.Option(key="4", text="4 Jam"),
            ],
            value="1", #durasi awal 1 jam
        )


        self.reservation_list_column = ft.Column()
        self.log_column = ft.Column()

        submit_btn = ft.Button("Ajukan Reservasi", on_click=self.submit_reservation)
        allowed_text = ", ".join(self.reservation_service.ALLOWED_USERS)

        self.page.add(
            ft.Text(
                "Sistem Reservasi Ruangan (Tanpa Pattern)", 
                size=20, 
                weight="bold",
                ),
            ft.Row([
                ft.Column([
                    ft.Text("Form Pengajuan", weight="bold"),
                    self.user_input,
                    ft.Text(f"User terdaftar: {allowed_text}", size=11, italic=True),
                    self.room_dropdown,
                    btn_pick_date,
                    self.selected_date_text,
                    self.btn_pick_time,
                    self.selected_time_text,
                    self.duration_dropdown,
                    submit_btn,
                ]),
                ft.VerticalDivider(width=20),
                ft.Column([
                    ft.Text("Daftar Reservasi", weight="bold"),
                    self.reservation_list_column
                ])
            ]),
            ft.Divider(),
            ft.Text("Log System / Notification Area", weight="bold"),
            self.log_column
        )
        #render reservasi file JSON setelah launch aplikasi
        self.refresh_reservation_list()
        self.page.update()

    def open_date_picker(self, e):
        self.date_picker.open = True
        self.page.update()

    def on_date_change(self, e):
        if self.date_picker.value:
            self.selected_date_val[0] = self.date_picker.value.strftime("%Y-%m-%d")
            self.selected_date_text.value = f"Terpilih: {self.selected_date_val[0]}"
            self.selected_date_text.color = ft.Colors.GREEN_700
            self.btn_pick_time.disabled = False # aktifkan tomboljam setelah pilih tanggal
            self.selected_time_text.value = "belum memilih jam"
            self.selected_time_text.color = ft.Colors.GREY_700
            self.page.update()

    def open_time_picker(self, e):
        self.time_picker.open = True
        self.page.update

    def on_time_change(self, e):
        if self.time_picker.value:
            self.selected_time_val[0] = self.time_picker.value.strftime("%H:%M")
            self.selected_time_text.value = f"Mulai: {self.selected_time_val[0]} WIB"
            self.selected_time_text.color = ft.Colors.GREEN_700
            self.page.update() 


    def update_ui_and_notify(self, message):
        self.log_column.controls.append(ft.Text(f"[LOG NOTIFIKASI]: {message}"))
        self.refresh_reservation_list()
        self.page.update()

    def refresh_reservation_list(self):
        self.reservation_list_column.controls.clear()
        for res in self.reservation_service.get_all_reservations():
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"ID #{res.res_id} - {res.user_name} | {res.room.name}", weight="bold"
                            ),
                        ft.Text(
                            f"Jadwal: {res.date_str} Pukul {res.time_str} WIB "
                            f"{res.duration_hours} Jam| Status: {res.status}"
                            ),
                        ft.Row([
                            ft.Button("Setujui", on_click=lambda e, r=res: self.handle_action(r, "approve")),
                            ft.Button("Tolak", on_click=lambda e, r=res: self.handle_action(r, "reject")),
                            ft.Button("Batalkan", on_click=lambda e, r=res: self.handle_action(r, "cancel")),
                        ])
                    ]),
                    padding=10
                )
            )
            self.reservation_list_column.controls.append(card)

    def handle_action(self, res, action_type):
        if action_type == "approve":
            success, msg = res.approve()
        elif action_type == "reject":
            success, msg = res.reject()
        elif action_type == "cancel":
            success, msg = res.cancel()

        if success:
            # Simpan status terbaru ke file JSON
            self.reservation_service.save_to_json()
            self.update_ui_and_notify(
                f"Reservasi #{res.res_id} status berubah menjadi {res.status}"
            )
        else:
            self.update_ui_and_notify(f"Gagal mengubah status: {msg}")

    def submit_reservation(self, e):
        input_user = self.user_input.value.strip() if self.user_input.value else ""

        if (
            not input_user or not self.room_dropdown.value 
            or not self.selected_date_val[0]
            or not self.selected_time_val[0]
            ):
            self.update_ui_and_notify("Mohon isi nama, pilih ruangan, tanggal, dan jam!")
            return

        selected_room = self.room_service.find_room_by_id(self.room_dropdown.value)
        duration_val = int (self.duration_dropdown.value)

        success, msg, _ = self.reservation_service.create_reservation(
            input_user, 
            selected_room, 
            self.selected_date_val[0],
            self.selected_time_val[0],
            duration_val,
        )

        self.update_ui_and_notify(msg)

        if success:
            #reset form
            self.user_input.value = ""
            self.selected_date_val[0] = None
            self.selected_time_val[0] = None
            self.selected_date_text.value = "Belum memilih tanggal"
            self.selected_date_text.color = ft.Colors.GREY_700
            # kunci lagi tombol jam
            self.btn_pick_time.disabled = True
            self.selected_time_text.value = "Pilih tanggal terlebih dahulu"
            self.selected_time_text.color = ft.Colors.GREY_700
            self.page.update()