import flet as ft
from views.reservation_card import build_reservation_card


class HistoryView:
    """Halaman Riwayat: reservasi milik pengguna yang sedang masuk."""

    def __init__(self, reservation_service, get_current_user, on_action):
        self.reservation_service = reservation_service
        self.get_current_user = get_current_user
        self.on_action = on_action
        self.control = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh(self):
        user = self.get_current_user()
        self.control.controls.clear()
        self.control.controls.append(ft.Text("Riwayat Reservasi Saya", size=20, weight="bold"))

        items = self.reservation_service.get_user_reservations(user.name)
        if not items:
            self.control.controls.append(ft.Text("Belum ada reservasi.", italic=True))
        for res in reversed(items):  # terbaru di atas
            buttons = []
            if res.is_active and self.reservation_service.can_cancel(res, user):
                buttons.append(
                    ft.Button("Batalkan", on_click=lambda e, r=res: self.on_action(r, "cancel"))
                )
            self.control.controls.append(build_reservation_card(res, buttons))
