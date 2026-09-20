import flet as ft
from views.reservation_card import build_reservation_card


class ApprovalView:
    """Halaman Persetujuan (khusus admin): reservasi yang masih aktif."""

    def __init__(self, reservation_service, get_current_user, on_action):
        self.reservation_service = reservation_service
        self.get_current_user = get_current_user
        self.on_action = on_action
        self.control = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh(self):
        user = self.get_current_user()
        self.control.controls.clear()
        self.control.controls.append(ft.Text("Persetujuan Reservasi", size=20, weight="bold"))

        items = self.reservation_service.get_active_reservations()
        if not items:
            self.control.controls.append(ft.Text("Tidak ada reservasi aktif.", italic=True))
        for res in reversed(items):
            buttons = []
            if res.is_reviewable and self.reservation_service.can_review(user):
                buttons.append(
                    ft.Button("Setujui", on_click=lambda e, r=res: self.on_action(r, "approve"))
                )
                buttons.append(
                    ft.Button("Tolak", on_click=lambda e, r=res: self.on_action(r, "reject"))
                )
            if self.reservation_service.can_cancel(res, user):
                buttons.append(
                    ft.Button("Batalkan", on_click=lambda e, r=res: self.on_action(r, "cancel"))
                )
            self.control.controls.append(build_reservation_card(res, buttons))
