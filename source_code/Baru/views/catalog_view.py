import flet as ft


class CatalogView:
    """Halaman Katalog: daftar ruangan beserta detailnya."""

    def __init__(self, room_service):
        self.room_service = room_service
        self.control = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh(self):
        self.control.controls.clear()
        self.control.controls.append(ft.Text("Katalog Ruangan", size=20, weight="bold"))
        for room in self.room_service.get_all_rooms():
            self.control.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(room.name, weight="bold"),
                            ft.Text(room.get_description()),
                            ft.Text(
                                f"Durasi maksimum: {room.max_duration_hours} jam",
                                italic=True,
                                size=12,
                            ),
                        ]),
                    )
                )
            )
