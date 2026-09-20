import flet as ft

STATUS_COLORS = {
    "PENDING": ft.Colors.ORANGE_700,
    "APPROVED": ft.Colors.GREEN_700,
    "REJECTED": ft.Colors.RED_700,
    "CANCELLED": ft.Colors.GREY_700,
}


def build_reservation_card(res, buttons=None):
    """Kartu reservasi yang dipakai bersama oleh halaman Riwayat dan Persetujuan."""
    return ft.Card(
        content=ft.Container(
            padding=10,
            content=ft.Column([
                ft.Text(f"ID #{res.res_id} - {res.user_name} | {res.room.name}", weight="bold"),
                ft.Text(f"Jadwal: {res.date_str} pukul {res.time_str} WIB, {res.duration_hours} jam"),
                ft.Text(f"Tujuan: {res.purpose or '-'}"),
                ft.Text(f"Status: {res.status}", weight="bold", color=STATUS_COLORS.get(res.status)),
                ft.Row(buttons or []),
            ]),
        )
    )
