import flet as ft
from patterns.observer.observer import RESERVATION_CREATED, STATUS_CHANGED

EVENT_LABELS = {
    RESERVATION_CREATED: "Reservasi baru",
    STATUS_CHANGED: "Perubahan status",
}


class NotificationView:
    """Halaman Notifikasi (dashboard): riwayat kejadian dari NotificationService."""

    def __init__(self, notification_service, get_current_user):
        self.notification_service = notification_service
        self.get_current_user = get_current_user
        self.control = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh(self):
        user = self.get_current_user()
        self.control.controls.clear()
        self.control.controls.append(ft.Text("Dashboard Notifikasi", size=20, weight="bold"))

        items = self.notification_service.get_for(user)
        if not items:
            self.control.controls.append(ft.Text("Belum ada notifikasi.", italic=True))
        for n in items:
            label = EVENT_LABELS.get(n["event"], n["event"])
            self.control.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(f"{label} - {n['time']}", size=12, italic=True),
                            ft.Text(n["message"]),
                        ]),
                    )
                )
            )
