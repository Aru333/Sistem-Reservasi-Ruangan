import flet as ft
from patterns.observer.observer import Observer
from views.catalog_view import CatalogView
from views.reservation_form_view import ReservationFormView
from views.history_view import HistoryView
from views.approval_view import ApprovalView
from views.notification_view import NotificationView

# (kunci halaman, label menu, ikon, hanya untuk admin?)
MENU = [
    ("catalog", "Katalog", ft.Icons.MEETING_ROOM, False),
    ("form", "Ajukan", ft.Icons.ADD_CIRCLE_OUTLINE, False),
    ("history", "Riwayat", ft.Icons.HISTORY, False),
    ("approval", "Persetujuan", ft.Icons.ADMIN_PANEL_SETTINGS, True),
    ("notifications", "Notifikasi", ft.Icons.NOTIFICATIONS, False),
]


class AppShell(Observer):
    """Kerangka aplikasi: header, menu navigasi, dan area konten yang berganti halaman."""

    def __init__(self, page, room_service, reservation_service, user_service, notification_service):
        self.page = page
        self.reservation_service = reservation_service
        self.user_service = user_service
        self.current_user = user_service.get_all_users()[0]
        self.current_key = "catalog"

        self.pages = {
            "catalog": CatalogView(room_service),
            "form": ReservationFormView(
                page, room_service, reservation_service, self.get_current_user, self.show_message
            ),
            "history": HistoryView(reservation_service, self.get_current_user, self.handle_action),
            "approval": ApprovalView(reservation_service, self.get_current_user, self.handle_action),
            "notifications": NotificationView(notification_service, self.get_current_user),
        }
        self.setup_ui()

    def get_current_user(self):
        return self.current_user

    def visible_menu(self):
        return [m for m in MENU if not m[3] or self.current_user.is_admin()]

    def setup_ui(self):
        self.page.title = "Sistem Reservasi Ruangan"
        self.page.window.width = 950
        self.page.window.height = 800

        self.user_dropdown = ft.Dropdown(
            label="Masuk sebagai",
            width=300,
            options=[
                ft.dropdown.Option(key=u.name, text=f"{u.name} ({u.role})")
                for u in self.user_service.get_all_users()
            ],
            value=self.current_user.name,
            on_select=self.on_user_change,
        )
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[],
            on_change=self.on_nav_change,
        )
        self.content_area = ft.Container(expand=True, padding=10)
        self.status_text = ft.Text("", size=12)
        self.rebuild_menu()  # isi menu SEBELUM ditambahkan ke halaman

        self.page.add(
            ft.Row([
                ft.Text("Sistem Reservasi Ruangan", size=20, weight="bold"),
                ft.Container(expand=True),
                self.user_dropdown,
            ]),
            ft.Divider(),
            ft.Row([self.rail, ft.VerticalDivider(width=1), self.content_area], expand=True),
            ft.Divider(),
            self.status_text,
        )
        self.show_page("catalog")

    def rebuild_menu(self):
        menu = self.visible_menu()
        self.rail.destinations = [
            ft.NavigationRailDestination(icon=icon, label=label) for _, label, icon, _ in menu
        ]
        keys = [m[0] for m in menu]
        self.rail.selected_index = keys.index(self.current_key) if self.current_key in keys else 0

    def on_nav_change(self, e):
        key = self.visible_menu()[self.rail.selected_index][0]
        self.show_page(key)

    def show_page(self, key):
        self.current_key = key
        page_obj = self.pages[key]
        page_obj.refresh()
        self.content_area.content = page_obj.control
        self.page.update()

    def on_user_change(self, e):
        user = self.user_service.find_by_name(self.user_dropdown.value)
        if not user:
            return
        self.current_user = user
        if self.current_key not in [m[0] for m in self.visible_menu()]:
            self.current_key = "catalog"  # halaman admin tidak boleh diakses pemohon
        self.rebuild_menu()
        self.status_text.value = ""
        self.show_page(self.current_key)

    def show_message(self, message, is_error=False):
        self.status_text.value = message
        self.status_text.color = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        self.page.update()

    # Dipanggil OTOMATIS oleh ReservationService setiap ada kejadian (Observer)
    def update(self, event_type, reservation, message):
        self.show_message(message)
        self.pages[self.current_key].refresh()
        self.page.update()

    def handle_action(self, res, action_type):
        user = self.current_user
        if action_type == "approve":
            success, msg = self.reservation_service.approve_reservation(res, user)
        elif action_type == "reject":
            success, msg = self.reservation_service.reject_reservation(res, user)
        else:
            success, msg = self.reservation_service.cancel_reservation(res, user)

        # Kalau berhasil, pesan & refresh halaman terjadi otomatis lewat Observer
        if not success:
            self.show_message(f"Gagal mengubah status: {msg}", is_error=True)
